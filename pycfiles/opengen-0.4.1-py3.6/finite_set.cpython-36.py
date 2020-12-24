# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/opengen/constraints/finite_set.py
# Compiled at: 2019-10-16 17:13:36
# Size of source mod 2**32: 1283 bytes
import casadi.casadi as cs, numpy as np
from .constraint import Constraint
import opengen.functions as fn

class FiniteSet(Constraint):
    __doc__ = 'Finite sets\n    '

    def __init__(self, points=None):
        """Constructor for a finite set
        """
        if points is not None:
            if len(points) > 0:
                first_point_len = len(points[0])
                for point in points[1:]:
                    point_len = len(point)
                    if point_len != first_point_len:
                        raise Exception('Invalid input (points have unequal dimensions)')

        self._FiniteSet__points = None if points is None else [[float(x) for x in p] for p in points]

    @property
    def points(self):
        return self._FiniteSet__points

    def dimension(self):
        p = self.points
        if p is None or len(p) == 0:
            return 0
        else:
            return len(p[0])

    def cardinality(self):
        p = self.points
        if p is None:
            return 0
        else:
            return len(p)

    def distance_squared(self, u):
        raise NotImplementedError()

    def project(self, u):
        raise NotImplementedError()

    def is_convex(self):
        return self.cardinality() == 1 and self.dimension() > 0

    def is_compact(self):
        return True