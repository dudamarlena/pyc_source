# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/user/feldbauer/PycharmProjects/hubness/skhubness/neighbors/random_projection_trees.py
# Compiled at: 2019-10-30 06:53:24
# Size of source mod 2**32: 8644 bytes
from __future__ import annotations
import logging
from typing import Union, Tuple
try:
    import annoy
except ImportError:
    annoy = None

import numpy as np
from sklearn.base import BaseEstimator
from sklearn.utils.validation import check_array, check_is_fitted, check_X_y
from tqdm.auto import tqdm
from .approximate_neighbors import ApproximateNearestNeighbor
from utils.check import check_n_candidates
from utils.io import create_tempfile_preferably_in_dir
__all__ = [
 'RandomProjectionTree']

class RandomProjectionTree(BaseEstimator, ApproximateNearestNeighbor):
    __doc__ = 'Wrapper for using annoy.AnnoyIndex\n\n    Annoy is an approximate nearest neighbor library,\n    that builds a forest of random projections trees.\n\n    Parameters\n    ----------\n    n_candidates: int, default = 5\n        Number of neighbors to retrieve\n    metric: str, default = \'euclidean\'\n        Distance metric, allowed are "angular", "euclidean", "manhattan", "hamming", "dot"\n    n_trees: int, default = 10\n        Build a forest of n_trees trees. More trees gives higher precision when querying,\n        but are more expensive in terms of build time and index size.\n    search_k: int, default = -1\n        Query will inspect search_k nodes. A larger value will give more accurate results,\n        but will take longer time.\n    mmap_dir: str, default = \'auto\'\n        Memory-map the index to the given directory.\n        This is required to make the the class pickleable.\n        If None, keep everything in main memory (NON pickleable index),\n        if mmap_dir is a string, it is interpreted as a directory to store the index into,\n        if \'auto\', create a temp dir for the index, preferably in /dev/shm on Linux.\n    n_jobs: int, default = 1\n        Number of parallel jobs\n    verbose: int, default = 0\n        Verbosity level. If verbose > 0, show tqdm progress bar on indexing and querying.\n\n    Attributes\n    ----------\n    valid_metrics:\n        List of valid distance metrics/measures\n    '
    valid_metrics = ['angular', 'euclidean', 'manhattan', 'hamming', 'dot', 'minkowski']

    def __init__(self, n_candidates=5, metric='euclidean', n_trees=10, search_k=-1, mmap_dir='auto', n_jobs=1, verbose=0):
        if annoy is None:
            raise ImportError('Please install the `annoy` package, before using this class.\n$ pip install annoy') from None
        super().__init__(n_candidates=n_candidates, metric=metric,
          n_jobs=n_jobs,
          verbose=verbose)
        self.n_trees = n_trees
        self.search_k = search_k
        self.mmap_dir = mmap_dir

    def fit(self, X, y=None) -> 'RandomProjectionTree':
        """ Build the annoy.Index and insert data from X.

        Parameters
        ----------
        X: np.array
            Data to be indexed
        y: any
            Ignored

        Returns
        -------
        self: RandomProjectionTree
            An instance of RandomProjectionTree with a built index
        """
        if y is None:
            X = check_array(X)
        else:
            X, y = check_X_y(X, y)
            self.y_train_ = y
        self.n_samples_fit_ = X.shape[0]
        self.n_features_ = X.shape[1]
        self.X_dtype_ = X.dtype
        if self.metric == 'minkowski':
            self.metric = 'euclidean'
        else:
            metric = self.metric if self.metric != 'sqeuclidean' else 'euclidean'
            self.effective_metric_ = metric
            annoy_index = annoy.AnnoyIndex((X.shape[1]), metric=metric)
            if self.mmap_dir == 'auto':
                self.annoy_ = create_tempfile_preferably_in_dir(prefix='skhubness_', suffix='.annoy',
                  directory='/dev/shm')
                logging.warning(f"The index will be stored in {self.annoy_}. It will NOT be deleted automatically, when this instance is destructed.")
            else:
                if isinstance(self.mmap_dir, str):
                    self.annoy_ = create_tempfile_preferably_in_dir(prefix='skhubness_', suffix='.annoy',
                      directory=(self.mmap_dir))
                else:
                    self.mmap_dir = None
            for i, x in tqdm((enumerate(X)), desc='Build RPtree', disable=(False if self.verbose else True)):
                annoy_index.add_item(i, x.tolist())

            annoy_index.build(self.n_trees)
            if self.mmap_dir is None:
                self.annoy_ = annoy_index
            else:
                annoy_index.save(self.annoy_)
        return self

    def kneighbors(self, X=None, n_candidates=None, return_distance=True) -> 'Union[Tuple[np.array, np.array], np.array]':
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
        check_is_fitted(self, 'annoy_')
        if X is not None:
            X = check_array(X)
        else:
            n_test = self.n_samples_fit_ if X is None else X.shape[0]
            dtype = self.X_dtype_ if X is None else X.dtype
            if n_candidates is None:
                n_candidates = self.n_candidates
            else:
                n_candidates = check_n_candidates(n_candidates)
                if X is None:
                    n_neighbors = n_candidates + 1
                    start = 1
                else:
                    n_neighbors = n_candidates
                start = 0
            neigh_ind = -np.ones((n_test, n_candidates), dtype=(np.int32))
            neigh_dist = np.empty_like(neigh_ind, dtype=dtype) * np.nan
            if isinstance(self.annoy_, str):
                annoy_index = annoy.AnnoyIndex((self.n_features_), metric=(self.effective_metric_))
                annoy_index.load(self.annoy_)
            else:
                if isinstance(self.annoy_, annoy.AnnoyIndex):
                    annoy_index = self.annoy_
        assert isinstance(annoy_index, annoy.AnnoyIndex), 'Internal error: unexpected type for annoy index'
        disable_tqdm = False if self.verbose else True
        if X is None:
            n_items = annoy_index.get_n_items()
            for i in tqdm((range(n_items)), desc='Query RPtree',
              disable=disable_tqdm):
                ind, dist = annoy_index.get_nns_by_item(i,
                  n_neighbors, (self.search_k), include_distances=True)
                ind = ind[start:]
                dist = dist[start:]
                neigh_ind[i, :len(ind)] = ind
                neigh_dist[i, :len(dist)] = dist

        else:
            for i, x in tqdm((enumerate(X)), desc='Query RPtree',
              disable=disable_tqdm):
                ind, dist = annoy_index.get_nns_by_vector((x.tolist()),
                  n_neighbors, (self.search_k), include_distances=True)
                ind = ind[start:]
                dist = dist[start:]
                neigh_ind[i, :len(ind)] = ind
                neigh_dist[i, :len(dist)] = dist

        if self.metric == 'sqeuclidean':
            neigh_dist **= 2
        if return_distance:
            return (
             neigh_dist, neigh_ind)
        return neigh_ind