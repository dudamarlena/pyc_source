# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/tom/.local/miniconda/lib/python3.6/site-packages/alphacsc/other/k_medoids.py
# Compiled at: 2019-06-04 04:10:26
# Size of source mod 2**32: 11533 bytes
__doc__ = 'K-medoids clustering\n\nTaken from https://github.com/scikit-learn/scikit-learn/pull/7694\n\n'
import warnings, numpy as np
from sklearn.base import BaseEstimator, ClusterMixin, TransformerMixin
from sklearn.metrics.pairwise import pairwise_distances
from sklearn.utils import check_array, check_random_state
from sklearn.utils.validation import check_is_fitted

class KMedoids(BaseEstimator, ClusterMixin, TransformerMixin):
    """KMedoids"""

    def __init__(self, n_clusters=8, distance_metric='euclidean', init='heuristic', max_iter=300, random_state=None):
        self.n_clusters = n_clusters
        self.distance_metric = distance_metric
        self.init = init
        self.max_iter = max_iter
        self.random_state = random_state

    def _check_init_args(self):
        """Validates the input arguments. """
        if self.n_clusters is None or self.n_clusters <= 0 or not isinstance(self.n_clusters, (int, np.integer)):
            raise ValueError('n_clusters should be a nonnegative integer. %s was given' % self.n_clusters)
        else:
            init_methods = [
             'random', 'heuristic']
            if isinstance(self.init, str):
                if self.init not in init_methods:
                    raise ValueError('init needs to be one of the following: ' + '%s' % init_methods)
            if isinstance(self.init, np.ndarray):
                assert self.init.size == self.n_clusters
        self.random_state_ = check_random_state(self.random_state)

    def fit(self, X, y=None):
        """Fit K-Medoids to the provided data.

        Parameters
        ----------
        X : {array-like, sparse matrix}, shape=(n_samples, n_features).
            Dataset to cluster.

        Returns
        -------
        self
        """
        self._check_init_args()
        X = check_array(X, accept_sparse=['csr', 'csc'])
        if self.n_clusters > X.shape[0]:
            raise ValueError('The number of medoids %d must be less than the number of samples %d.' % (
             self.n_clusters, X.shape[0]))
        else:
            if callable(self.distance_metric):
                distances = self.distance_metric(X)
            else:
                distances = pairwise_distances(X, metric=(self.distance_metric))
            medoid_idxs = self._get_initial_medoid_indices(distances, self.n_clusters)
            if distances is not None:
                this = distances[medoid_idxs, :]
            else:
                this = self.distance_metric(X, np.atleast_2d(X[medoid_idxs])).T
        labels = np.argmin(this, axis=0)
        old_medoid_idxs = np.zeros((self.n_clusters,))
        self.n_iter_ = 0
        while not np.all(old_medoid_idxs == medoid_idxs) and self.n_iter_ < self.max_iter:
            self.n_iter_ += 1
            old_medoid_idxs = np.copy(medoid_idxs)
            if distances is not None:
                this = distances[medoid_idxs, :]
            else:
                this = self.distance_metric(X, np.atleast_2d(X[medoid_idxs])).T
            labels = np.argmin(this, axis=0)
            self._update_medoid_idxs_in_place(X, distances, labels, medoid_idxs)

        self.labels_ = labels
        self.medoid_idxs_ = medoid_idxs
        self.cluster_centers_ = X[medoid_idxs]
        self.inertia_ = self._compute_inertia(X)
        return self

    def _update_medoid_idxs_in_place(self, X, distances, cluster_idxs, medoid_idxs):
        """In-place update of the medoid indices"""
        for k in range(self.n_clusters):
            if sum(cluster_idxs == k) == 0:
                warnings.warn('Cluster %d is empty!' % k)
            else:
                cluster_k_idxs = np.where(cluster_idxs == k)[0]
                if distances is not None:
                    in_cluster_distances = distances[np.ix_(cluster_k_idxs, cluster_k_idxs)]
                else:
                    in_cluster_distances = self.distance_metric(np.atleast_2d(X[cluster_k_idxs]))
                in_cluster_all_costs = np.sum(in_cluster_distances, axis=1)
                min_cost_idx = np.argmin(in_cluster_all_costs)
                min_cost = in_cluster_all_costs[min_cost_idx]
                if distances is not None:
                    curr_cost = np.sum(distances[(medoid_idxs[k], cluster_k_idxs)])
                else:
                    curr_cost = np.sum(self.distance_metric(np.atleast_2d(X[cluster_k_idxs]), np.atleast_2d(X[medoid_idxs[k]])).T)
                if min_cost < curr_cost:
                    medoid_idxs[k] = cluster_k_idxs[min_cost_idx]

    def transform(self, X):
        """Transforms X to cluster-distance space.

        Parameters
        ----------
        X : {array-like, sparse matrix}, shape=(n_samples, n_features)
            Data to transform.

        Returns
        -------
        X_new : {array-like, sparse matrix}, shape=(n_samples, n_clusters)
            X transformed in the new space of distances to cluster centers.
        """
        X = check_array(X, accept_sparse=['csr', 'csc'])
        check_is_fitted(self, 'cluster_centers_')
        if callable(self.distance_metric):
            return self.distance_metric(X, Y=(self.cluster_centers_))
        else:
            return pairwise_distances(X, Y=(self.cluster_centers_), metric=(self.distance_metric))

    def predict(self, X):
        """Predict the closest cluster for each sample in X

        Parameters
        ----------
        X : {array-like, sparse matrix}, shape = [n_samples, n_features]
            New data to predict.

        Returns
        -------
        labels : array, shape [n_samples,]
            Index of the cluster each sample belongs to.
        """
        check_is_fitted(self, 'cluster_centers_')
        X = check_array(X, accept_sparse=['csr', 'csc'])
        if callable(self.distance_metric):
            distances = self.distance_metric(X, Y=(self.cluster_centers_))
        else:
            distances = pairwise_distances(X, Y=(self.cluster_centers_), metric=(self.distance_metric))
        labels = np.argmin(distances, axis=1)
        return labels

    def _compute_inertia(self, X):
        """Compute inertia of new samples. Inertia is defined as the sum of the
        sample distances to closest cluster centers.

        Parameters
        ----------
        X : {array-like, sparse matrix}, shape=(n_samples, n_features)
            Samples to compute inertia for.

        Returns
        -------
        Sum of sample distances to closest cluster centers.
        """
        distances = self.transform(X)
        inertia = np.sum(np.min(distances, axis=1))
        return inertia

    def _get_initial_medoid_indices(self, distances, n_clusters):
        """Select initial medoids randomly or heuristically"""
        if isinstance(self.init, str):
            if self.init == 'random':
                medoids = self.random_state_.permutation(distances.shape[0])[:n_clusters]
        elif isinstance(self.init, str):
            if self.init == 'heuristic':
                medoids = list(np.argsort(np.sum(distances, axis=1))[:n_clusters])
        else:
            if isinstance(self.init, np.ndarray):
                medoids = self.init
            else:
                raise ValueError("Initialization not implemented for method: '%s'" % self.init)
        return medoids