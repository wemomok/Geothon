import numpy as np

from point import Point


def Heaviside_step_function(x=float or int):
    if x >= 0:
        return 1
    else:
        return 0


def sgn_0(x=float or int):
    return 2 * Heaviside_step_function(x) - 1


def IGP(point_1=Point, point_2=Point):
    delta_x = point_2[0] - point_1[0]
    delta_y = point_2[1] - point_1[1]
    distance = np.sqrt(delta_x ** 2 + delta_y ** 2)
    rumb = np.arccos(delta_x / distance)
    return (1 - sgn_0(delta_y) / 2 - sgn_0(delta_x) * sgn_0(delta_y) / 2) * \
        np.pi + sgn_0(delta_x) * sgn_0(delta_y) * rumb, distance


def find_angle_to_point(point_1=Point, point_2=Point, point_3=Point):
    alpha_2_1 = IGP(point_2, point_1)
    alpha_2_3 = IGP(point_2, point_3)
    return alpha_2_1 - alpha_2_3

