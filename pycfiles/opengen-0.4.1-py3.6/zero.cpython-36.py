# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/opengen/constraints/zero.py
# Compiled at: 2019-10-16 17:13:36
# Size of source mod 2**32: 599 bytes
import casadi.casadi as cs, numpy as np
from .constraint import Constraint
import opengen.functions as fn

class Zero(Constraint):
    __doc__ = 'A Euclidean ball constraint\n\n    A constraint of the form ||u-u0|| <= r, where u0 is the center\n    of the ball and r is its radius\n\n    '

    def __init__(self):
        """
        Constructor for set Z = {0}

        """
        pass

    def distance_squared(self, u):
        return fn.norm2_squared(u)

    def project(self, u):
        raise NotImplementedError()

    def is_convex(self):
        return True

    def is_compact(self):
        return True