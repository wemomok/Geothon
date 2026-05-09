import numpy as np

from enum import Enum
from collections.abc import Iterable


class GeothonConstants(Enum):
     RAD = 'rad'
     DEG = 'deg'
     DMS = 'dms'
     SEC = 'sec'


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
        return d, m, s

    raise AttributeError('Invalid angle type provided')


def convert(input_angle, input_type=GeothonConstants, output_type=GeothonConstants):
    rads = convert_to_rads(input_angle, input_type)
    return convert_rads_to(rads, output_type)

