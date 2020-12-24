# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cluster_drug_discovery/methods/dbscan.py
# Compiled at: 2019-06-11 07:56:19
# Size of source mod 2**32: 1548 bytes
from sklearn.cluster import DBSCAN
import cluster_drug_discovery.methods.clusterclass as cls

class DbscanAlg(cls.Cluster):
    """DbscanAlg"""

    def __init__(self, data, epsilon=3, min_samples=2):
        cls.Cluster.__init__(self, data)
        self.epsilon = epsilon
        self.min_samples = min_samples

    def _run(self):
        print('Clustering with Dbscan Algorithm...')
        self._clusterer = DBSCAN(eps=(self.epsilon), min_samples=(self.min_samples))
        return self._clusterer.fit_predict(self.data)