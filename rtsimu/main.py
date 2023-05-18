import logging as log
import multiprocessing as mp
import hydra
import numpy as np
import opensim as osim  
import pandas as pd
from pathlib import Path
from typing import Union
from operator import attrgetter

from config_store import BaseConfig, register_configs
from data_collection.frames import Frame, FrameCollection
from data_collection.imu import IMUCollection
from data_collection.risk import Risk, RiskCollection
from evaluator import Evaluator, RiskLevel
from sensor import sensor_process
from utils import safe_eval

osim.Logger_setLevelString("Warn")

# Register hydra config classes
register_configs()

is_enabled = attrgetter("enabled")
get_details = attrgetter("name", "frame")

RAD2DEG = 180 / np.pi

def write_data(path: Path, data: Union[FrameCollection, IMUCollection, RiskCollection]) -> None:
    """
    Write data to file. Open file in append mode if it exists, otherwise open in write mode.

    :param path: path to write to.
    :type path: Path
    :param data: data to write.
    :type data: Union[FrameCollection, IMUCollection, RiskCollection]
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    data.to_csv(path, mode="a" if path.exists() else "w", header=not path.exists())

@hydra.main(config_path=Path("rtsimu/config").absolute().as_posix(), config_name="config", version_base=None)
def main(config: BaseConfig):
    """Main function."""
    logger = log.getLogger("MAIN")
    logger.info("System started.")

    logger.info("Initializing simulation tool.")
    sensor2osim = osim.Rotation(
        osim.SpaceRotationSequence,
        float(safe_eval(str(config.opensim.sensor_to_opensim_rotation.x))),
        osim.CoordinateAxis(0),
        float(safe_eval(str(config.opensim.sensor_to_opensim_rotation.y))),
        osim.CoordinateAxis(1),
        float(safe_eval(str(config.opensim.sensor_to_opensim_rotation.z))),
        osim.CoordinateAxis(2)
    )

    model = osim.Model(config.opensim.model_path)
    model.setUseVisualizer(config.opensim.visualize)
    state = model.initSystem()
    if config.opensim.visualize:
        model.getVisualizer().show(state)
        model.getVisualizer().getSimbodyVisualizer().setShowSimTime(True)
        model.getVisualizer().getSimbodyVisualizer().setShutdownWhenDestructed(True)

    logger.info("Sensors data processes.")
    sensor_details = dict(map(get_details, filter(is_enabled, config.sensor.sensors)))
    num_enabled_sensors = len(sensor_details)
    barrier = mp.Barrier(num_enabled_sensors)
    processes = {}
    queues = {}
    frame_names = {}

    # Identify and start a process for each sensor.
    for s in config.sensor.sensors:
        logger.debug("Starting Sensor data from %s." % s.name)
        q = mp.Queue()
        process = mp.Process(
            target=sensor_process,
            args=(barrier, s.name, 2, config.sensor.AHRS.settings, q)
        )
        processes[s.name] = process
        queues[s.name] = q
        frame_names[s.name] = sensor_details[s.name]
        process.start()

    logger.info("%d Sensor processes initialized: %s" % (len(processes), ", ".join(processes.keys())))

    curr_timestamp = 0.0
    frame_collection = FrameCollection()
    risk_evaluator = Evaluator(config.opensim.risk.severe.rules, config.opensim.risk.moderate.rules)
    severe_risk_collection = RiskCollection()
    moderate_risk_collection = RiskCollection()
    severe_risk = Risk()
    moderate_risk = Risk()


    quaternion_collection = {k: IMUCollection() for k in sensor_details.keys()}

    df = pd.read_csv(config.sensor.data_sensors+s.name+".csv")

    logger.info("Running...")
    
    while len(frame_collection) < len(df):
        if any(q.empty() for q in queues.values()):
            continue

        qtable = osim.TimeSeriesTableQuaternion([curr_timestamp])            

        # get quaternion and append to table
        for name, q in queues.items():
            qdata = q.get()[-1]
            quaternion_collection[name].append(qdata)
            qvector = osim.VectorQuaternion(
                1,
                osim.Quaternion(float(qdata.w), float(qdata.x), float(qdata.y), float(qdata.z))
            )
            qtable.appendColumn(frame_names[name], qvector)

        # Convert to OpenSim rotation.
        osim.OpenSenseUtilities.rotateOrientationTable(qtable, sensor2osim)

        # Inverse kinematics.
        ik_solver = osim.InverseKinematicsSolver(
            model,
            osim.MarkersReference(),
            osim.OrientationsReference(osim.OpenSenseUtilities.convertQuaternionsToRotations(qtable)),
            osim.SimTKArrayCoordinateReference()
        )
        state.setTime(curr_timestamp)
        ik_solver.assemble(state)
        ik_solver.track(state)
        if config.opensim.visualize:
            model.getVisualizer().show(state)
        frames = {}
        for frame, coord in config.opensim.coordinates.items():
            if coord is None:
                continue
            value = model.getCoordinateSet().get(coord).getValue(state) * RAD2DEG
            frames[frame] = value
        frame = Frame(time=curr_timestamp, **frames)
        frame_collection.append(frame)

        # Risk
        severe_risk_collection.append(risk_evaluator.eval_sev_risk(frame))
        moderate_risk_collection.append(risk_evaluator.eval_mod_risk(frame))
        logger.info("Frames collected: %s" % len(frame_collection))

        if len(severe_risk_collection) >= config.opensim.risk.severe.duration:
            severe_risk = \
                severe_risk_collection[-config.opensim.risk.severe.duration:].aggregate().logical_and()

        if len(moderate_risk_collection) >= config.opensim.risk.moderate.duration:
            moderate_risk = \
                moderate_risk_collection[-config.opensim.risk.moderate.duration:].aggregate().logical_and()

        curr_timestamp = round(curr_timestamp + 0.5, 2)
       
    for name, collection in quaternion_collection.items():
        write_data(Path(config.data_path) / name / "quaternions.csv", collection)
    write_data(Path(config.data_path) / "frames.csv", frame_collection)
    write_data(Path(config.data_path) / "severe_risk.csv", severe_risk_collection)
    write_data(Path(config.data_path) / "moderate_risk.csv", moderate_risk_collection)

    logger.info("Terminating process.")


if __name__ == "__main__":
    # Set the start method for multiprocessing.
    # The parent process starts a fresh Python interpreter process. The child process will only
    # inherit those resources necessary to run the process object’s run() method. In particular,
    # unnecessary file descriptors and handles from the parent process will not be inherited.
    mp.set_start_method("spawn")

    main()  
