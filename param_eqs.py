import math
from typing import List, Tuple

import numpy as np


class ParamEq:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __setattr__(self, key, value):
        super().__setattr__(key, value)

    def __getattr__(self, key):
        return self.__dict__.get(key, 0)

    def get_points(self) -> List[Tuple[int, int]]:
        raise NotImplementedError


class CircleParamEq(ParamEq):
    def __init__(self, **kwargs):
        super().__init__(radius=10, **kwargs)

    def get_points(self) -> List[Tuple[int, int]]:
        theta = 0
        end = 2 * math.pi
        ans = []
        while theta < end:
            ans.append((
                self.radius * math.cos(theta),
                self.radius * math.sin(theta)
            ))
            theta += 0.001
        return ans


class HypotrochoidParamEq(ParamEq):
    def get_points(self) -> List[Tuple[int, int]]:
        end = self.R * self.k * 2 * np.pi / np.gcd(int(self.R), int(self.k * self.R))
        thetas = np.linspace(0, end, 10000)
        xs = self.R * ((1 - self.k) * np.cos(thetas) + self.l * self.k * np.cos((1 - self.k) / self.k * thetas))
        ys = self.R * ((1 - self.k) * np.sin(thetas) + self.l * self.k * np.sin((1 - self.k) / self.k * thetas))
        return [tuple(p) for p in zip(xs, ys)]
