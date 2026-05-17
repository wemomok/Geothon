import numpy as np


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
        if isinstance(other, ScalarMeasurement):
            self.value += other.value
            self.tolerance = np.sqrt(
                self.tolerance ** 2 + other.tolerance ** 2)
        else:
            self.value += other
        return self

    def __isub__(self, other):
        if isinstance(other, ScalarMeasurement):
            self.value -= other.value
            self.tolerance = np.sqrt(
                self.tolerance ** 2 + other.tolerance ** 2)
        else:
            self.value -= other
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

    def __pow__(self, n):
        if not isinstance(n, int):
            raise BaseException(f'Raising ScalarMeasurement to {
                                type(n)} is not supported')
        result = self
        for _ in range(n):
            result *= self

        return result

    def __ipow__(self, n):
        if not isinstance(n, int):
            raise BaseException(f'Raising ScalarMeasurement to {
                                type(n)} is not supported')
        initial = self
        for _ in range(n):
            self *= initial

        return self
