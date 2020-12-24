# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/user/feldbauer/PycharmProjects/hubness/skhubness/neighbors/regression.py
# Compiled at: 2019-11-11 04:26:33
# Size of source mod 2**32: 15934 bytes
"""Nearest Neighbor Regression
adapted from https://github.com/scikit-learn/scikit-learn/blob/0.21.X/sklearn/neighbors/regression.py"""
import warnings, numpy as np
from scipy.sparse import issparse
from sklearn.base import RegressorMixin
from sklearn.utils import check_array
from .base import _get_weights, _check_weights, NeighborsBase, KNeighborsMixin
from .base import RadiusNeighborsMixin, SupervisedFloatMixin

class KNeighborsRegressor(NeighborsBase, KNeighborsMixin, SupervisedFloatMixin, RegressorMixin):
    __doc__ = "Regression based on k-nearest neighbors.\n\n    The target is predicted by local interpolation of the targets\n    associated of the nearest neighbors in the training set.\n\n    Read more in the `scikit-learn User Guide <https://scikit-learn.org/stable/modules/neighbors.html#regression>`_.\n\n    Parameters\n    ----------\n    n_neighbors: int, optional (default = 5)\n        Number of neighbors to use by default for :meth:`kneighbors` queries.\n\n    weights: str or callable\n        weight function used in prediction.  Possible values:\n\n        - 'uniform': uniform weights.  All points in each neighborhood\n          are weighted equally.\n        - 'distance': weight points by the inverse of their distance.\n          in this case, closer neighbors of a query point will have a\n          greater influence than neighbors which are further away.\n        - [callable]: a user-defined function which accepts an\n          array of distances, and returns an array of the same shape\n          containing the weights.\n\n        Uniform weights are used by default.\n\n    algorithm : {'auto', 'hnsw', 'lsh', 'falconn_lsh', 'nng', 'rptree', 'ball_tree', 'kd_tree', 'brute'}, optional\n        Algorithm used to compute the nearest neighbors:\n\n        - 'hnsw' will use :class:`HNSW`\n        - 'lsh' will use :class:`PuffinnLSH`\n        - 'falconn_lsh' will use :class:`FalconnLSH`\n        - 'nng' will use :class:`NNG`\n        - 'rptree' will use :class:`RandomProjectionTree`\n        - 'ball_tree' will use :class:`BallTree`\n        - 'kd_tree' will use :class:`KDTree`\n        - 'brute' will use a brute-force search.\n        - 'auto' will attempt to decide the most appropriate exact algorithm\n          based on the values passed to :meth:`fit` method. This will not\n          select an approximate nearest neighbor algorithm.\n\n        Note: fitting on sparse input will override the setting of\n        this parameter, using brute force.\n\n    algorithm_params: dict, optional\n        Override default parameters of the NN algorithm.\n        For example, with algorithm='lsh' and algorithm_params={n_candidates: 100}\n        one hundred approximate neighbors are retrieved with LSH.\n        If parameter hubness is set, the candidate neighbors are further reordered\n        with hubness reduction.\n        Finally, n_neighbors objects are used from the (optionally reordered) candidates.\n\n    hubness: {'mutual_proximity', 'local_scaling', 'dis_sim_local', None}, optional\n        Hubness reduction algorithm\n\n        - 'mutual_proximity' or 'mp' will use :class:`MutualProximity`\n        - 'local_scaling' or 'ls' will use :class:`LocalScaling`\n        - 'dis_sim_local' or 'dsl' will use :class:`DisSimLocal`\n\n        If None, no hubness reduction will be performed (=vanilla kNN).\n\n    hubness_params: dict, optional\n        Override default parameters of the selected hubness reduction algorithm.\n        For example, with hubness='mp' and hubness_params={'method': 'normal'}\n        a mutual proximity variant is used, which models distance distributions\n        with independent Gaussians.\n\n    leaf_size: int, optional (default = 30)\n        Leaf size passed to BallTree or KDTree.  This can affect the\n        speed of the construction and query, as well as the memory\n        required to store the tree.  The optimal value depends on the\n        nature of the problem.\n\n    p: integer, optional (default = 2)\n        Power parameter for the Minkowski metric. When p = 1, this is\n        equivalent to using manhattan_distance (l1), and euclidean_distance\n        (l2) for p = 2. For arbitrary p, minkowski_distance (l_p) is used.\n\n    metric: string or callable, default 'minkowski'\n        the distance metric to use for the tree.  The default metric is\n        minkowski, and with p=2 is equivalent to the standard Euclidean\n        metric. See the documentation of the DistanceMetric class for a\n        list of available metrics.\n\n    metric_params: dict, optional (default = None)\n        Additional keyword arguments for the metric function.\n\n    n_jobs: int or None, optional (default=None)\n        The number of parallel jobs to run for neighbors search.\n        ``None`` means 1 unless in a :obj:`joblib.parallel_backend` context.\n        ``-1`` means using all processors. See scikit-learn\n        `Glossary <https://scikit-learn.org/stable/glossary.html#term-n-jobs>`_\n        for more details.\n        Doesn't affect :meth:`fit` method.\n\n    Examples\n    --------\n    >>> X = [[0], [1], [2], [3]]\n    >>> y = [0, 0, 1, 1]\n    >>> from skhubness.neighbors import KNeighborsRegressor\n    >>> neigh = KNeighborsRegressor(n_neighbors=2)\n    >>> neigh.fit(X, y) # doctest: +ELLIPSIS\n    KNeighborsRegressor(...)\n    >>> print(neigh.predict([[1.5]]))\n    [0.5]\n\n    See also\n    --------\n    NearestNeighbors\n    RadiusNeighborsRegressor\n    KNeighborsClassifier\n    RadiusNeighborsClassifier\n\n    Notes\n    -----\n    See `Nearest Neighbors <https://scikit-learn.org/stable/modules/neighbors.html#neighbors>`_\n    in the scikit-learn online documentation for a discussion\n    of the choice of ``algorithm`` and ``leaf_size``.\n\n    .. warning::\n\n       Regarding the Nearest Neighbors algorithms, if it is found that two\n       neighbors, neighbor `k+1` and `k`, have identical distances but\n       different labels, the results will depend on the ordering of the\n       training data.\n\n    https://en.wikipedia.org/wiki/K-nearest_neighbor_algorithm\n    "

    def __init__(self, n_neighbors=5, weights='uniform', algorithm='auto', algorithm_params=None, hubness=None, hubness_params=None, leaf_size=30, p=2, metric='minkowski', metric_params=None, n_jobs=None, **kwargs):
        (super().__init__)(n_neighbors=n_neighbors, 
         algorithm=algorithm, 
         algorithm_params=algorithm_params, 
         hubness=hubness, 
         hubness_params=hubness_params, 
         leaf_size=leaf_size, 
         metric=metric, p=p, metric_params=metric_params, 
         n_jobs=n_jobs, **kwargs)
        self.weights = _check_weights(weights)

    def predict(self, X):
        """Predict the target for the provided data

        Parameters
        ----------
        X: array-like, shape (n_query, n_features),                 or (n_query, n_indexed) if metric == 'precomputed'
            Test samples.

        Returns
        -------
        y: array of int, shape = [n_samples] or [n_samples, n_outputs]
            Target values
        """
        if issparse(X):
            if self.metric == 'precomputed':
                raise ValueError('Sparse matrices not supported for prediction with precomputed kernels. Densify your matrix.')
        else:
            X = check_array(X, accept_sparse='csr')
            neigh_dist, neigh_ind = self.kneighbors(X)
            weights = _get_weights(neigh_dist, self.weights)
            _y = self._y
            if _y.ndim == 1:
                _y = _y.reshape((-1, 1))
            if weights is None:
                y_pred = np.mean((_y[neigh_ind]), axis=1)
            else:
                y_pred = np.empty((X.shape[0], _y.shape[1]), dtype=(np.float64))
                denom = np.sum(weights, axis=1)
                for j in range(_y.shape[1]):
                    num = np.sum((_y[(neigh_ind, j)] * weights), axis=1)
                    y_pred[:, j] = num / denom

        if self._y.ndim == 1:
            y_pred = y_pred.ravel()
        return y_pred


