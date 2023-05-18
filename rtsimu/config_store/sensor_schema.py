from dataclasses import dataclass, field
from typing import List
from omegaconf import MISSING


@dataclass
class Sensor:
    """
    Sensor configuration.
    """
    name: str = MISSING
    frame: str = MISSING
    enabled: bool = True


@dataclass
class AHRSSettings:
    """
    AHRS settings.
    """
    gain: float = 0.5
    acceleration_rejection: float = 10
    magnetic_rejection: float = 20
    rejection_timeout: int = 500


@dataclass
class AHRSConfig:
    """
    AHRS configuration.
    """
    settings: AHRSSettings = field(default_factory=AHRSSettings)


@dataclass
class SensorConfig:
    """
    Sensor configuration.
    """
    data_sensors: str = MISSING
    sensors: List[Sensor] = field(default_factory=list)
    AHRS: AHRSConfig = field(default_factory=AHRSConfig)
    

    