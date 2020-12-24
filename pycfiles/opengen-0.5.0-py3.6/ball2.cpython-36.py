# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/opengen/constraints/ball2.py
# Compiled at: 2020-05-07 20:26:31
# Size of source mod 2**32: 3198 bytes
import casadi.casadi as cs, numpy as np
from .constraint import Constraint
import opengen.functions as fn

class Ball2(Constraint):
    __doc__ = 'A Euclidean ball constraint\n\n    A constraint of the form ||u-u0|| <= r, where u0 is the center\n    of the ball and r is its radius\n\n    '

    def __init__(self, center=None, radius: float=1.0):
        """Constructor for a Euclidean ball constraint

        Args:
            center: center of the ball; if this is equal to Null, the
            ball is centered at the origin

            radius: radius of the ball

        Returns:
            New instance of Ball2 with given center and radius
        """
        if radius <= 0:
            raise Exception('The radius must be a positive number')
        if center is not None:
            if not isinstance(center, (list, np.ndarray)):
                raise Exception('center is neither None nor a list nor np.ndarray')
        self._Ball2__center = None if center is None else np.array([float(i) for i in center])
        self._Ball2__radius = float(radius)

    @property
    def center(self):
        """Returns the center of the ball"""
        return self._Ball2__center

    @property
    def radius(self):
        """Returns the radius of the ball"""
        return self._Ball2__radius

    def distance_squared(self, u):
        """Computes the squared distance between a given point `u` and this ball

            :param u: given point; can be a list of float, a numpy
                n-dim array (`ndarray`) or a CasADi SX/MX symbol

            :return: distance from set as a float or a CasADi symbol
        """
        if fn.is_symbolic(u):
            v = u if self._Ball2__center is None else u - self._Ball2__center
        else:
            if isinstance(u, list) and all(isinstance(x, (int, float)) for x in u) or isinstance(u, np.ndarray):
                if self._Ball2__center is None:
                    v = u
                else:
                    z = self._Ball2__center.reshape(len(u))
                    u = np.array(u).reshape(len(u))
                    v = np.subtract(u, z)
            else:
                raise Exception('u is of invalid type')
        t = fn.norm2(v) - self.radius
        return fn.fmax(0.0, fn.sign(t) * t ** 2)

    def project(self, u):
        raise NotImplementedError()

    def is_convex(self):
        return True

    def is_compact(self):
        return True