from constants import GeothonConstants
from point import Point


class Vector:
    __p1: Point
    __p2: Point

    __delta: Point

    def __init__(self, p1=Point, p2=None):
        if not p2:
            p2 = p1
            if p1.point_type == GeothonConstants.XY:
                p1 = Point(0, 0)
            else:
                p1 = Point(0, 0, 0)

        self.__p1 = p1
        self.__p2 = p2
        self.__delta = p2 - p1

    def length(self):
        if self.__delta.point_type == GeothonConstants.XY:
            return (self.__delta[0] ** 2 + self.__delta[1] ** 2) ** 0.5
        elif self.__delta.point_type == GeothonConstants.XYZ:
            return (self.__delta[0] ** 2 + self.__delta[1] ** 2 + self.__delta[2] ** 2) ** 0.5

    def get_delta(self):
        return self.__delta

    def __add__(self, other):
        if not isinstance(other, Vector):
            raise BaseException(f'No overload for adding Vector and {type(other)}')
        return Vector(self.__p1, self.__p2 + other.get_delta())

    def __sub__(self, other):
        if not isinstance(other, Vector):
            raise BaseException(f'No overload for subtracting Vector and {type(other)}')
        return Vector(self.__p1, self.__p2 - other.get_delta())

    def __iadd__(self, other):
        if not isinstance(other, Vector):
            raise BaseException(f'No overload for adding Vector and {type(other)}')
        self.__p2 += other.get_delta()
        return self

    def __isub__(self, other):
        if not isinstance(other, Vector):
            raise BaseException(f'No overload for subtracting Vector and {type(other)}')
        self.__p2 -= other.get_delta()
        return self

