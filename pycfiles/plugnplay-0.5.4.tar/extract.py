# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\plugml\extract.py
# Compiled at: 2015-02-10 20:54:59
import numpy as np
from scipy.sparse import hstack

class Extractor:

    def __init__(self, features, weights=None):
        self.feats = features
        self.weights = [ 1.0 for i in range(len(self.feats)) ] if not weights else weights
        self.names = [ feat.name for feat in self.feats ]
        self._map = {name:i for name, i in zip(self.names, range(len(self.feats)))}
        self.featNames = [ feat.featNames for feat in self.feats ]
        self.featNames = [ name for names in self.featNames for name in names ]
        self.dim = sum([ feat.dim for feat in self.feats ])

    def __getitem__(self, key):
        if isinstance(key, basestring):
            return self.feats[self._map[key]][:] * self.weights[self._map[key]]
        if isinstance(key, (int, long, np.int64)):
            return hstack([ feat[key] * self.weights[self._map[feat.name]] for feat in self.feats ])
        row, col = key
        if isinstance(col, basestring):
            e = self.feats[self._map[col]][row] * self.weights[self._map[key]]
        else:
            e = self.feats[col][row] * self.weights[col]
        return e

    def get(self):
        return hstack([ feat.data for feat in self.feats ])

    def transform(self, data):
        if isinstance(data, list):
            return [ self.transform(elem) for elem in data ]
        else:
            checked = {name:0 for name in self.names}
            for key in data:
                checked[key] = 1

            for key in checked:
                if checked[key] == 0:
                    data[key] = None

            feats = hstack([ feat.transform([data[feat.name]]) * self.weights[self._map[feat.name]] for feat in self.feats
                           ])
            return feats