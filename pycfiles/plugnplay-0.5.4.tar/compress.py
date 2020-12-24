# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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