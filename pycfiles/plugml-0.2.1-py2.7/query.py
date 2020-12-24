# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\plugml\query.py
# Compiled at: 2015-02-06 12:59:09
import numpy as np
from sklearn.neighbors import NearestNeighbors

class KNN(object):

    def __init__(self, data):
        self._nn = NearestNeighbors(algorithm='brute', metric='cosine')
        self._nn.fit(data)

    def query(self, v, k=10):
        _, idx = self._nn.kneighbors(v, k)
        return idx[0]