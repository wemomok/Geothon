import numpy as np

from copy import copy
from collections.abc import Iterable

from constants import GeothonConstants
from scalar_measurement import ScalarMeasurement


def convert_to_rads(input_angle=float or int or Iterable,
                    angle_type=GeothonConstants):
    if not isinstance(input_angle, Iterable) and angle_type == GeothonConstants.DMS or \
            isinstance(input_angle, Iterable) and angle_type != GeothonConstants.DMS:
        raise BaseException('Angle type provided doesn\'t match input angle')

    if angle_type == GeothonConstants.RAD:
        angle = input_angle
    elif angle_type == GeothonConstants.DEG:
        angle = np.deg2rad(input_angle)
    elif angle_type == GeothonConstants.SEC:
        angle = np.deg2rad(input_angle / 3600)
    elif angle_type == GeothonConstants.DMS:
        dms = [*input_angle]

        if len(dms) > 3:
            raise BaseException('Too many values provided')

        while len(dms) < 3:
            dms.append(0)

        deg, mins, sec = dms
        angle = np.deg2rad((deg + mins / 60 + sec / 3600) *
                           (-1 if any(val < 0 for val in dms) else 1))

    else:
        raise BaseException('Invalid angle type provided')

    return angle % (2 * np.pi)


def convert_rads_to(input_angle=float, angle_type=GeothonConstants):
    input_angle %= (2 * np.pi)
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

    raise BaseException('Invalid angle type provided')


def convert(input_angle, input_type=GeothonConstants,
            output_type=GeothonConstants):
    rads = convert_to_rads(input_angle, input_type)
    return convert_rads_to(rads, output_type)


class Angle:
    __angle: ScalarMeasurement

    angle_type: GeothonConstants
    tolerance_type: GeothonConstants

    def __init__(self, input_angle=float or int or Iterable,
                 angle_type=GeothonConstants.RAD, tolerance=(0,),
                 tolerance_type=GeothonConstants.DMS):
        self.angle_type = angle_type
        self.tolerance_type = tolerance_type

        self.__angle = ScalarMeasurement(convert_to_rads(
            input_angle, angle_type), convert_to_rads(tolerance, tolerance_type))

    def set(self, input_angle=float or int or Iterable, angle_type=None, tolerance=(0,), tolerance_type=None):
        if not angle_type:
            angle_type = self.angle_type
        if not tolerance_type:
            tolerance_type = self.tolerance_type

        self.__angle = ScalarMeasurement(convert_to_rads(
            input_angle, angle_type), convert_to_rads(tolerance, tolerance_type))

    def get_angle(self):
        return convert_rads_to(self.__angle.value, self.angle_type)

    def get_tolerance(self):
        return convert_rads_to(self.__angle.tolerance, self.tolerance_type)

    def __iadd__(self, other):
        if not isinstance(other, Angle):
            raise BaseException(
                f"No overload for adding Angle and {type(other)}")
        self.__angle += other.__angle
        self.__angle.value %= (2 * np.pi)
        return self

    def __isub__(self, other):
        if not isinstance(other, Angle):
            raise BaseException(
                f"No overload for subtracting Angle and {type(other)}")
        self.__angle -= other.__angle
        self.__angle.value %= (2 * np.pi)
        return self

    def __add__(self, other):
        if not isinstance(other, Angle):
            raise BaseException(
                f"No overload for adding Angle and {type(other)}")
        result = self.__angle + other.__angle
        result.value %= (2 * np.pi)
        result_angle = Angle(
            result.value, tolerance=result.tolerance, tolerance_type=GeothonConstants.RAD)
        result_angle.angle_type = self.angle_type
        result_angle.tolerance_type = self.tolerance_type
        return result_angle

    def __sub__(self, other):
        if not isinstance(other, Angle):
            raise BaseException(
                f"No overload for subtracting Angle and {type(other)}")
        result = self.__angle - other.__angle
        result.value %= (2 * np.pi)
        result_angle = Angle(
            result.value, tolerance=result.tolerance, tolerance_type=GeothonConstants.RAD)
        result_angle.angle_type = self.angle_type
        result_angle.tolerance_type = self.tolerance_type
        return result_angle

    def __mul__(self, other):
        result = copy(self)
        result.__angle *= other
        result.__angle.value %= (2 * np.pi)
        return result

    def __truediv__(self, other):
        result = copy(self)
        result.__angle /= other
        result.__angle.value %= (2 * np.pi)
        return result

    def __imul__(self, other):
        self = self * other
        return self

    def __itruediv__(self, other):
        self = self / other
        return self

    def __str__(self):
        return f'{str(self.get_angle())}±{str(self.get_tolerance())}'

    def __repr__(self):
        return f'Angle: {str(self.get_angle())}±{str(self.get_tolerance())}'
