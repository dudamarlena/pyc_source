# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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