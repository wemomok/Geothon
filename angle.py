import numpy as np

from collections.abc import Iterable

from constants import GeothonConstants


def convert_to_rads(input_angle=float or int or Iterable, angle_type=GeothonConstants):
    if not isinstance(input_angle, Iterable) and angle_type == GeothonConstants.DMS or \
            isinstance(input_angle, Iterable) and angle_type != GeothonConstants.DMS:
        raise AttributeError('Angle type provided doesn\'t match input angle')

    if angle_type == GeothonConstants.RAD:
        angle = input_angle
    elif angle_type == GeothonConstants.DEG:
        angle = np.deg2rad(input_angle)
    elif angle_type == GeothonConstants.SEC:
        angle = np.deg2rad(input_angle / 3600)
    elif angle_type == GeothonConstants.DMS:
        dms = [*input_angle]

        if len(dms) > 3:
            raise AttributeError('Too many values provided')

        while len(dms) < 3:
            dms.append(0)

        deg, mins, sec = dms
        angle = np.deg2rad(deg + mins / 60 + sec / 3600)

    else:
        raise AttributeError('Invalid angle type provided')

    return angle


def convert_rads_to(input_angle=float, angle_type=GeothonConstants):
    if angle_type == GeothonConstants.RAD:
        return input_angle
    elif angle_type == GeothonConstants.DEG:
        return np.rad2deg(input_angle)
    elif angle_type == GeothonConstants.SEC:
        return np.rad2deg(input_angle) * 3600
    elif angle_type == GeothonConstants.DMS:
        deg = np.rad2deg(input_angle)
        d = int(deg)
        m = int((deg - d) * 60)
        s = (deg - d - m / 60) * 3600
        return d, m, round(s, 10)

    raise AttributeError('Invalid angle type provided')


def convert(input_angle, input_type=GeothonConstants, output_type=GeothonConstants):
    rads = convert_to_rads(input_angle, input_type)
    return convert_rads_to(rads, output_type)


class Angle:
    __angle: float
    __tolerance: float

    angle_type: GeothonConstants
    tolerance_type: GeothonConstants

    def __init__(self, input_angle=float or int or Iterable,
                 angle_type=GeothonConstants.RAD, tolerance=(0,), tolerance_type=GeothonConstants.DMS):
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

    def __iadd__(self, other):
        if not isinstance(other, Angle):
            raise BaseException(
                f"No overload for adding Angle and {type(other)}")
        self.__angle += other.__angle
        return self

    def __isub__(self, other):
        if not isinstance(other, Angle):
            raise BaseException(
                f"No overload for subtracting Angle and {type(other)}")
        self.__angle -= other.__angle
        return self

    def __add__(self, other):
        if not isinstance(other, Angle):
            raise BaseException(
                f"No overload for adding Angle and {type(other)}")
        return Angle(self.__angle + other.__angle)

    def __sub__(self, other):
        if not isinstance(other, Angle):
            raise BaseException(
                f"No overload for subtracting Angle and {type(other)}")
        return Angle(self.__angle - other.__angle)

