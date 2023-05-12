from dataclasses import dataclass, field
from hydra.core.config_store import ConfigStore
from omegaconf import MISSING


@dataclass
class Coordinates:
    """
    Coordinates for the opensim model.
    """
    right_abduction: str = "shoulder_abduction_r"
    right_flexion: str = "shoulder_flexion_r"
    right_rotation: str = "shoulder_rotation_r"
    right_elevation: str = "clav_elev_r"
    left_abduction: str = "shoulder_abduction_l"
    left_flexion: str = "shoulder_flexion_l"
    left_rotation: str = "shoulder_rotation_l"
    left_elevation: str = "clav_elev_l"


@dataclass
class Sensor2OpensimRotation:
    """
    Rotation of reference from the sensor to the opensim model.
    """
    x: str = "0"
    y: str = "0"
    z: str = "0"


@dataclass
class RiskRules:
    """
    Rules for the risk.
    """
    right_abduction: str = MISSING
    right_flexion: str = MISSING
    right_rotation: str = MISSING
    right_elevation: str = MISSING
    left_abduction: str = MISSING
    left_flexion: str = MISSING
    left_rotation: str = MISSING
    left_elevation: str = MISSING


@dataclass
class SevereRisk:
    """
    Severe risk.
    """
    duration: int = 4
    rules: RiskRules = field(default_factory=RiskRules)


@dataclass
class ModerateRisk:
    """
    Moderate risk.
    """
    duration: int = 8
    rules: RiskRules = field(default_factory=RiskRules)


@dataclass
class Risk:
    """
    Risk.
    """
    severe: SevereRisk = field(default_factory=SevereRisk)
    moderate: ModerateRisk = field(default_factory=ModerateRisk)


@dataclass
class OpensimConfig:
    """
    Config for opensim.
    """
    model_path: str = MISSING
    visualize: bool = False
    frames_per_second: int = 100
    coordinates: Coordinates = field(default_factory=Coordinates)
    sensor_to_opensim_rotation: Sensor2OpensimRotation = field(default_factory=Sensor2OpensimRotation)
    risk: Risk = field(default_factory=Risk)
