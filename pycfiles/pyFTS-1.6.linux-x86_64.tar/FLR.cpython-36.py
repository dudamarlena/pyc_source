# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyFTS/models/multivariate/FLR.py
# Compiled at: 2019-01-03 13:05:45
# Size of source mod 2**32: 526 bytes


class FLR(object):
    __doc__ = 'Multivariate Fuzzy Logical Relationship'

    def __init__(self):
        """
        Creates a Fuzzy Logical Relationship
        :param LHS: Left Hand Side fuzzy set
        :param RHS: Right Hand Side fuzzy set
        """
        self.LHS = {}
        self.RHS = None

    def set_lhs(self, var, set):
        self.LHS[var] = set

    def set_rhs(self, set):
        self.RHS = set

    def __str__(self):
        return '{} -> {}'.format([self.LHS[k] for k in self.LHS.keys()], self.RHS)