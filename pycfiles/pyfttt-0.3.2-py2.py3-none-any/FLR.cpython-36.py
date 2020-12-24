# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyFTS/models/multivariate/FLR.py
# Compiled at: 2019-01-03 13:05:45
# Size of source mod 2**32: 526 bytes


class FLR(object):
    """FLR"""

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