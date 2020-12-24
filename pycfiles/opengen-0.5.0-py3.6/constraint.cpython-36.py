# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/opengen/constraints/constraint.py
# Compiled at: 2020-04-17 11:54:47
# Size of source mod 2**32: 331 bytes


class Constraint:

    def distance_squared(self, u):
        raise NotImplementedError('Method `distance_squared` is not implemented')

    def project(self, u):
        raise NotImplementedError('Method `project` is not implemented')

    def is_convex(self):
        return False

    def is_compact(self):
        return False