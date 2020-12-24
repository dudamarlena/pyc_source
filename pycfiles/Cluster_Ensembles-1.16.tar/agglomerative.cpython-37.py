# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cluster_drug_discovery/methods/agglomerative.py
# Compiled at: 2019-09-30 08:30:28
# Size of source mod 2**32: 1037 bytes
from sklearn.cluster import AgglomerativeClustering
import cluster_drug_discovery.methods.clusterclass as cls

class AgglomerativeAlg(cls.Cluster):
    """AgglomerativeAlg"""

    def __init__(self, data, nclust):
        cls.Cluster.__init__(self, data)
        self.nclust = nclust

    def _run(self):
        print('Clustering with Agglomerative Clustering...')
        self._clusterer = AgglomerativeClustering(n_clusters=(self.nclust))
        return self._clusterer.fit_predict(self.data)