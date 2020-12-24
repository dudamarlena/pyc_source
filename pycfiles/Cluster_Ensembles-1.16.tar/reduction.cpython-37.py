# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cluster_drug_discovery/dimensionallity/reduction.py
# Compiled at: 2019-06-11 07:56:19
# Size of source mod 2**32: 664 bytes
from sklearn.decomposition import PCA
import umap

class ReduceDimension(object):

    def __init__(self, data, n_components):
        self.data = data
        self.n_components = n_components

    def run(self, method):
        if method == 'umap':
            return self.compute_umap()
        if method == 'pca':
            return self.compute_pca()

    def compute_pca(self):
        pca = PCA(n_components=(self.n_components))
        return pca.fit_transform(self.data)

    def compute_umap(self, neighbors=5, min_dist=0.2):
        reducer = umap.UMAP(n_neighbors=neighbors, min_dist=min_dist)
        return reducer.fit_transform(self.data)