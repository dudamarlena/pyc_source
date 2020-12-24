# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/lsga/components/decimal_individual.py
# Compiled at: 2019-02-10 14:34:46
# Size of source mod 2**32: 859 bytes
""" Definition of individual class with decimal encoding.
"""
from .individual import IndividualBase

class DecimalIndividual(IndividualBase):
    __doc__ = ' Individual with decimal encoding.\n\n    :param ranges: value ranges for all entries in solution.\n    :type ranges: tuple list\n\n    :param eps: decrete precisions for binary encoding, default is 0.001.\n    :type eps: float or float list (with the same length with ranges)\n    '

    def __init__(self, ranges, eps=0.001):
        super(self.__class__, self).__init__(ranges, eps)
        self.init()

    def encode(self):
        """ Encode solution to gene sequence
        """
        return self.solution

    def decode(self):
        """ Decode gene sequence to decimal solution
        """
        return self.solution