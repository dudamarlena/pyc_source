# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/kemlglearn/cluster/consensus/MeanPartition.py
# Compiled at: 2018-02-01 02:52:53
"""
.. module:: MeanPartition

MeanPartition
*************

:Description: MeanPartition

    

:Authors: bejar
    

:Version: 

:Created on: 10/02/2015 9:40 

"""
__author__ = 'bejar'
import numpy as np
from sklearn.base import BaseEstimator, ClusterMixin, TransformerMixin
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.cluster import KMeans, SpectralClustering
from sklearn.metrics import adjusted_mutual_info_score, adjusted_rand_score, v_measure_score
from sklearn.manifold import MDS, TSNE, SpectralEmbedding

class MeanPartitionClustering(BaseEstimator, ClusterMixin, TransformerMixin):
    """Consensus Clustering Algorithm based on the estimation of the mean partition
    """

    def __init__(self, n_clusters, base='kmeans', n_components=10, cdistance='ANMI', trans='spectral', n_neighbors=5):
        self.n_clusters = n_clusters
        self.cluster_centers_ = None
        self.labels_ = None
        self.cluster_sizes_ = None
        self.base = base
        self.n_components = n_components
        self.trans = trans
        self.cdistance = cdistance
        self.n_neighbors = n_neighbors
        return

    def fit(self, X, y):
        """
        Clusters the examples
        :param X:
        :return:
        """
        baseclust = [
         y]
        if self.base == 'kmeans':
            km = KMeans(n_clusters=self.n_clusters, n_init=1)
        l = [
         'r']
        for i in range(self.n_components):
            km.fit(X)
            baseclust.append(km.labels_)
            l.append('b')

        mdist = np.zeros((self.n_components, self.n_components))
        if self.cdistance == 'ANMI':
            dfun = adjusted_mutual_info_score
        else:
            if self.cdistance == 'ARAND':
                dfun = adjusted_rand_score
            elif self.cdistance == 'vmeasure':
                dfun = v_measure_score
            for i in range(self.n_components - 1):
                for j in range(i + 1, self.n_components):
                    mdist[(i, j)] = dfun(baseclust[i], baseclust[j])
                    mdist[(j, i)] = mdist[(i, j)]

        if self.trans == 'MDS':
            embed = MDS(dissimilarity='precomputed')
        elif self.trans == 'TNE':
            embed = TSNE(metric='precomputed')
        elif self.trans == 'spectral':
            embed = SpectralEmbedding(affinity='precomputed', n_neighbors=self.n_neighbors)
        X = embed.fit_transform(mdist)
        return (
         X, l)