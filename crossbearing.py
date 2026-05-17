import numpy as np

from collections.abc import Iterable

from angle import Angle
from point import Point
from utilities import IGP
from constants import GeothonConstants


def inverseLinearAngularCrossbearing(points=Iterable[Point], angles=Iterable[Angle],
                                     distances=Iterable[float]):
    def calculate_triangle(a=Point, b=Point, s1=float, s2=float):
        alphaba, sab = IGP(b, a)
        phi = np.arccos((s1 ** 2 + sab ** 2 - s2 ** 2) / (2 * sab * s1))
        alphaap = alphaba - phi + np.pi
        return Point(a[0] + s1 * np.cos(alphaap), a[1] + s1 * np.sin(alphaap))

    points = [*points]
    angles = [*angles]
    distances = [*distances]

    if not (len(points) == len(distances) and len(angles) == len(points) - 1):
        raise BaseException(
            'Incorrect data configuration: amount of points, angles and\
                    distances doesn\'t match')

    result_points = []
    for i in range(1, len(points)):
        result_points.append(calculate_triangle(
            points[i-1], points[i], distances[i-1], distances[i]))

    result_points.append(calculate_triangle(
        points[-2], points[-1], distances[-2], distances[-1]))

    sumx = sum(point[0] for point in result_points)
    sumy = sum(point[1] for point in result_points)

    return Point(sumx/len(result_points), sumy/len(result_points))

