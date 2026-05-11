import numpy as np

from utilities import *


class Point:
    coords: np.array

    point_type: GeothonConstants

    def __init__(self, x=float, y=float, z=None):
        self.point_type = GeothonConstants.XY if not z else GeothonConstants.XYZ

        self.coords = np.array([x, y]) if not z else np.array([x, y, z])

    def __iadd__(self, other):
        if not isinstance(other, Point):
            raise BaseException(f'No overload for adding Point and {type(other)}')

        if self.point_type == GeothonConstants.XY and other.point_type == GeothonConstants.XYZ:
            self.coords += other.coords[:2]
        elif self.point_type == GeothonConstants.XYZ and other.point_type == GeothonConstants.XY:
            self.coords += np.array([*other.coords, 0])
        else:
            self.coords += other.coords

        return self

    def __isub__(self, other):
        if not isinstance(other, Point):
            raise BaseException(f'No overload for subtracting Point and {type(other)}')

        if self.point_type == GeothonConstants.XY and other.point_type == GeothonConstants.XYZ:
            self.coords -= other.coords[:2]
        elif self.point_type == GeothonConstants.XYZ and other.point_type == GeothonConstants.XY:
            self.coords -= np.array([*other.coords, 0])
        else:
            self.coords -= other.coords

        return self

    def __add__(self, other):
        if not isinstance(other, Point):
            raise BaseException(f'No overload for adding Point and {type(other)}')

        if self.point_type == GeothonConstants.XY and other.point_type == GeothonConstants.XYZ:
            return Point(*(self.coords + other.coords[:2]))
        elif self.point_type == GeothonConstants.XYZ and other.point_type == GeothonConstants.XY:
            return Point(*(self.coords + np.array([*other.coords, 0])))
        else:
            return Point(*(self.coords + other.coords))

    def __sub__(self, other):
        if not isinstance(other, Point):
            raise BaseException(f'No overload for adding Point and {type(other)}')

        if self.point_type == GeothonConstants.XY and other.point_type == GeothonConstants.XYZ:
            return Point(*(self.coords - other.coords[:2]))
        elif self.point_type == GeothonConstants.XYZ and other.point_type == GeothonConstants.XY:
            return Point(*(self.coords - np.array([*other.coords, 0])))

        else:
            return Point(*(self.coords - other.coords))

    def __setitem__(self, index, value):
        self.coords[index] = value

    def __getitem__(self, index):
        return self.coords[index]

