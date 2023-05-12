from dataclasses import MISSING, dataclass, field
from hydra.core.config_store import ConfigStore
from .sensor_schema import SensorConfig
from .opensim_schema import OpensimConfig


@dataclass
class BaseConfig:
    """
    Base config for the project.
    """
    data_path: str = "${hydra:runtime.cwd}/data/runs/${now:%Y-%m-%dT%H-%M-%S}"
    opensim_process_data: bool = True
    sensor: SensorConfig = field(default_factory=SensorConfig)
    opensim: OpensimConfig = field(default_factory=OpensimConfig)


def register_configs():
    """
    Register configs with the config store.
    """
    cs = ConfigStore.instance()
    cs.store(name="base_config", node=BaseConfig)
    cs.store(group="sensor", name="base_sensor_config", node=SensorConfig)
    cs.store(group="opensim", name="base_opensim_config", node=OpensimConfig)
