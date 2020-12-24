# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cluster_drug_discovery/methods/hdbscan.py
# Compiled at: 2019-09-30 07:06:24
# Size of source mod 2**32: 1581 bytes
import hdbscan
import cluster_drug_discovery.methods.clusterclass as cls

class HdbscanAlg(cls.Cluster):
    """HdbscanAlg"""

    def __init__(self, data, epsilon=None, min_samples=None):
        cls.Cluster.__init__(self, data)
        self.epsilon = epsilon
        self.min_samples = min_samples

    def _run(self):
        print('Clustering with hdbscan Algorithm...')
        self._clusterer = clusterer = hdbscan.HDBSCAN()
        self._clusterer.fit(self.data)
        self.nclust = self._clusterer.labels_.max()
        return clusterer.labels_