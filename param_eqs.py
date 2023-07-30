import math
from typing import List, Tuple


class ParamEq:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __setattr__(self, key, value):
        super().__setattr__(key, value)
        print(key, value)

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


class HypocycloidParamEq(ParamEq):
    def get_points(self) -> List[Tuple[int, int]]:
        theta = 0
        end = 2 * math.pi
        ans = []
        while theta < end:
            ans.append((
                (self.a - self.b) * math.cos(theta) + self.b * math.cos(theta * (self.a - self.b) / self.b),
                (self.a - self.b) * math.sin(theta) - self.b * math.sin(theta * (self.a - self.b) / self.b)
            ))
            theta += 0.001
        return ans
