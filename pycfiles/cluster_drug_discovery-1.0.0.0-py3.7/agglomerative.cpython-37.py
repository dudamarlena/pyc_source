# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cluster_drug_discovery/methods/agglomerative.py
# Compiled at: 2019-09-30 08:30:28
# Size of source mod 2**32: 1037 bytes
from sklearn.cluster import AgglomerativeClustering
import cluster_drug_discovery.methods.clusterclass as cls

class AgglomerativeAlg(cls.Cluster):
    __doc__ = '\n     Hierarchical clustering is a general family of clustering algorithms that build nested clusters by merging or splitting them successively. This hierarchy of clusters is represented as a tree (or dendrogram). The root of the tree is the unique cluster that gathers all the samples, the leaves being the clusters with only one sample. See the Wikipedia page for more details.\n\n     Implementation from : https://scikit-learn.org/stable/modules/generated/sklearn.cluster.AgglomerativeClustering.html#sklearn.cluster.AgglomerativeClustering\n    '

    def __init__(self, data, nclust):
        cls.Cluster.__init__(self, data)
        self.nclust = nclust

    def _run(self):
        print('Clustering with Agglomerative Clustering...')
        self._clusterer = AgglomerativeClustering(n_clusters=(self.nclust))
        return self._clusterer.fit_predict(self.data)