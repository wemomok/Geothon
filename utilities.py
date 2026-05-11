import numpy as np

from enum import Enum
from collections.abc import Iterable


class GeothonConstants(Enum):
     RAD = 'rad'
     DEG = 'deg'
     DMS = 'dms'
     SEC = 'sec'
     XY = 'xy'
     XYZ = 'xyz'


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

#NEW
def Heaviside_step_function(x=float or int):
    if x >= 0:
        return 1
    else:
        return 0


def sgn_0(x=float or int):
    return 2 * Heaviside_step_function(x) - 1


def IGP_alpha(point_1=Iterable, point_2=Iterable):
    delta_x = point_2[0] - point_1[0]
    delta_y = point_2[1] - point_1[1]
    distance = np.sqrt(delta_x ** 2 + delta_y ** 2)
    rumb = np.arccos(delta_x / distance)
    return (1 - sgn_0(delta_y) / 2 - sgn_0(delta_x) * sgn_0(delta_y) / 2) * np.pi + sgn_0(delta_x) * sgn_0(delta_y) * rumb


def find_angle_to_point(point_1=Iterable, point_2=Iterable, point_3=Iterable):
    alpha_2_1 = IGP_alpha(point_2, point_1)
    alpha_2_3 = IGP_alpha(point_2, point_3)
    return alpha_2_1 - alpha_2_3

