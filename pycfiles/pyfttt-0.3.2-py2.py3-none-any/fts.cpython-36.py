# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyFTS/fcm/fts.py
# Compiled at: 2019-04-26 16:24:46
# Size of source mod 2**32: 769 bytes
from pyFTS.common import fts
from pyFTS.models import hofts
from pyFTS.fcm import common
import numpy as np

class FCM_FTS(hofts.HighOrderFTS):

    def __init__(self, **kwargs):
        (super(FCM_FTS, self).__init__)(**kwargs)
        self.fcm = (common.FuzzyCognitiveMap)(**kwargs)

    def forecast(self, ndata, **kwargs):
        ret = []
        midpoints = np.array([fset.centroid for fset in self.partitioner])
        for t in np.arange(self.order, len(ndata) + 1):
            sample = ndata[t - self.order:t]
            fuzzyfied = self.partitioner.fuzzyfy(sample, mode='vector')
            activation = self.fcm.activate(fuzzyfied)
            final = np.dot(midpoints, activation) / np.sum(activation)
            ret.append(final)

        return ret