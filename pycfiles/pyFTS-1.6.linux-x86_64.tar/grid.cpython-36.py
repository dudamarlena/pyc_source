# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyFTS/partitioners/Grid.py
# Compiled at: 2018-08-30 00:51:51
# Size of source mod 2**32: 1416 bytes
"""Even Length Grid Partitioner"""
import numpy as np, math, random as rnd, functools, operator
from pyFTS.common import FuzzySet, Membership
from pyFTS.partitioners import partitioner

class GridPartitioner(partitioner.Partitioner):
    __doc__ = 'Even Length Grid Partitioner'

    def __init__(self, **kwargs):
        (super(GridPartitioner, self).__init__)(name='Grid', **kwargs)

    def build(self, data):
        sets = {}
        kwargs = {'type':self.type, 
         'variable':self.variable}
        dlen = self.max - self.min
        partlen = dlen / self.partitions
        count = 0
        for c in np.arange(self.min, self.max, partlen):
            _name = self.get_name(count)
            if self.membership_function == Membership.trimf:
                sets[_name] = (FuzzySet.FuzzySet)(_name, (Membership.trimf), [c - partlen, c, c + partlen], c, **kwargs)
            else:
                if self.membership_function == Membership.gaussmf:
                    sets[_name] = (FuzzySet.FuzzySet)(_name, (Membership.gaussmf), [c, partlen / 3], c, **kwargs)
                else:
                    if self.membership_function == Membership.trapmf:
                        q = partlen / 2
                        sets[_name] = (FuzzySet.FuzzySet)(_name, (Membership.trapmf), [c - partlen, c - q, c + q, c + partlen], c, **kwargs)
            count += 1

        self.min = self.min - partlen
        return sets