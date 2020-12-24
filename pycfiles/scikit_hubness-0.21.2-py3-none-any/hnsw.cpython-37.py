# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/user/feldbauer/PycharmProjects/hubness/skhubness/neighbors/hnsw.py
# Compiled at: 2019-11-22 10:10:44
# Size of source mod 2**32: 5990 bytes
from __future__ import annotations
from typing import Tuple, Union
import numpy as np
from sklearn.utils.validation import check_is_fitted, check_array
try:
    import nmslib
except (ImportError, ModuleNotFoundError):
    nmslib = None

from .approximate_neighbors import ApproximateNearestNeighbor
from utils.check import check_n_candidates
__all__ = [
 'HNSW']

class HNSW(ApproximateNearestNeighbor):
    __doc__ = 'Wrapper for using nmslib\n\n    Hierarchical navigable small-world graphs are data structures,\n    that allow for approximate nearest neighbor search.\n    Here, an implementation from nmslib is used.\n\n    Parameters\n    ----------\n    n_candidates: int, default = 5\n        Number of neighbors to retrieve\n    metric: str, default = \'euclidean\'\n        Distance metric, allowed are "angular", "euclidean", "manhattan", "hamming", "dot"\n    method: str, default = \'hnsw\',\n        ANN method to use. Currently, only \'hnsw\' is supported.\n    post_processing: int, default = 2\n        More post processing means longer index creation,\n        and higher retrieval accuracy.\n    n_jobs: int, default = 1\n        Number of parallel jobs\n    verbose: int, default = 0\n        Verbosity level. If verbose >= 2, show progress bar on indexing.\n\n    Attributes\n    ----------\n    valid_metrics:\n        List of valid distance metrics/measures\n    '
    valid_metrics = ['euclidean', 'l2', 'minkowski', 'squared_euclidean', 'sqeuclidean',
     'cosine', 'cosinesimil']

    def __init__(self, n_candidates=5, metric='euclidean', method='hnsw', post_processing=2, n_jobs=1, verbose=0):
        if nmslib is None:
            raise ImportError('Please install the `nmslib` package, before using this class.\n$ pip install nmslib') from None
        super().__init__(n_candidates=n_candidates, metric=metric,
          n_jobs=n_jobs,
          verbose=verbose)
        self.method = method
        self.post_processing = post_processing
        self.space = None

    def fit(self, X, y=None) -> 'HNSW':
        """ Setup the HNSW index from training data.

        Parameters
        ----------
        X: np.array
            Data to be indexed
        y: any
            Ignored

        Returns
        -------
        self: HNSW
            An instance of HNSW with a built graph
        """
        X = check_array(X)
        method = self.method
        post_processing = self.post_processing
        if self.metric in ('euclidean', 'l2', 'minkowski', 'squared_euclidean', 'sqeuclidean'):
            if self.metric in ('squared_euclidean', 'sqeuclidean'):
                self.metric = 'sqeuclidean'
            else:
                self.metric = 'euclidean'
            self.space = 'l2'
        else:
            if self.metric in ('cosine', 'cosinesimil'):
                self.space = 'cosinesimil'
            else:
                raise ValueError(f'Invalid metric "{self.metric}". Please try "euclidean" or "cosine".')
        hnsw_index = nmslib.init(method=method, space=(self.space))
        hnsw_index.addDataPointBatch(X)
        hnsw_index.createIndex({'post':post_processing,  'indexThreadQty':self.n_jobs},
          print_progress=(self.verbose >= 2))
        self.index_ = hnsw_index
        self.n_samples_fit_ = len(self.index_)
        assert self.space in ('l2', 'cosinesimil'), f"Internal: self.space={self.space} not allowed"
        return self

    def kneighbors(self, X: 'np.ndarray'=None, n_candidates: 'int'=None, return_distance: 'bool'=True) -> 'Union[Tuple[np.array, np.array], np.array]':
        """ Retrieve k nearest neighbors.

        Parameters
        ----------
        X: np.array or None, optional, default = None
            Query objects. If None, search among the indexed objects.
        n_candidates: int or None, optional, default = None
            Number of neighbors to retrieve.
            If None, use the value passed during construction.
        return_distance: bool, default = True
            If return_distance, will return distances and indices to neighbors.
            Else, only return the indices.
        """
        check_is_fitted(self, ['index_'])
        if X is None:
            raise NotImplementedError('Please provide X to hnsw.kneighbors().')
        if n_candidates is None:
            n_candidates = self.n_candidates
        n_candidates = check_n_candidates(n_candidates)
        neigh_ind_dist = self.index_.knnQueryBatch(X, k=n_candidates,
          num_threads=(self.n_jobs))
        n_test = X.shape[0]
        neigh_ind = -np.ones((n_test, n_candidates), dtype=(np.int32))
        neigh_dist = np.empty_like(neigh_ind, dtype=(X.dtype)) * np.nan
        for i, (ind, dist) in enumerate(neigh_ind_dist):
            neigh_ind[i, :ind.size] = ind
            neigh_dist[i, :dist.size] = dist

        if self.space == 'cosinesimil':
            neigh_dist *= -1
            neigh_dist += 1
        else:
            if self.space == 'l2':
                if self.metric == 'sqeuclidean':
                    neigh_dist **= 2
        if return_distance:
            return (
             neigh_dist, neigh_ind)
        return neigh_ind