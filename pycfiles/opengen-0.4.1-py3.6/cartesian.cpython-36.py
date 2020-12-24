# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/opengen/constraints/cartesian.py
# Compiled at: 2019-10-16 17:13:36
# Size of source mod 2**32: 1529 bytes
from . import constraint
from typing import List

class CartesianProduct(constraint.Constraint):

    def __init__(self, dimension: int, segments: List[int], constraints: List[constraint.Constraint]):
        self._CartesianProduct__dimension = dimension
        self._CartesianProduct__segments = segments
        self._CartesianProduct__constraints = constraints

    @property
    def constraints(self):
        return self._CartesianProduct__constraints

    @property
    def segments(self):
        return self._CartesianProduct__segments

    def segment_dimension(self, i):
        if i == 0:
            return self._CartesianProduct__segments[0] + 1
        else:
            return self._CartesianProduct__segments[i] - self._CartesianProduct__segments[(i - 1)]

    def distance_squared(self, u):
        squared_distance = 0.0
        num_segments = len(self._CartesianProduct__segments)
        idx_previous = -1
        for i in range(num_segments):
            idx_current = self._CartesianProduct__segments[i]
            ui = u[idx_previous + 1:idx_current + 1]
            current_sq_dist = self._CartesianProduct__constraints[i].distance_squared(ui)
            idx_previous = idx_current
            squared_distance += current_sq_dist

        return squared_distance

    def project(self, u):
        raise NotImplementedError()

    def is_convex(self):
        flag = True
        for c in self._CartesianProduct__constraints:
            flag &= c.is_convex()

        return flag

    def is_compact(self):
        for set_i in self._CartesianProduct__constraints:
            if not set_i.is_compact():
                return False

        return True