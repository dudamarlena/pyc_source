# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyFTS/models/ifts.py
# Compiled at: 2019-03-22 10:09:43
# Size of source mod 2**32: 2605 bytes
"""
High Order Interval Fuzzy Time Series

SILVA, Petrônio CL; SADAEI, Hossein Javedani; GUIMARÃES, Frederico Gadelha. Interval Forecasting with Fuzzy Time Series.
In: Computational Intelligence (SSCI), 2016 IEEE Symposium Series on. IEEE, 2016. p. 1-8.
"""
import numpy as np
from pyFTS.common import FuzzySet, FLR, fts, tree
from pyFTS.models import hofts

class IntervalFTS(hofts.WeightedHighOrderFTS):
    __doc__ = '\n    High Order Interval Fuzzy Time Series\n    '

    def __init__(self, **kwargs):
        (super(IntervalFTS, self).__init__)(**kwargs)
        self.shortname = 'IFTS'
        self.name = 'Interval FTS'
        self.detail = 'Silva, P.; Guimarães, F.; Sadaei, H. (2016)'
        self.flrgs = {}
        self.has_point_forecasting = False
        self.has_interval_forecasting = True
        self.is_high_order = True
        self.min_order = 1

    def get_upper(self, flrg):
        ret = np.nan
        if len(flrg.LHS) > 0:
            if flrg.get_key() in self.flrgs:
                tmp = self.flrgs[flrg.get_key()]
                ret = tmp.get_upper(self.sets)
            else:
                ret = self.sets[flrg.LHS[(-1)]].upper
        return ret

    def get_lower(self, flrg):
        ret = np.nan
        if len(flrg.LHS) > 0:
            if flrg.get_key() in self.flrgs:
                tmp = self.flrgs[flrg.get_key()]
                ret = tmp.get_lower(self.partitioner.sets)
            else:
                ret = self.partitioner.sets[flrg.LHS[(-1)]].lower
        return ret

    def get_sequence_membership(self, data, fuzzySets):
        mb = [fuzzySets[k].membership(data[k]) for k in np.arange(0, len(data))]
        return mb

    def forecast_interval(self, ndata, **kwargs):
        ret = []
        l = len(ndata)
        if l <= self.order:
            return ndata
        else:
            for k in np.arange(self.max_lag, l + 1):
                sample = ndata[k - self.max_lag:k]
                flrgs = self.generate_lhs_flrg(sample)
                up = []
                lo = []
                affected_flrgs_memberships = []
                for flrg in flrgs:
                    if len(flrg.LHS) > 0:
                        mv = flrg.get_membership(sample, self.sets)
                        up.append(mv * self.get_upper(flrg))
                        lo.append(mv * self.get_lower(flrg))
                        affected_flrgs_memberships.append(mv)

                norm = sum(affected_flrgs_memberships)
                lo_ = sum(lo) / norm
                up_ = sum(up) / norm
                ret.append([lo_, up_])

            return ret