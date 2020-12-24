# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyFTS/models/chen.py
# Compiled at: 2019-04-09 15:22:00
# Size of source mod 2**32: 2678 bytes
"""
First Order Conventional Fuzzy Time Series by Chen (1996)

S.-M. Chen, “Forecasting enrollments based on fuzzy time series,” Fuzzy Sets Syst., vol. 81, no. 3, pp. 311–319, 1996.
"""
import numpy as np
from pyFTS.common import FuzzySet, FLR, fts, flrg

class ConventionalFLRG(flrg.FLRG):
    __doc__ = 'First Order Conventional Fuzzy Logical Relationship Group'

    def __init__(self, LHS, **kwargs):
        (super(ConventionalFLRG, self).__init__)(*(1, ), **kwargs)
        self.LHS = LHS
        self.RHS = set()

    def get_key(self, sets):
        return sets[self.LHS].name

    def append_rhs(self, c, **kwargs):
        self.RHS.add(c)

    def __str__(self):
        tmp = str(self.LHS) + ' -> '
        tmp2 = ''
        for c in sorted((self.RHS), key=(lambda s: s)):
            if len(tmp2) > 0:
                tmp2 = tmp2 + ','
            tmp2 = tmp2 + str(c)

        return tmp + tmp2


class ConventionalFTS(fts.FTS):
    __doc__ = 'Conventional Fuzzy Time Series'

    def __init__(self, **kwargs):
        (super(ConventionalFTS, self).__init__)(order=1, **kwargs)
        self.name = 'Conventional FTS'
        self.detail = 'Chen'
        self.shortname = 'CFTS'
        self.flrgs = {}

    def generate_flrg(self, flrs):
        for flr in flrs:
            if flr.LHS in self.flrgs:
                self.flrgs[flr.LHS].append_rhs(flr.RHS)
            else:
                self.flrgs[flr.LHS] = ConventionalFLRG(flr.LHS)
                self.flrgs[flr.LHS].append_rhs(flr.RHS)

    def train(self, data, **kwargs):
        tmpdata = self.partitioner.fuzzyfy(data, method='maximum', mode='sets')
        flrs = FLR.generate_non_recurrent_flrs(tmpdata)
        self.generate_flrg(flrs)

    def forecast(self, ndata, **kwargs):
        explain = kwargs.get('explain', False)
        l = len(ndata) if not explain else 1
        ret = []
        for k in np.arange(0, l):
            actual = FuzzySet.get_maximum_membership_fuzzyset(ndata[k], self.sets)
            if explain:
                print('Fuzzyfication:\n\n {} -> {} \n'.format(ndata[k], actual.name))
            if actual.name not in self.flrgs:
                ret.append(actual.centroid)
                if explain:
                    print('Rules:\n\n {} -> {} (Naïve)\t Midpoint: {}  \n\n'.format(actual.name, actual.name, actual.centroid))
                else:
                    _flrg = self.flrgs[actual.name]
                    mp = _flrg.get_midpoint(self.sets)
                    ret.append(mp)
                    if explain:
                        print('Rules:\n\n {} \t Midpoint: {} \n'.format(str(_flrg), mp))
                        print('Deffuzyfied value: {} \n'.format(mp))

        return ret