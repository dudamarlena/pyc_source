# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyFTS/models/song.py
# Compiled at: 2019-04-09 15:22:00
# Size of source mod 2**32: 2709 bytes
__doc__ = '\nFirst Order Traditional Fuzzy Time Series method by Song & Chissom (1993)\n\nQ. Song and B. S. Chissom, “Fuzzy time series and its models,” Fuzzy Sets Syst., vol. 54, no. 3, pp. 269–277, 1993.\n'
import numpy as np
from pyFTS.common import FuzzySet, FLR, fts

class ConventionalFTS(fts.FTS):
    """ConventionalFTS"""

    def __init__(self, **kwargs):
        (super(ConventionalFTS, self).__init__)(order=1, name='FTS', **kwargs)
        self.name = 'Traditional FTS'
        self.detail = 'Song & Chissom'
        if self.sets is not None:
            if self.partitioner is not None:
                self.sets = self.partitioner.sets
        self.R = None
        if self.sets is not None:
            l = len(self.sets)
            self.R = np.zeros((l, l))

    def flr_membership_matrix(self, flr):
        ordered_set = FuzzySet.set_ordered(self.sets)
        centroids = [self.sets[k].centroid for k in ordered_set]
        lm = [self.sets[flr.LHS].membership(k) for k in centroids]
        rm = [self.sets[flr.RHS].membership(k) for k in centroids]
        l = len(ordered_set)
        r = np.zeros((l, l))
        for k in range(0, l):
            for l in range(0, l):
                r[k][l] = min(lm[k], rm[l])

        return r

    def operation_matrix(self, flrs):
        l = len(self.sets)
        if self.R is None or len(self.R) == 0:
            self.R = np.zeros((l, l))
        for k in flrs:
            mm = self.flr_membership_matrix(k)
            for k in range(0, l):
                for l in range(0, l):
                    self.R[k][l] = max(self.R[k][l], mm[k][l])

    def train(self, data, **kwargs):
        tmpdata = self.partitioner.fuzzyfy(data, method='maximum', mode='sets')
        flrs = FLR.generate_non_recurrent_flrs(tmpdata)
        self.operation_matrix(flrs)

    def forecast(self, ndata, **kwargs):
        if self.partitioner is not None:
            ordered_sets = self.partitioner.ordered_sets
        else:
            ordered_sets = FuzzySet.set_ordered(self.sets)
        l = len(ndata)
        npart = len(self.sets)
        ret = []
        for k in np.arange(0, l):
            mv = FuzzySet.fuzzyfy_instance(ndata[k], self.sets)
            r = [max([min(self.R[i][j], mv[j]) for j in np.arange(0, npart)]) for i in np.arange(0, npart)]
            fs = np.ravel(np.argwhere(r == max(r)))
            if len(fs) == 1:
                ret.append(self.sets[ordered_sets[fs[0]]].centroid)
            else:
                mp = [self.sets[ordered_sets[s]].centroid for s in fs]
                ret.append(sum(mp) / len(mp))

        return ret

    def __str__(self):
        tmp = self.name + ':\n'
        return tmp + str(self.R)