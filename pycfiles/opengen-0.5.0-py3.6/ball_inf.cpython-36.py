# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/opengen/constraints/ball_inf.py
# Compiled at: 2020-05-07 20:26:31
# Size of source mod 2**32: 3069 bytes
import casadi.casadi as cs, numpy as np
from .constraint import Constraint
import opengen.functions as fn

class BallInf(Constraint):
    __doc__ = 'Norm-ball of norm infinity translated by given vector\n\n    Centered inf-ball around given point\n    '

    def __init__(self, center=None, radius: float=0.0):
        """Constructor for an infinity ball constraint

        Args:
            :param center: center of the ball; if this is equal to Null, the
                ball is centered at the origin

            :param radius: radius of the ball

        :return:
            New instance of Ballinf with given center and radius
        """
        if radius <= 0:
            raise Exception('The radius must be a positive number')
        if center is not None:
            if not isinstance(center, (list, np.ndarray)):
                raise Exception('center is neither None nor a list nor np.ndarray')
        self._BallInf__center = None if center is None else np.array([float(i) for i in center])
        self._BallInf__radius = float(radius)

    @property
    def center(self):
        """Returns the center of the ball"""
        return self._BallInf__center

    @property
    def radius(self):
        """Returns the radius of the ball"""
        return self._BallInf__radius

    def norm_inf_fun_np(a):
        return np.linalg.norm(a, ord=(np.inf))

    def distance_squared(self, u):
        if fn.is_symbolic(u):
            nu = u.size(1)
            v = u if self._BallInf__center is None else u - self._BallInf__center
        else:
            if isinstance(u, list) and all(isinstance(x, (int, float)) for x in u) or isinstance(u, np.ndarray):
                nu = len(u)
                if self._BallInf__center is None:
                    v = u
                else:
                    z = self._BallInf__center.reshape(nu)
                    u = np.array(u).reshape(nu)
                    v = np.subtract(u, z)
            else:
                raise Exception('u is of invalid type')
        squared_distance = fn.norm2(v) ** 2
        for i in range(nu):
            squared_distance += fn.fmin(v[i] ** 2, self.radius ** 2) - 2.0 * fn.fmin(v[i] ** 2, self.radius * fn.fabs(v[i]))

        return squared_distance

    def project(self, u):
        raise NotImplementedError('Method `project` is not implemented')

    def is_convex(self):
        return True

    def is_compact(self):
        return True