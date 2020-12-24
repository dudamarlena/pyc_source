# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/opengen/constraints/no_constraints.py
# Compiled at: 2019-10-16 17:13:36
# Size of source mod 2**32: 301 bytes
from .constraint import Constraint

class NoConstraints(Constraint):

    def __init__(self):
        pass

    def distance_squared(self, u):
        return 0.0

    def project(self, u):
        return u

    def is_convex(self):
        return True

    def is_compact(self):
        return False