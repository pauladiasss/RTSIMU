"""Sensor process."""

import time
from typing import Tuple
from multiprocessing import Barrier, Queue

import imufusion
import pandas as pd
import numpy as np

from config_store.sensor_schema import AHRSSettings
from data_collection.imu import IMUCollection, IMUData, IMUSensorLabels, QuaternionData
from utils import create_colorlog_logger


def sensor_process(
        barrier: Barrier, name: str, frequency: int, ahrs_settings: AHRSSettings, queue: Queue
) -> None:
    """
    Read data from the serial port and return the quaternion obtained from teh sensor fusion.
    :param barrier: barrier to synchronize the processes.
    :type barrier: multiprocessing.Barrier
    :param name: sensor name.
    :type name: str
    :param frequency: frequency of the sensor.
    :type frequency: int
    :param ahrs_settings: settings for the sensor fusion.
    :type ahrs_settings: AHRSSettings
    :param queue: queue to send the quaternion to.
    :type queue: multiprocessing.Queue
    """

    logger = create_colorlog_logger(name=name)

    logger.info("Process started.")
    num_lines_read = 0
    num_sensor_lines = {s: 0 for s in IMUSensorLabels()}
    collection = {sensor: IMUCollection() for sensor in IMUSensorLabels()}
    quaternions = IMUCollection()
    ahrs = imufusion.Ahrs()
    ahrs.settings = imufusion.Settings(
        float(ahrs_settings.gain),
        float(ahrs_settings.acceleration_rejection),
        float(ahrs_settings.magnetic_rejection),
        int(ahrs_settings.rejection_timeout),
    )
    offset = imufusion.Offset(frequency)
    barrier.wait()

    logger.info("Data from sensor.")

    df = pd.read_csv("/data/data_sensors/"+name+".csv")
    
    for row in df.itertuples(index=False, name='Pandas'):

        timestamp = row[0]
        gyr = np.array(row[1:4])
        acc = np.array(row[4:7])
        mag = np.array(row[7:])

        ahrs.update(
            offset.update(gyr),
            acc,
            mag,
            round(1/frequency, 2),
        )

        quaternions.append(QuaternionData(timestamp, *[round(n, 5) for n in ahrs.quaternion.array.round(5)]))
        queue.put(quaternions.flush(1))
