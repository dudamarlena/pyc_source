# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cluster_drug_discovery/methods/kmeans.py
# Compiled at: 2019-09-30 06:50:01
# Size of source mod 2**32: 1193 bytes
from sklearn.cluster import KMeans
import cluster_drug_discovery.methods.clusterclass as cls

class KmeansAlg(cls.Cluster):
    __doc__ = "\n     K-Means Clustering Advantages and Disadvantages\n     K-Means Advantages :\n    \n     1) If variables are huge, then  K-Means most of the times computationally faster than hierarchical clustering, if we keep k smalls.\n    \n     2) K-Means produce tighter clusters than hierarchical clustering, especially if the clusters are globular.\n    \n     K-Means Disadvantages :\n    \n     1) Difficult to predict K-Value.\n     2) With global cluster, it didn't work well.\n     3) Different initial partitions can result in different final clusters.\n     4) It does not work well with different size and density clusters\n     \n     Implementation from : https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html#sklearn.cluster.KMeans\n    "

    def __init__(self, data, nclust):
        cls.Cluster.__init__(self, data)
        self.nclust = nclust

    def _run(self):
        print('Clustering with Kmeans Algorithm...')
        self._clusterer = KMeans(n_clusters=(self.nclust))
        return self._clusterer.fit_predict(self.data)