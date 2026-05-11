import numpy as np

from collections.abc import Iterable

from utilities import *

class Angle:
    __angle: float
    __tolerance: float

    angle_type: GeothonConstants
    tolerance_type: GeothonConstants

    def __init__(self, input_angle=float or int or Iterable, angle_type=GeothonConstants.RAD, tolerance=(0,), tolerance_type=GeothonConstants.DMS):
        self.angle_type = angle_type
        self.tolerance_type = tolerance_type

        self.__angle = convert_to_rads(input_angle, angle_type)
        self.__tolerance = convert_to_rads(tolerance, tolerance_type)

    def set(self, input_angle=float or int or Iterable, angle_type=None, tolerance=(0,), tolerance_type=None):
        if not angle_type:
            angle_type = self.angle_type
        if not tolerance_type:
            tolerance_type = self.tolerance_type

        self.__angle = convert_to_rads(input_angle, angle_type)
        self.__tolerance = convert_to_rads(tolerance, tolerance_type)

    def get_angle(self):
        return convert_rads_to(self.__angle, self.angle_type)

    def get_tolerance(self):
        return convert_rads_to(self.__tolerance, self.tolerance_type)

    def solve_IGP(self, point_1=Iterable, point_2=Iterable):
        self.__angle = IGP_alpha(point_1, point_2)

    def find_angle(self, point_1=Iterable, point_2=Iterable, point_3=Iterable):
        self.__angle = find_angle_to_point(point_1, point_2, point_3)

    def broadcast_to_next(self, directional_angle):
        new = directional_angle - self.angle + np.pi
        self.__angle = new

