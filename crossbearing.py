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
    def calculate_triangle(a=Point, b=Point, s1=float, s2=float):
        alphaba, sab = IGP(b, a)
        phi = np.arccos((s1 ** 2 + sab ** 2 - s2 ** 2) / (2 * sab * s1))
        alphaap = alphaba - phi + np.pi
        return Point(a[0] + s1 * np.cos(alphaap), a[1] + s1 * np.sin(alphaap))


    def __init__(self, points=Iterable[Point], angles=Iterable[Angle], distances=Iterable[float]):
        self.points = [*points]
        self.angles = [*angles]
        self.distances = [*distances]

        if not (len(points) == len(distances) and len(angles) == len(points) - 1):
            raise BaseException('Incorrect data configuration: amount of points, angles and distances doesn\'t match')

    def solve(self):
        p = []
        for i in range(1, len(self.points)):
            pi = self.calculate_triangle(self.points[i-1], self.points[i], self.distances[i-1], self.distances[i])
            p.append(pi)
        sumx = 0
        sumy = 0
        for i in p:
            sumx += i[0]
            sumy += i[1]
        return Point(sumx/len(p), sumy/len(p))


a = Point(100, 120)
b = Point(83.949, 88.791)
c = Point(65.362, 100.884)
points = [a, b, c]
a1 = Angle((26, 56, 56), GeothonConstants.DMS)
a2 = Angle((31, 23, 33), GeothonConstants.DMS)
angles = [a1, a2]
s = [18.572, 42.570, 36.398]

p = InverseLinearAngularCrossbearing(points, angles, s)
P = p.solve()
print(P.coords)
