# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/user/feldbauer/PycharmProjects/hubness/skhubness/neighbors/onng.py
# Compiled at: 2019-10-29 10:24:03
# Size of source mod 2**32: 9972 bytes
from __future__ import annotations
import logging
from typing import Union, Tuple
try:
    import ngtpy
except (ImportError, ModuleNotFoundError) as e:
    try:
        ngtpy = None
    finally:
        e = None
        del e

import numpy as np
from sklearn.base import BaseEstimator
from sklearn.utils.validation import check_array, check_is_fitted, check_X_y
from tqdm.auto import tqdm
from .approximate_neighbors import ApproximateNearestNeighbor
from utils.check import check_n_candidates
from utils.io import create_tempfile_preferably_in_dir
__all__ = [
 'ONNG']

class ONNG(BaseEstimator, ApproximateNearestNeighbor):
    __doc__ = "Wrapper for ngtpy and ONNG\n\n    Parameters\n    ----------\n    n_candidates: int, default = 5\n        Number of neighbors to retrieve\n    metric: str, default = 'euclidean'\n        Distance metric, allowed are 'manhattan', 'L1', 'euclidean', 'L2', 'minkowski',\n        'Angle', 'Normalized Angle', 'Hamming', 'Jaccard', 'Cosine' or 'Normalized Cosine'.\n    index_dir: str, default = 'auto'\n        Store the index in the given directory.\n        If None, keep the index in main memory (NON pickleable index),\n        If index_dir is a string, it is interpreted as a directory to store the index into,\n        if 'auto', create a temp dir for the index, preferably in /dev/shm on Linux.\n        Note: The directory/the index will NOT be deleted automatically.\n    n_jobs: int, default = 1\n        Number of parallel jobs\n    verbose: int, default = 0\n        Verbosity level. If verbose > 0, show tqdm progress bar on indexing and querying.\n\n    Attributes\n    ----------\n    valid_metrics:\n        List of valid distance metrics/measures\n\n    Notes\n    -----\n    ONNG stores the index to a directory specified in `index_dir`.\n    The index is persistent, and will NOT be deleted automatically.\n    It is the user's responsibility to take care of deletion,\n    when required.\n    "
    valid_metrics = ['manhattan', 'L1', 'euclidean', 'L2', 'minkowski', 'sqeuclidean',
     'Angle', 'Normalized Angle', 'Cosine', 'Normalized Cosine', 'Hamming', 'Jaccard']
    internal_distance_type = {'manhattan':'L1',  'euclidean':'L2', 
     'minkowski':'L2', 
     'sqeuclidean':'L2'}

    def __init__(self, n_candidates=5, metric='euclidean', index_dir='auto', edge_size_for_creation=40, edge_size_for_search=10, n_jobs=1, verbose=0):
        if ngtpy is None:
            raise ImportError('Please install the `ngt` package, before using this class. You may so by running $ pip3 install ngt.') from None
        super().__init__(n_candidates=n_candidates, metric=metric,
          n_jobs=n_jobs,
          verbose=verbose)
        self.index_dir = index_dir
        self.edge_size_for_creation = edge_size_for_creation
        self.edge_size_for_search = edge_size_for_search

    def fit(self, X, y=None) -> 'ONNG':
        """ Build the ngtpy.Index and insert data from X.

        Parameters
        ----------
        X: np.array
            Data to be indexed
        y: any
            Ignored

        Returns
        -------
        self: ONNG
            An instance of ONNG with a built index
        """
        if y is None:
            X = check_array(X)
        else:
            X, y = check_X_y(X, y)
            self.y_train_ = y
        self.n_samples_train_ = X.shape[0]
        self.n_features_ = X.shape[1]
        self.X_dtype_ = X.dtype
        try:
            self.effective_metric_ = ONNG.internal_distance_type[self.metric]
        except KeyError:
            self.effective_metric_ = self.metric

        if self.effective_metric_ not in ONNG.valid_metrics:
            raise ValueError(f"Unknown distance/similarity measure: {self.effective_metric_}. Please use one of: {ONNG.valid_metrics}.")
        else:
            if self.index_dir in ('auto', ):
                index_path = create_tempfile_preferably_in_dir(prefix='skhubness_', suffix='.onng',
                  directory='/dev/shm')
                logging.warning(f"The index will be stored in {index_path}. It will NOT be deleted automatically, when this instance is destructed.")
            else:
                if isinstance(self.index_dir, str):
                    index_path = create_tempfile_preferably_in_dir(prefix='skhubness_', suffix='.onng',
                      directory=(self.index_dir))
                else:
                    if self.index_dir is None:
                        index_path = create_tempfile_preferably_in_dir(prefix='skhubness_', suffix='.onng')
                    else:
                        raise TypeError('ONNG requires to write an index to the filesystem. Please provide a valid path with parameter `index_dir`.')
            ngtpy.create(path=index_path, dimension=(self.n_features_),
              edge_size_for_creation=(self.edge_size_for_creation),
              edge_size_for_search=(self.edge_size_for_search),
              distance_type=(self.effective_metric_))
            index_obj = ngtpy.Index(index_path)
            index_obj.batch_insert(X, num_threads=(self.n_jobs))
            if self.index_dir is None:
                self.index_ = index_obj
            else:
                index_obj.save()
            self.index_ = index_path
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
        check_is_fitted(self, 'index_')
        if X is not None:
            X = check_array(X)
        else:
            n_test = self.n_samples_train_ if X is None else X.shape[0]
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
                if return_distance:
                    neigh_dist = np.empty_like(neigh_ind, dtype=dtype) * np.nan
                if isinstance(self.index_, str):
                    index = ngtpy.Index(self.index_)
                else:
                    index = self.index_
            disable_tqdm = False if self.verbose else True
            if X is None:
                for i in tqdm((range(n_test)), desc='Query ONNG', disable=disable_tqdm):
                    query = index.get_object(i)
                    response = index.search(query=query, size=n_neighbors,
                      with_distance=return_distance)
                    if return_distance:
                        ind, dist = [np.array(arr) for arr in zip(*response)]
                    else:
                        ind = response
                    ind = ind[start:]
                    neigh_ind[i, :len(ind)] = ind
                    if return_distance:
                        dist = dist[start:]
                        neigh_dist[i, :len(dist)] = dist

            else:
                for i, x in tqdm((enumerate(X)), desc='Query ONNG',
                  disable=disable_tqdm):
                    response = index.search(query=x, size=n_neighbors,
                      with_distance=return_distance)
                    if return_distance:
                        ind, dist = [np.array(arr) for arr in zip(*response)]
                    else:
                        ind = response
                    ind = ind[start:]
                    neigh_ind[i, :len(ind)] = ind
                    if return_distance:
                        dist = dist[start:]
                        neigh_dist[i, :len(dist)] = dist

        if return_distance:
            if self.metric == 'sqeuclidean':
                neigh_dist **= 2
        if return_distance:
            return (
             neigh_dist, neigh_ind)
        return neigh_ind