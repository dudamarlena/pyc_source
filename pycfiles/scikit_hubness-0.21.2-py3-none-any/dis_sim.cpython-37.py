# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/user/feldbauer/PycharmProjects/hubness/skhubness/reduction/dis_sim.py
# Compiled at: 2019-08-29 04:04:58
# Size of source mod 2**32: 6993 bytes
from __future__ import annotations
import warnings, numpy as np
from sklearn.metrics import euclidean_distances
from sklearn.utils.extmath import row_norms
from sklearn.utils.validation import check_is_fitted, check_consistent_length, check_array
from .base import HubnessReduction

class DisSimLocal(HubnessReduction):
    __doc__ = ' Hubness reduction with DisSimLocal [1]_.\n\n    Parameters\n    ----------\n    k: int, default = 5\n        Number of neighbors to consider for the local centroids\n\n    squared: bool, default = True\n        DisSimLocal operates on squared Euclidean distances.\n        If True, return (quasi) squared Euclidean distances;\n        if False, return (quasi) Eucldean distances.\n\n    References\n    ----------\n    .. [1] Hara K, Suzuki I, Kobayashi K, Fukumizu K, Radovanović M (2016)\n           Flattening the density gradient for eliminating spatial centrality to reduce hubness.\n           In: Proceedings of the 30th AAAI conference on artificial intelligence, pp 1659–1665.\n           https://www.aaai.org/ocs/index.php/AAAI/AAAI16/paper/viewPaper/12055\n    '

    def __init__(self, k=5, squared=True, *args, **kwargs):
        super().__init__()
        self.k = k
        self.squared = squared

    def fit(self, neigh_dist: 'np.ndarray', neigh_ind: 'np.ndarray', X: 'np.ndarray', assume_sorted: 'bool'=True, *args, **kwargs) -> 'DisSimLocal':
        """ Fit the model using X, neigh_dist, and neigh_ind as training data.

        Parameters
        ----------
        neigh_dist: np.ndarray, shape (n_samples, n_neighbors)
            Distance matrix of training objects (rows) against their
            individual k nearest neighbors (colums).

        neigh_ind: np.ndarray, shape (n_samples, n_neighbors)
            Neighbor indices corresponding to the values in neigh_dist.

        X: np.ndarray, shape (n_samples, n_features)
            Training data, where n_samples is the number of vectors,
            and n_features their dimensionality (number of features).

        assume_sorted: bool, default = True
            Assume input matrices are sorted according to neigh_dist.
            If False, these are sorted here.
        """
        check_consistent_length(neigh_ind, neigh_dist)
        check_consistent_length(neigh_ind.T, neigh_dist.T)
        X = check_array(X)
        try:
            if self.k <= 0:
                raise ValueError(f"Expected k > 0. Got {self.k}")
        except TypeError:
            raise TypeError(f"Expected k: int > 0. Got {self.k}")

        k = self.k
        if k > neigh_ind.shape[1]:
            warnings.warn(f"Neighborhood parameter k larger than provided neighbors in neigh_dist, neigh_ind. Will reduce to k={neigh_ind.shape[1]}.")
            k = neigh_ind.shape[1]
        elif assume_sorted:
            knn = neigh_ind[:, :k]
        else:
            mask = np.argpartition(neigh_dist, kth=(k - 1))[:, :k]
            knn = np.take_along_axis(neigh_ind, mask, axis=1)
        centroids = X[knn].mean(axis=1)
        dist_to_cent = row_norms((X - centroids), squared=True)
        self.X_train_ = X
        self.X_train_centroids_ = centroids
        self.X_train_dist_to_centroids_ = dist_to_cent
        return self

    def transform(self, neigh_dist: 'np.ndarray', neigh_ind: 'np.ndarray', X: 'np.ndarray', assume_sorted: 'bool'=True, *args, **kwargs) -> '(np.ndarray, np.ndarray)':
        """ Transform distance between test and training data with DisSimLocal.

        Parameters
        ----------
        neigh_dist: np.ndarray, shape (n_query, n_neighbors)
            Distance matrix of test objects (rows) against their individual
            k nearest neighbors among the training data (columns).

        neigh_ind: np.ndarray, shape (n_query, n_neighbors)
            Neighbor indices corresponding to the values in neigh_dist

        X: np.ndarray, shape (n_query, n_features)
            Test data, where n_query is the number of vectors,
            and n_features their dimensionality (number of features).

        assume_sorted: ignored

        Returns
        -------
        hub_reduced_dist, neigh_ind
            DisSimLocal distances, and corresponding neighbor indices

        Notes
        -----
        The returned distances are NOT sorted! If you use this class directly,
        you will need to sort the returned matrices according to hub_reduced_dist.
        Classes from :mod:`skhubness.neighbors` do this automatically.
        """
        check_is_fitted(self, ['X_train_', 'X_train_centroids_', 'X_train_dist_to_centroids_'])
        if X is None:
            X = self.X_train_
        else:
            X = check_array(X)
        n_test, n_indexed = neigh_dist.shape
        if n_indexed == 1:
            warnings.warn('Cannot perform hubness reduction with a single neighbor per query. Skipping hubness reduction, and returning untransformed distances.')
            return (
             neigh_dist, neigh_ind)
        k = self.k
        if k > neigh_ind.shape[1]:
            warnings.warn(f"Neighborhood parameter k larger than provided neighbors in neigh_dist, neigh_ind. Will reduce to k={neigh_ind.shape[1]}.")
            k = neigh_ind.shape[1]
        mask = np.argpartition(neigh_dist, kth=(k - 1))
        for i, ind in enumerate(neigh_ind):
            neigh_dist[i, :] = euclidean_distances((X[i].reshape(1, -1)), (self.X_train_[ind]), squared=True)

        neigh_ind = np.take_along_axis(neigh_ind, mask, axis=1)
        knn = neigh_ind[:, :k]
        centroids = self.X_train_centroids_[knn].mean(axis=1)
        X_test = X - centroids
        X_test **= 2
        X_test_dist_to_centroids = X_test.sum(axis=1)
        X_train_dist_to_centroids = self.X_train_dist_to_centroids_[neigh_ind]
        hub_reduced_dist = neigh_dist.copy()
        hub_reduced_dist -= X_test_dist_to_centroids[:, np.newaxis]
        hub_reduced_dist -= X_train_dist_to_centroids
        min_dist = hub_reduced_dist.min()
        if min_dist < 0.0:
            hub_reduced_dist += -min_dist
        if not self.squared:
            hub_reduced_dist **= 0.5
        return (
         hub_reduced_dist, neigh_ind)