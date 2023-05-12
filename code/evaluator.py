from data_collection.risk import Risk
from data_collection.frames import Frame
from utils.eval import safe_eval
from enum import Enum, unique


@unique
class RiskLevel(Enum):
    """Enum for risk levels."""

    SEVERE = 2
    MODERATE = 1
    NONE = 0


class Evaluator:
    """
    Class for evaluating risk.
    """

    def __init__(self, severe_rules, moderate_rules) -> None:
        self.sev_risk_rules = severe_rules
        self.mod_risk_rules = moderate_rules

    def eval_sev_risk(self, frame: Frame) -> Risk:
        """Evaluate a frame using severe risk rules."""
        return Risk(
            time=frame.time,
            right_abduction=safe_eval(self.sev_risk_rules.right_abduction.replace("@value", str(frame.right_abduction))),
            right_flexion=safe_eval(self.sev_risk_rules.right_flexion.replace("@value", str(frame.right_flexion))),
            right_rotation=safe_eval(self.sev_risk_rules.right_rotation.replace("@value", str(frame.right_rotation))),
            right_elevation=safe_eval(self.sev_risk_rules.right_elevation.replace("@value", str(frame.right_elevation))),
            left_abduction=safe_eval(self.sev_risk_rules.left_abduction.replace("@value", str(frame.left_abduction))),
            left_flexion=safe_eval(self.sev_risk_rules.left_flexion.replace("@value", str(frame.left_flexion))),
            left_rotation=safe_eval(self.sev_risk_rules.left_rotation.replace("@value", str(frame.left_rotation))),
            left_elevation=safe_eval(self.sev_risk_rules.left_elevation.replace("@value", str(frame.left_elevation))),
        )

    def eval_mod_risk(self, frame: Frame) -> Risk:
        """Evaluate moderate risk."""
        return Risk(
            time=frame.time,
            right_abduction=safe_eval(self.mod_risk_rules.right_abduction.replace("@value", str(frame.right_abduction))),
            right_flexion=safe_eval(self.mod_risk_rules.right_flexion.replace("@value", str(frame.right_flexion))),
            right_rotation=safe_eval(self.mod_risk_rules.right_rotation.replace("@value", str(frame.right_rotation))),
            right_elevation=safe_eval(self.mod_risk_rules.right_elevation.replace("@value", str(frame.right_elevation))),
            left_abduction=safe_eval(self.mod_risk_rules.left_abduction.replace("@value", str(frame.left_abduction))),
            left_flexion=safe_eval(self.mod_risk_rules.left_flexion.replace("@value", str(frame.left_flexion))),
            left_rotation=safe_eval(self.mod_risk_rules.left_rotation.replace("@value", str(frame.left_rotation))),
            left_elevation=safe_eval(self.mod_risk_rules.left_elevation.replace("@value", str(frame.left_elevation))),
        )