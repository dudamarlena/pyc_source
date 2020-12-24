# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cluster_drug_discovery/methods/dbscan.py
# Compiled at: 2019-06-11 07:56:19
# Size of source mod 2**32: 1548 bytes
from sklearn.cluster import DBSCAN
import cluster_drug_discovery.methods.clusterclass as cls

class DbscanAlg(cls.Cluster):
    __doc__ = '\n     The DBSCAN algorithm is deterministic, always generating the same clusters when given the same data in the same order. However, the results can differ when data is provided in a different order. First, even though the core samples will always be assigned to the same clusters, the labels of those clusters will depend on the order in which those samples are encountered in the data. Second and more importantly, the clusters to which non-core samples are assigned can differ depending on the data order. This would happen when a non-core sample has a distance lower than eps to two core samples in different clusters. By the triangular inequality, those two core samples must be more distant than eps from each other, or they would be in the same cluster. The non-core sample is assigned to whichever cluster is generated first in a pass through the data, and so the results will depend on the data ordering.\n     Implementation from : https://scikit-learn.org/stable/modules/generated/sklearn.cluster.DBSCAN.html\n    '

    def __init__(self, data, epsilon=3, min_samples=2):
        cls.Cluster.__init__(self, data)
        self.epsilon = epsilon
        self.min_samples = min_samples

    def _run(self):
        print('Clustering with Dbscan Algorithm...')
        self._clusterer = DBSCAN(eps=(self.epsilon), min_samples=(self.min_samples))
        return self._clusterer.fit_predict(self.data)