import numpy as np

from collections.abc import Iterable

from angle import Angle
from point import Point
from vector import Vector
from utilities import IGP
from constants import GeothonConstants


class InverseLinearAngularCrossbearing:
    points: Iterable[Point]
    angles: Iterable[Angle]
    distances: Iterable[float]

    @staticmethod
    def calculate_triangle(a=Point, b=Point, s1=float, s2=float, beta=Angle):
        alphaba, sab = IGP(b, a)
        phi = np.arccos((s1 ** 2 + sab ** 2 - s2 ** 2) / (2 * sab * s1))
        alphaap = alphaba - phi + np.pi
        return Point(a[0] + s1 * np.cos(alphaap), a[1] + s1 * np.sin(alphaap))

    def __init__(self, points=Iterable[Point], angles=Iterable[Angle], distances=Iterable[float]):
        points = [*points]
        angles = [*angles]
        distances = [*distances]

        if not (len(points) == len(distances) and len(angles) == len(points) - 1):
            raise BaseException('Incorrect data configuration: amount of points, angles and distances doesn\'t match')

        

