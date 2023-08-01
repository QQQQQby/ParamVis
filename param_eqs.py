from functools import lru_cache
from typing import List, Tuple

import numpy as np


class ParamEq:
    def eq(self, *params) -> List[np.ndarray]:
        raise NotImplementedError

    def param_values(self) -> List[np.ndarray]:
        raise NotImplementedError

    def get_points(self) -> List[Tuple]:
        param_values = self.param_values()
        points = None
        if len(param_values) == 1:
            points = self.eq(param_values[0])
        elif len(param_values) == 2:
            raise NotImplementedError
        return [tuple(p) for p in zip(*points)]


class CircleParamEq(ParamEq):
    def __init__(self, radius):
        self.radius = radius

    def eq(self, thetas) -> List[np.ndarray]:
        return [
            self.radius * np.cos(thetas),
            self.radius * np.sin(thetas)
        ]

    def param_values(self) -> List[np.ndarray]:
        return [np.linspace(0, 2 * np.pi, 10000)]


class HypotrochoidParamEq(ParamEq):
    def __init__(self, R, k, l):
        self.R = R
        self.k = k
        self.l = l

    def eq(self, thetas) -> List[np.ndarray]:
        return [
            self.R * ((1 - self.k) * np.cos(thetas) + self.l * self.k * np.cos((1 - self.k) / self.k * thetas)),
            self.R * ((1 - self.k) * np.sin(thetas) + self.l * self.k * np.sin((1 - self.k) / self.k * thetas))
        ]

    def param_values(self) -> List[np.ndarray]:
        return [np.linspace(0, self.R * self.k * 2 * np.pi / np.gcd(int(self.R), int(self.k * self.R)), 10000)]


class LineParamEq(ParamEq):
    def __init__(self, x0, y0, a):
        self.x0 = x0
        self.y0 = y0
        self.a = a

    def eq(self, ts) -> List[np.ndarray]:
        return [
            self.x0 + np.cos(self.a) * ts,
            self.y0 + np.sin(self.a) * ts
        ]

    def param_values(self) -> List[np.ndarray]:
        return [np.array([-10000, 10000])]
