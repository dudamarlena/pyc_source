# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\plugml\compress.py
# Compiled at: 2015-02-03 10:29:22
from sklearn.decomposition import TruncatedSVD

class Compressor(object):

    def __init__(self, extractor, dim):
        self.extractor = extractor
        self.dim = dim
        self._svd = TruncatedSVD(dim)
        self._svd.fit(self.extractor.get())

    def get(self):
        return self._svd.transform(self.extractor.get())

    def transform(self, data):
        return self._svd.transform(data)