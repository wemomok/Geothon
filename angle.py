import numpy as np

from collections.abc import Iterable

from utilities import *

class Angle:
    angle: float
    tolerance: float

    angle_type: GeothonConstants
    tolerance_type: GeothonConstants

    def __init__(self, input_angle=float or int or Iterable, angle_type=GeothonConstants.RAD, tolerance=(0,), tolerance_type=GeothonConstants.DMS) -> None:
        self.type = angle_type
        self.tolerance_type = tolerance_type

        self.angle = convert_to_rads(input_angle, angle_type)
        self.tolerance = convert_to_rads(tolerance, tolerance_type)

    def set(self, input_angle=float or int or Iterable, angle_type=None, tolerance=(0,), tolerance_type=GeothonConstants.DMS) -> None:
        if not angle_type:
            angle_type = self.type

        self.angle = convert_to_rads(input_angle, angle_type)
        self.tolerance = convert_to_rads(tolerance, tolerance_type)

    def get_angle(self):
        return convert_rads_to(self.angle, self.type)

    def get_tolerance(self):
        return convert_rads_to(self.tolerance, self.tolerance_type)

