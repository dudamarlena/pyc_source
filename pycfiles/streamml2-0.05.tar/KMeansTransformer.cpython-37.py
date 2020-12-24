# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\bmccs\Desktop\streamml2\streamml2\streamline\transformation\transformers\KMeansTransformer.py
# Compiled at: 2019-01-19 21:05:43
# Size of source mod 2**32: 571 bytes
from ..AbstractTransformer import *
from sklearn.cluster import KMeans

class KMeansTransformer(AbstractTransformer):

    def __init__(self, nclusters):
        self._n_clusters = nclusters
        AbstractTransformer.__init__(self, 'scale')

    def transform(self, X):
        kmeans = KMeans(n_clusters=(self._n_clusters)).fit(X)
        X['cluster'] = pd.DataFrame((kmeans.labels_), columns=['cluster'], dtype='category')
        return X