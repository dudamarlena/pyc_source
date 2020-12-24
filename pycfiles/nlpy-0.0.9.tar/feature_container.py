# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hadoop/nlpy/nlpy/util/feature_container.py
# Compiled at: 2014-12-01 04:14:13
import numpy as np
from line_iterator import LineIterator

class FeatureContainer(object):

    def __init__(self, path=None, dtype='libsvm', feature_n=-1):
        self.N = 0
        self.data = np.zeros(0)
        self.targets = np.zeros(0)
        self.feature_n = feature_n
        self.path = path
        self.dtype = dtype

    def read(self):
        """
        Read feature matrix from data
        :param path: data path
        :param type: libsvm (only)
        """
        ys = []
        xs = []
        for line in LineIterator(self.path):
            items = line.split(' ')
            feature_map = {}
            y = 0
            for item in items:
                if ':' in item:
                    feature_idx, value = item.split(':')
                    feature_map[int(feature_idx)] = float(value)
                else:
                    y = int(item)

            if self.feature_n == -1:
                max_key = max(feature_map.keys()) if feature_map else 0
            else:
                max_key = self.feature_n
            features = []
            for fidx in range(1, max_key + 1):
                if fidx in feature_map:
                    features.append(feature_map[fidx])
                else:
                    features.append(0)

            yield (
             features, y)