# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyFTS/benchmarks/knn.py
# Compiled at: 2018-04-27 13:20:12
# Size of source mod 2**32: 1984 bytes
import numpy as np
from statsmodels.tsa.tsatools import lagmat
from pyFTS.common import fts
from pyFTS.probabilistic import ProbabilityDistribution

class KNearestNeighbors(fts.FTS):
    """KNearestNeighbors"""

    def __init__(self, **kwargs):
        (super(KNearestNeighbors, self).__init__)(**kwargs)
        self.name = 'kNN'
        self.shortname = 'kNN'
        self.detail = 'K-Nearest Neighbors'
        self.is_high_order = True
        self.has_point_forecasting = True
        self.has_interval_forecasting = True
        self.has_probability_forecasting = True
        self.benchmark_only = True
        self.min_order = 1
        self.alpha = kwargs.get('alpha', 0.05)
        self.lag = None
        self.k = kwargs.get('k', 30)
        self.uod = None

    def train(self, data, **kwargs):
        self.data = np.array(data)

    def knn(self, sample):
        if self.order == 1:
            dist = np.apply_along_axis(lambda x: (x - sample) ** 2, 0, self.data)
            ix = np.argsort(dist) + 1
        else:
            dist = []
            for k in np.arange(self.order, len(self.data)):
                dist.append(sum([(self.data[(k - kk)] - sample[kk]) ** 2 for kk in range(self.order)]))

            ix = np.argsort(np.array(dist)) + self.order + 1
        ix2 = np.clip(ix[:self.k], 0, len(self.data) - 1)
        return self.data[ix2]

    def forecast_distribution(self, data, **kwargs):
        ret = []
        smooth = kwargs.get('smooth', 'KDE')
        alpha = kwargs.get('alpha', None)
        uod = self.get_UoD()
        for k in np.arange(self.order, len(data)):
            sample = data[k - self.order:k]
            forecasts = self.knn(sample)
            dist = (ProbabilityDistribution.ProbabilityDistribution)(smooth, uod=uod, data=forecasts, name='', **kwargs)
            ret.append(dist)

        return ret