class RadiusNeighborsRegressor(NeighborsBase, RadiusNeighborsMixin, SupervisedFloatMixin, RegressorMixin):
    __doc__ = "Regression based on neighbors within a fixed radius.\n\n    The target is predicted by local interpolation of the targets\n    associated of the nearest neighbors in the training set.\n\n    Read more in the `scikit-learn User Guide <https://scikit-learn.org/stable/modules/neighbors.html#regression>`_.\n\n    Parameters\n    ----------\n    radius: float, optional (default = 1.0)\n        Range of parameter space to use by default for :meth:`radius_neighbors`\n        queries.\n\n    weights: str or callable\n        weight function used in prediction.  Possible values:\n\n        - 'uniform': uniform weights.  All points in each neighborhood\n          are weighted equally.\n        - 'distance': weight points by the inverse of their distance.\n          in this case, closer neighbors of a query point will have a\n          greater influence than neighbors which are further away.\n        - [callable]: a user-defined function which accepts an\n          array of distances, and returns an array of the same shape\n          containing the weights.\n\n        Uniform weights are used by default.\n\n    algorithm: {'auto', 'falconn_lsh', 'ball_tree', 'kd_tree', 'brute'}, optional\n        Algorithm used to compute the nearest neighbors:\n\n        - 'falconn_lsh' will use :class:`FalconnLSH`\n        - 'ball_tree' will use :class:`BallTree`\n        - 'kd_tree' will use :class:`KDTree`\n        - 'brute' will use a brute-force search.\n        - 'auto' will attempt to decide the most appropriate algorithm\n          based on the values passed to :meth:`fit` method.\n\n        Note: fitting on sparse input will override the setting of\n        this parameter, using brute force.\n\n    algorithm_params: dict, optional\n        Override default parameters of the NN algorithm.\n        For example, with algorithm='lsh' and algorithm_params={n_candidates: 100}\n        one hundred approximate neighbors are retrieved with LSH.\n        If parameter hubness is set, the candidate neighbors are further reordered\n        with hubness reduction.\n        Finally, n_neighbors objects are used from the (optionally reordered) candidates.\n\n    hubness: {'mutual_proximity', 'local_scaling', 'dis_sim_local', None}, optional\n        Hubness reduction algorithm\n\n        - 'mutual_proximity' or 'mp' will use :class:`MutualProximity`\n        - 'local_scaling' or 'ls' will use :class:`LocalScaling`\n        - 'dis_sim_local' or 'dsl' will use :class:`DisSimLocal`\n\n        If None, no hubness reduction will be performed (=vanilla kNN).\n\n    hubness_params: dict, optional\n        Override default parameters of the selected hubness reduction algorithm.\n        For example, with hubness='mp' and hubness_params={'method': 'normal'}\n        a mutual proximity variant is used, which models distance distributions\n        with independent Gaussians.\n\n    leaf_size: int, optional (default = 30)\n        Leaf size passed to BallTree or KDTree.  This can affect the\n        speed of the construction and query, as well as the memory\n        required to store the tree.  The optimal value depends on the\n        nature of the problem.\n\n    p: integer, optional (default = 2)\n        Power parameter for the Minkowski metric. When p = 1, this is\n        equivalent to using manhattan_distance (l1), and euclidean_distance\n        (l2) for p = 2. For arbitrary p, minkowski_distance (l_p) is used.\n\n    metric: string or callable, default 'minkowski'\n        the distance metric to use for the tree.  The default metric is\n        minkowski, and with p=2 is equivalent to the standard Euclidean\n        metric. See the documentation of the DistanceMetric class for a\n        list of available metrics.\n\n    metric_params: dict, optional (default = None)\n        Additional keyword arguments for the metric function.\n\n    n_jobs: int or None, optional (default=None)\n        The number of parallel jobs to run for neighbors search.\n        ``None`` means 1 unless in a :obj:`joblib.parallel_backend` context.\n        ``-1`` means using all processors. See scikit-learn\n        `Glossary <https://scikit-learn.org/stable/glossary.html#term-n-jobs>`_\n        for more details.\n\n    Examples\n    --------\n    >>> X = [[0], [1], [2], [3]]\n    >>> y = [0, 0, 1, 1]\n    >>> from skhubness.neighbors import RadiusNeighborsRegressor\n    >>> neigh = RadiusNeighborsRegressor(radius=1.0)\n    >>> neigh.fit(X, y) # doctest: +ELLIPSIS\n    RadiusNeighborsRegressor(...)\n    >>> print(neigh.predict([[1.5]]))\n    [0.5]\n\n    See also\n    --------\n    NearestNeighbors\n    KNeighborsRegressor\n    KNeighborsClassifier\n    RadiusNeighborsClassifier\n\n    Notes\n    -----\n    See `Nearest Neighbors <https://scikit-learn.org/stable/modules/neighbors.html#neighbors>`_\n    in the scikit-learn online documentation for a discussion\n    of the choice of ``algorithm`` and ``leaf_size``.\n\n    https://en.wikipedia.org/wiki/K-nearest_neighbor_algorithm\n    "

    def __init__(self, radius=1.0, weights='uniform', algorithm='auto', algorithm_params=None, hubness=None, hubness_params=None, leaf_size=30, p=2, metric='minkowski', metric_params=None, n_jobs=None, **kwargs):
        (super().__init__)(radius=radius, 
         algorithm=algorithm, 
         algorithm_params=algorithm_params, 
         hubness=hubness, 
         hubness_params=hubness_params, 
         leaf_size=leaf_size, 
         p=p, 
         metric=metric, metric_params=metric_params, n_jobs=n_jobs, **kwargs)
        self.weights = _check_weights(weights)

    def predict(self, X):
        """Predict the target for the provided data

        Parameters
        ----------
        X: array-like, shape (n_query, n_features), or (n_query, n_indexed) if metric == 'precomputed'
            Test samples.

        Returns
        -------
        y: array of float, shape = [n_samples] or [n_samples, n_outputs]
            Target values
        """
        X = check_array(X, accept_sparse='csr')
        neigh_dist, neigh_ind = self.radius_neighbors(X)
        weights = _get_weights(neigh_dist, self.weights)
        _y = self._y
        if _y.ndim == 1:
            _y = _y.reshape((-1, 1))
        else:
            empty_obs = np.full_like(_y[0], np.nan)
            if weights is None:
                y_pred = np.array([np.mean((_y[ind, :]), axis=0) if len(ind) else empty_obs for i, ind in enumerate(neigh_ind)])
            else:
                y_pred = np.array([np.average((_y[ind, :]), axis=0, weights=(weights[i])) if len(ind) else empty_obs for i, ind in enumerate(neigh_ind)])
        if np.max(np.isnan(y_pred)):
            empty_warning_msg = 'One or more samples have no neighbors within specified radius; predicting NaN.'
            warnings.warn(empty_warning_msg)
        if self._y.ndim == 1:
            y_pred = y_pred.ravel()
        return y_pred