from typing import List, Tuple

import numpy as np


class ParamEq:
    def eq(self, *params) -> List[np.ndarray]:
        raise NotImplementedError

    def param_values(self) -> List[np.ndarray]:
        raise NotImplementedError

    def get_points(self) -> List[Tuple]:
        param_values = self.param_values()
        points = self.eq(*param_values)
        return [tuple(p) for p in zip(*points)]


class LineParamEq(ParamEq):
    def __init__(self, x0, y0, k):
        self.x0 = x0
        self.y0 = y0
        self.k = k

    def eq(self, ts) -> List[np.ndarray]:
        return [
            self.x0 + np.cos(self.k * np.pi) * ts,
            self.y0 + np.sin(self.k * np.pi) * ts
        ]

    def param_values(self) -> List[np.ndarray]:
        return [np.array([-10000, 10000])]


class CircleParamEq(ParamEq):
    def __init__(self, r, x0, y0):
        self.r = r
        self.x0 = x0
        self.y0 = y0

    def eq(self, thetas) -> List[np.ndarray]:
        return [
            self.x0 + self.r * np.cos(thetas),
            self.y0 + self.r * np.sin(thetas)
        ]

    def param_values(self) -> List[np.ndarray]:
        return [np.linspace(0, 2 * np.pi, 10000)]


class HyperbolaParamEq(ParamEq):
    def __init__(self, a, b, x0, y0):
        self.a = a
        self.b = b
        self.x0 = x0
        self.y0 = y0

    def eq(self, thetas) -> List[np.ndarray]:
        return [
            self.x0 + self.a / np.cos(thetas),
            self.y0 + self.b * np.tan(thetas)
        ]

    def param_values(self) -> List[np.ndarray]:
        return [np.linspace(-np.pi / 2 + 1e-5, np.pi / 2 - 1e-5, 10000)]


class LemniscateParamEq(ParamEq):
    def __init__(self, a):
        self.a = a

    def eq(self, thetas) -> List[np.ndarray]:
        return [
            100 * self.a * np.cos(thetas) * np.sqrt(np.cos(2 * thetas)),
            100 * self.a * np.sin(thetas) * np.sqrt(np.cos(2 * thetas))
        ]

    def param_values(self) -> List[np.ndarray]:
        return [np.append(np.linspace(-np.pi / 4 + 1e-5, np.pi / 4 - 1e-5, 5000),
                          np.linspace(np.pi * 3 / 4 + 1e-5, np.pi * 5 / 4 - 1e-5, 5000))]


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


class RoseCurveParamEq(ParamEq):
    def __init__(self, n, a):
        self.n = n
        self.a = a

    def eq(self, thetas) -> List[np.ndarray]:
        return [
            50 * self.a * np.sin(self.n * thetas) * np.cos(thetas),
            50 * self.a * np.sin(self.n * thetas) * np.sin(thetas)
        ]

    def param_values(self) -> List[np.ndarray]:
        return [np.linspace(0, 2 * np.pi, 10000)]


class LissajousParamEq(ParamEq):
    def __init__(self, n, phi, a, b):
        self.n = n
        self.phi = phi
        self.a = a
        self.b = b

    def eq(self, ts) -> List[np.ndarray]:
        return [
            self.a * np.sin(ts),
            self.b * np.sin(self.n * ts + self.phi)
        ]

    def param_values(self) -> List[np.ndarray]:
        return [np.linspace(0, 2 * np.pi * np.lcm(int(self.n * 100), 100) / int(self.n * 100), 10000)]


class Extra1ParamEq(ParamEq):
    def __init__(self, a):
        self.a = a

    def eq(self, ts) -> List[np.ndarray]:
        return [
            100 * np.sin(ts + np.cos(self.a * ts)),
            100 * np.cos(ts + np.sin(self.a * ts))
        ]

    def param_values(self) -> List[np.ndarray]:
        return [np.linspace(-np.pi, np.pi, 10000)]
