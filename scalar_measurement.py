import numpy as np

from copy import copy


class ScalarMeasurement:
    def __init__(self, value, tolerance=0):
        self.value = value
        self.tolerance = tolerance

    def __add__(self, other):
        if isinstance(other, ScalarMeasurement):
            return ScalarMeasurement(self.value + other.value,
                                     np.sqrt(self.tolerance ** 2 + other.tolerance ** 2))
        return ScalarMeasurement(self.value + other, self.tolerance)

    def __sub__(self, other):
        if isinstance(other, ScalarMeasurement):
            return ScalarMeasurement(self.value - other.value,
                                     np.sqrt(self.tolerance ** 2 + other.tolerance ** 2))
        return ScalarMeasurement(self.value - other, self.tolerance)

    def __iadd__(self, other):
        self = self + other
        return self

    def __isub__(self, other):
        self = self - other
        return self

    def __mul__(self, other):
        if isinstance(other, ScalarMeasurement):
            return ScalarMeasurement(self.value * other.value, np.sqrt(
                (other.value * self.tolerance) ** 2 + (self.value * other.tolerance) ** 2))
        return ScalarMeasurement(self.value * other, self.tolerance * other)

    def __truediv__(self, other):
        if isinstance(other, ScalarMeasurement):
            return ScalarMeasurement(self.value / other.value, np.sqrt(
                (self.tolerance / other.value) ** 2 + (other.tolerance / self.value) ** 2))
        return ScalarMeasurement(self.value / other, self.tolerance / other)

    def __imul__(self, other):
        self = self * other
        return self

    def __itruediv__(self, other):
        self = self / other
        return self

    def __pow__(self, n):
        if not isinstance(n, int):
            raise BaseException(f'Raising ScalarMeasurement to {
                                type(n)} is not supported')
        result = copy(self)
        for _ in range(n):
            result *= self

        return result

    def __ipow__(self, n):
        if not isinstance(n, int):
            raise BaseException(f'Raising ScalarMeasurement to {
                                type(n)} is not supported')
        initial = copy(self)
        for _ in range(n):
            self *= initial

        return self

    def __eq__(self, other):
        if isinstance(other, ScalarMeasurement):
            return self.value == other.value
        return self.value == other

    def __ne__(self, other):
        if isinstance(other, ScalarMeasurement):
            return self.value != other.value
        return self.value != other

    def __lt__(self, other):
        if isinstance(other, ScalarMeasurement):
            return self.value < other.value
        return self.value < other

    def __le__(self, other):
        if isinstance(other, ScalarMeasurement):
            return self.value <= other.value
        return self.value <= other

    def __gt__(self, other):
        if isinstance(other, ScalarMeasurement):
            return self.value > other.value
        return self.value > other

    def __ge__(self, other):
        if isinstance(other, ScalarMeasurement):
            return self.value >= other.value
        return self.value >= other

    def __str__(self):
        return f'{self.value}±{self.tolerance}'

    def __repr__(self):
        return f'ScalarMeasurement: {self.value}±{self.tolerance}'
