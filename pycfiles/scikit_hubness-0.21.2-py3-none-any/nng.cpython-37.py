# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/user/feldbauer/PycharmProjects/hubness/skhubness/neighbors/nng.py
# Compiled at: 2019-11-22 10:10:44
# Size of source mod 2**32: 11649 bytes
from __future__ import annotations
import logging, pathlib
from typing import Union, Tuple
try:
    import ngtpy
except (ImportError, ModuleNotFoundError):
    ngtpy = None

import numpy as np
from sklearn.base import BaseEstimator
from sklearn.utils.validation import check_array, check_is_fitted, check_X_y
from tqdm.auto import tqdm
from .approximate_neighbors import ApproximateNearestNeighbor
from utils.check import check_n_candidates
from utils.io import create_tempfile_preferably_in_dir
__all__ = [
 'NNG']

class NNG(BaseEstimator, ApproximateNearestNeighbor):
    __doc__ = "Wrapper for ngtpy and NNG variants.\n\n    By default, the graph is an ANNG. Only when the `optimize` parameter is set,\n    the graph is optimized to obtain an ONNG.\n\n    Parameters\n    ----------\n    n_candidates: int, default = 5\n        Number of neighbors to retrieve\n    metric: str, default = 'euclidean'\n        Distance metric, allowed are 'manhattan', 'L1', 'euclidean', 'L2', 'minkowski',\n        'Angle', 'Normalized Angle', 'Hamming', 'Jaccard', 'Cosine' or 'Normalized Cosine'.\n    index_dir: str, default = 'auto'\n        Store the index in the given directory.\n        If None, keep the index in main memory (NON pickleable index),\n        If index_dir is a string, it is interpreted as a directory to store the index into,\n        if 'auto', create a temp dir for the index, preferably in /dev/shm on Linux.\n        Note: The directory/the index will NOT be deleted automatically.\n    optimize: bool, default = False\n        Use ONNG method by optimizing the ANNG graph.\n        May require long time for index creation.\n    edge_size_for_creation: int, default = 80\n        Increasing ANNG edge size improves retrieval accuracy at the cost of more time\n    edge_size_for_search: int, default = 40\n        Increasing ANNG edge size improves retrieval accuracy at the cost of more time\n    epsilon: float, default 0.1\n        Trade-off in ANNG between higher accuracy (larger epsilon) and shorter query time (smaller epsilon)\n    num_incoming: int\n        Number of incoming edges in ONNG graph\n    num_outgoing: int\n        Number of outgoing edges in ONNG graph\n    n_jobs: int, default = 1\n        Number of parallel jobs\n    verbose: int, default = 0\n        Verbosity level. If verbose > 0, show tqdm progress bar on indexing and querying.\n\n    Attributes\n    ----------\n    valid_metrics:\n        List of valid distance metrics/measures\n\n    Notes\n    -----\n    NNG stores the index to a directory specified in `index_dir`.\n    The index is persistent, and will NOT be deleted automatically.\n    It is the user's responsibility to take care of deletion,\n    when required.\n    "
    valid_metrics = ['manhattan', 'L1', 'euclidean', 'L2', 'minkowski', 'sqeuclidean',
     'Angle', 'Normalized Angle', 'Cosine', 'Normalized Cosine', 'Hamming', 'Jaccard']
    internal_distance_type = {'manhattan':'L1',  'euclidean':'L2', 
     'minkowski':'L2', 
     'sqeuclidean':'L2'}

    def __init__(self, n_candidates=5, metric='euclidean', index_dir='auto', optimize=False, edge_size_for_creation=80, edge_size_for_search=40, num_incoming=-1, num_outgoing=-1, epsilon=0.1, n_jobs=1, verbose=0):
        if ngtpy is None:
            raise ImportError('Please install the `ngt` package, before using this class.\n$ pip3 install ngt') from None
        super().__init__(n_candidates=n_candidates, metric=metric,
          n_jobs=n_jobs,
          verbose=verbose)
        self.index_dir = index_dir
        self.optimize = optimize
        self.edge_size_for_creation = edge_size_for_creation
        self.edge_size_for_search = edge_size_for_search
        self.num_incoming = num_incoming
        self.num_outgoing = num_outgoing
        self.epsilon = epsilon

    def fit(self, X, y=None) -> 'NNG':
        """ Build the ngtpy.Index and insert data from X.

        Parameters
        ----------
        X: np.array
            Data to be indexed
        y: any
            Ignored

        Returns
        -------
        self: NNG
            An instance of NNG with a built index
        """
        if y is None:
            X = check_array(X)
        else:
            X, y = check_X_y(X, y)
            self.y_train_ = y
        self.n_samples_fit_ = X.shape[0]
        self.n_features_ = X.shape[1]
        self.X_dtype_ = X.dtype
        try:
            self.effective_metric_ = NNG.internal_distance_type[self.metric]
        except KeyError:
            self.effective_metric_ = self.metric

        if self.effective_metric_ not in NNG.valid_metrics:
            raise ValueError(f"Unknown distance/similarity measure: {self.effective_metric_}. Please use one of: {NNG.valid_metrics}.")
        else:
            prefix = 'skhubness_'
            suffix = '.anng'
            if self.index_dir in ('auto', ):
                index_path = create_tempfile_preferably_in_dir(prefix=prefix, suffix=suffix,
                  directory='/dev/shm')
                logging.warning(f"The index will be stored in {index_path}. It will NOT be deleted automatically, when this instance is destructed.")
            else:
                if isinstance(self.index_dir, str):
                    index_path = create_tempfile_preferably_in_dir(prefix=prefix, suffix=suffix,
                      directory=(self.index_dir))
                else:
                    if self.index_dir is None:
                        index_path = create_tempfile_preferably_in_dir(prefix=prefix, suffix=suffix)
                    else:
                        raise TypeError('NNG requires to write an index to the filesystem. Please provide a valid path with parameter `index_dir`.')
            ngtpy.create(path=index_path, dimension=(self.n_features_),
              edge_size_for_creation=(self.edge_size_for_creation),
              edge_size_for_search=(self.edge_size_for_search),
              distance_type=(self.effective_metric_))
            index_obj = ngtpy.Index(index_path)
            index_obj.batch_insert(X, num_threads=(self.n_jobs))
            index_obj.save()
            if self.optimize:
                optimizer = ngtpy.Optimizer()
                optimizer.set(num_of_outgoings=(self.num_outgoing), num_of_incomings=(self.num_incoming))
                index_path_onng = str(pathlib.Path(index_path).with_suffix('.onng'))
                optimizer.execute(index_path, index_path_onng)
                index_path = index_path_onng
            if self.index_dir is None:
                self.index_ = index_obj
            else:
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
                if return_distance:
                    neigh_dist = np.empty_like(neigh_ind, dtype=dtype) * np.nan
                if isinstance(self.index_, str):
                    index = ngtpy.Index(self.index_)
                else:
                    index = self.index_
            disable_tqdm = False if self.verbose else True
            if X is None:
                for i in tqdm((range(n_test)), desc='Query NNG', disable=disable_tqdm):
                    query = index.get_object(i)
                    response = index.search(query=query, size=n_neighbors,
                      with_distance=return_distance,
                      epsilon=(self.epsilon))
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
                for i, x in tqdm((enumerate(X)), desc='Query NNG',
                  disable=disable_tqdm):
                    response = index.search(query=x, size=n_neighbors,
                      with_distance=return_distance,
                      epsilon=(self.epsilon))
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