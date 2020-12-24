# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/user/feldbauer/PycharmProjects/hubness/skhubness/neighbors/classification.py
# Compiled at: 2019-11-22 10:10:44
# Size of source mod 2**32: 18557 bytes
"""Nearest Neighbor Classification
adapted from https://github.com/scikit-learn/scikit-learn/blob/0.21.X/sklearn/neighbors/classification.py"""
import numpy as np
from scipy import stats
from sklearn.utils.extmath import weighted_mode
from sklearn.base import ClassifierMixin
from sklearn.utils import check_array
from .base import _check_weights, _get_weights
from .base import NeighborsBase, KNeighborsMixin, RadiusNeighborsMixin, SupervisedIntegerMixin

class KNeighborsClassifier(NeighborsBase, KNeighborsMixin, SupervisedIntegerMixin, ClassifierMixin):
    __doc__ = "Classifier implementing the k-nearest neighbors vote.\n\n    Read more in the `scikit-learn User Guide <https://scikit-learn.org/stable/modules/neighbors.html#classification>`_\n\n    Parameters\n    ----------\n    n_neighbors: int, optional (default = 5)\n        Number of neighbors to use by default for :meth:`kneighbors` queries.\n\n    weights: str or callable, optional (default = 'uniform')\n        weight function used in prediction.  Possible values:\n\n        - 'uniform': uniform weights.  All points in each neighborhood\n          are weighted equally.\n        - 'distance': weight points by the inverse of their distance.\n          in this case, closer neighbors of a query point will have a\n          greater influence than neighbors which are further away.\n        - [callable]: a user-defined function which accepts an\n          array of distances, and returns an array of the same shape\n          containing the weights.\n\n    algorithm : {'auto', 'hnsw', 'lsh', 'falconn_lsh', 'nng', 'rptree', 'ball_tree', 'kd_tree', 'brute'}, optional\n        Algorithm used to compute the nearest neighbors:\n\n        - 'hnsw' will use :class:`HNSW`\n        - 'lsh' will use :class:`PuffinnLSH`\n        - 'falconn_lsh' will use :class:`FalconnLSH`\n        - 'nng' will use :class:`NNG`\n        - 'rptree' will use :class:`RandomProjectionTree`\n        - 'ball_tree' will use :class:`BallTree`\n        - 'kd_tree' will use :class:`KDTree`\n        - 'brute' will use a brute-force search.\n        - 'auto' will attempt to decide the most appropriate exact algorithm\n          based on the values passed to :meth:`fit` method. This will not\n          select an approximate nearest neighbor algorithm.\n\n        Note: fitting on sparse input will override the setting of\n        this parameter, using brute force.\n\n    algorithm_params: dict, optional\n        Override default parameters of the NN algorithm.\n        For example, with algorithm='lsh' and algorithm_params={n_candidates: 100}\n        one hundred approximate neighbors are retrieved with LSH.\n        If parameter hubness is set, the candidate neighbors are further reordered\n        with hubness reduction.\n        Finally, n_neighbors objects are used from the (optionally reordered) candidates.\n\n    hubness: {'mutual_proximity', 'local_scaling', 'dis_sim_local', None}, optional\n        Hubness reduction algorithm\n\n        - 'mutual_proximity' or 'mp' will use :class:`MutualProximity`\n        - 'local_scaling' or 'ls' will use :class:`LocalScaling`\n        - 'dis_sim_local' or 'dsl' will use :class:`DisSimLocal`\n\n        If None, no hubness reduction will be performed (=vanilla kNN).\n\n    hubness_params: dict, optional\n        Override default parameters of the selected hubness reduction algorithm.\n        For example, with hubness='mp' and hubness_params={'method': 'normal'}\n        a mutual proximity variant is used, which models distance distributions\n        with independent Gaussians.\n\n    leaf_size: int, optional (default = 30)\n        Leaf size passed to BallTree or KDTree.  This can affect the\n        speed of the construction and query, as well as the memory\n        required to store the tree.  The optimal value depends on the\n        nature of the problem.\n\n    p: integer, optional (default = 2)\n        Power parameter for the Minkowski metric. When p = 1, this is\n        equivalent to using manhattan_distance (l1), and euclidean_distance\n        (l2) for p = 2. For arbitrary p, minkowski_distance (l_p) is used.\n\n    metric: string or callable, default 'minkowski'\n        the distance metric to use for the tree.  The default metric is\n        minkowski, and with p=2 is equivalent to the standard Euclidean\n        metric. See the documentation of the DistanceMetric class for a\n        list of available metrics.\n\n    metric_params: dict, optional (default = None)\n        Additional keyword arguments for the metric function.\n\n    n_jobs: int or None, optional (default=None)\n        The number of parallel jobs to run for neighbors search.\n        ``None`` means 1 unless in a :obj:`joblib.parallel_backend` context.\n        ``-1`` means using all processors.\n        See `Glossary <https://scikit-learn.org/stable/glossary.html#term-n-jobs>`_ for more details.\n        Doesn't affect :meth:`fit` method.\n\n    Examples\n    --------\n    >>> X = [[0], [1], [2], [3]]\n    >>> y = [0, 0, 1, 1]\n    >>> from skhubness.neighbors import KNeighborsClassifier\n    >>> neigh = KNeighborsClassifier(n_neighbors=3)\n    >>> neigh.fit(X, y) # doctest: +ELLIPSIS\n    KNeighborsClassifier(...)\n    >>> print(neigh.predict([[1.1]]))\n    [0]\n    >>> print(neigh.predict_proba([[0.9]]))\n    [[0.66666667 0.33333333]]\n\n    See also\n    --------\n    RadiusNeighborsClassifier\n    KNeighborsRegressor\n    RadiusNeighborsRegressor\n    NearestNeighbors\n\n    Notes\n    -----\n    See `Nearest Neighbors <https://scikit-learn.org/stable/modules/neighbors.html#neighbors>`_\n    in the scikit-learn online documentation for a discussion\n    of the choice of ``algorithm`` and ``leaf_size``.\n\n    .. warning::\n       Regarding the Nearest Neighbors algorithms, if it is found that two\n       neighbors, neighbor `k+1` and `k`, have identical distances\n       but different labels, the results will depend on the ordering of the\n       training data.\n\n    https://en.wikipedia.org/wiki/K-nearest_neighbor_algorithm\n    "

    def __init__(self, n_neighbors=5, weights='uniform', algorithm='auto', algorithm_params=None, hubness=None, hubness_params=None, leaf_size=30, p=2, metric='minkowski', metric_params=None, n_jobs=None, verbose=0, **kwargs):
        (super().__init__)(n_neighbors=n_neighbors, 
         algorithm=algorithm, 
         algorithm_params=algorithm_params, 
         hubness=hubness, 
         hubness_params=hubness_params, 
         leaf_size=leaf_size, 
         metric=metric, p=p, metric_params=metric_params, 
         n_jobs=n_jobs, 
         verbose=verbose, **kwargs)
        self.weights = _check_weights(weights)

    def predict(self, X):
        """Predict the class labels for the provided data

        Parameters
        ----------
        X: array-like, shape (n_query, n_features),                 or (n_query, n_indexed) if metric == 'precomputed'
            Test samples.

        Returns
        -------
        y: array of shape [n_samples] or [n_samples, n_outputs]
            Class labels for each data sample.
        """
        X = check_array(X, accept_sparse='csr')
        neigh_dist, neigh_ind = self.kneighbors(X)
        classes_ = self.classes_
        _y = self._y
        if not self.outputs_2d_:
            _y = self._y.reshape((-1, 1))
            classes_ = [self.classes_]
        n_outputs = len(classes_)
        n_samples = X.shape[0]
        weights = _get_weights(neigh_dist, self.weights)
        y_pred = np.empty((n_samples, n_outputs), dtype=(classes_[0].dtype))
        for k, classes_k in enumerate(classes_):
            if weights is None:
                mode, _ = stats.mode((_y[(neigh_ind, k)]), axis=1)
            else:
                mode, _ = weighted_mode((_y[(neigh_ind, k)]), weights, axis=1)
            mode = np.asarray((mode.ravel()), dtype=(np.intp))
            y_pred[:, k] = classes_k.take(mode)

        if not self.outputs_2d_:
            y_pred = y_pred.ravel()
        return y_pred

    def predict_proba(self, X):
        """Return probability estimates for the test data X.

        Parameters
        ----------
        X: array-like, shape (n_query, n_features),                 or (n_query, n_indexed) if metric == 'precomputed'
            Test samples.

        Returns
        -------
        p: array of shape = [n_samples, n_classes], or a list of n_outputs
            of such arrays if n_outputs > 1.
            The class probabilities of the input samples. Classes are ordered
            by lexicographic order.
        """
        X = check_array(X, accept_sparse='csr')
        neigh_dist, neigh_ind = self.kneighbors(X)
        classes_ = self.classes_
        _y = self._y
        if not self.outputs_2d_:
            _y = self._y.reshape((-1, 1))
            classes_ = [self.classes_]
        n_samples = X.shape[0]
        weights = _get_weights(neigh_dist, self.weights)
        if weights is None:
            weights = np.ones_like(neigh_ind)
        all_rows = np.arange(X.shape[0])
        probabilities = []
        for k, classes_k in enumerate(classes_):
            pred_labels = _y[:, k][neigh_ind]
            proba_k = np.zeros((n_samples, classes_k.size))
            for i, idx in enumerate(pred_labels.T):
                proba_k[(all_rows, idx)] += weights[:, i]

            normalizer = proba_k.sum(axis=1)[:, np.newaxis]
            normalizer[normalizer == 0.0] = 1.0
            proba_k /= normalizer
            probabilities.append(proba_k)

        if not self.outputs_2d_:
            probabilities = probabilities[0]
        return probabilities


class RadiusNeighborsClassifier(NeighborsBase, RadiusNeighborsMixin, SupervisedIntegerMixin, ClassifierMixin):
    __doc__ = "Classifier implementing a vote among neighbors within a given radius\n\n    Read more in the `scikit-learn User Guide\n    <https://scikit-learn.org/stable/modules/neighbors.html#classification>`_\n\n    Parameters\n    ----------\n    radius: float, optional (default = 1.0)\n        Range of parameter space to use by default for :meth:`radius_neighbors`\n        queries.\n\n    weights: str or callable\n        weight function used in prediction.  Possible values:\n\n        - 'uniform': uniform weights.  All points in each neighborhood\n          are weighted equally.\n        - 'distance': weight points by the inverse of their distance.\n          in this case, closer neighbors of a query point will have a\n          greater influence than neighbors which are further away.\n        - [callable]: a user-defined function which accepts an\n          array of distances, and returns an array of the same shape\n          containing the weights.\n\n        Uniform weights are used by default.\n\n    algorithm: {'auto', 'falconn_lsh', 'ball_tree', 'kd_tree', 'brute'}, optional\n        Algorithm used to compute the nearest neighbors:\n\n        - 'falconn_lsh' will use :class:`FalconnLSH`\n        - 'ball_tree' will use :class:`BallTree`\n        - 'kd_tree' will use :class:`KDTree`\n        - 'brute' will use a brute-force search.\n        - 'auto' will attempt to decide the most appropriate algorithm\n          based on the values passed to :meth:`fit` method.\n\n        Note: fitting on sparse input will override the setting of\n        this parameter, using brute force.\n\n    algorithm_params: dict, optional\n        Override default parameters of the NN algorithm.\n        For example, with algorithm='lsh' and algorithm_params={n_candidates: 100}\n        one hundred approximate neighbors are retrieved with LSH.\n        If parameter hubness is set, the candidate neighbors are further reordered\n        with hubness reduction.\n        Finally, n_neighbors objects are used from the (optionally reordered) candidates.\n\n    hubness: {'mutual_proximity', 'local_scaling', 'dis_sim_local', None}, optional\n        Hubness reduction algorithm\n\n        - 'mutual_proximity' or 'mp' will use :class:`MutualProximity`\n        - 'local_scaling' or 'ls' will use :class:`LocalScaling`\n        - 'dis_sim_local' or 'dsl' will use :class:`DisSimLocal`\n\n        If None, no hubness reduction will be performed (=vanilla kNN).\n\n    hubness_params: dict, optional\n        Override default parameters of the selected hubness reduction algorithm.\n        For example, with hubness='mp' and hubness_params={'method': 'normal'}\n        a mutual proximity variant is used, which models distance distributions\n        with independent Gaussians.\n\n    leaf_size: int, optional (default = 30)\n        Leaf size passed to BallTree or KDTree.  This can affect the\n        speed of the construction and query, as well as the memory\n        required to store the tree.  The optimal value depends on the\n        nature of the problem.\n\n    p: integer, optional (default = 2)\n        Power parameter for the Minkowski metric. When p = 1, this is\n        equivalent to using manhattan_distance (l1), and euclidean_distance\n        (l2) for p = 2. For arbitrary p, minkowski_distance (l_p) is used.\n\n    metric: string or callable, default 'minkowski'\n        the distance metric to use for the tree.  The default metric is\n        minkowski, and with p=2 is equivalent to the standard Euclidean\n        metric. See the documentation of the DistanceMetric class for a\n        list of available metrics.\n\n    outlier_label: int, optional (default = None)\n        Label, which is given for outlier samples (samples with no\n        neighbors on given radius).\n        If set to None, ValueError is raised, when outlier is detected.\n\n    metric_params: dict, optional (default = None)\n        Additional keyword arguments for the metric function.\n\n    n_jobs: int or None, optional (default=None)\n        The number of parallel jobs to run for neighbors search.\n        ``None`` means 1 unless in a :obj:`joblib.parallel_backend` context.\n        ``-1`` means using all processors.\n        See `Glossary <https://scikit-learn.org/stable/glossary.html#term-n-jobs>`_\n        for more details.\n\n    Examples\n    --------\n    >>> X = [[0], [1], [2], [3]]\n    >>> y = [0, 0, 1, 1]\n    >>> from skhubness.neighbors import RadiusNeighborsClassifier\n    >>> neigh = RadiusNeighborsClassifier(radius=1.0)\n    >>> neigh.fit(X, y) # doctest: +ELLIPSIS\n    RadiusNeighborsClassifier(...)\n    >>> print(neigh.predict([[1.5]]))\n    [0]\n\n    See also\n    --------\n    KNeighborsClassifier\n    RadiusNeighborsRegressor\n    KNeighborsRegressor\n    NearestNeighbors\n\n    Notes\n    -----\n    See `Nearest Neighbors <https://scikit-learn.org/stable/modules/neighbors.html#neighbors>`_\n    in the scikit-learn online documentation for a discussion\n    of the choice of ``algorithm`` and ``leaf_size``.\n\n    https://en.wikipedia.org/wiki/K-nearest_neighbor_algorithm\n    "

    def __init__(self, radius=1.0, weights='uniform', algorithm='auto', algorithm_params=None, hubness=None, hubness_params=None, leaf_size=30, p=2, metric='minkowski', outlier_label=None, metric_params=None, n_jobs=None, **kwargs):
        (super().__init__)(radius=radius, 
         algorithm=algorithm, 
         algorithm_params=algorithm_params, 
         hubness=hubness, 
         hubness_params=hubness_params, 
         leaf_size=leaf_size, 
         metric=metric, 
         p=p, metric_params=metric_params, n_jobs=n_jobs, **kwargs)
        self.weights = _check_weights(weights)
        self.outlier_label = outlier_label

    def predict(self, X):
        """Predict the class labels for the provided data

        Parameters
        ----------
        X: array-like, shape (n_query, n_features),                 or (n_query, n_indexed) if metric == 'precomputed'
            Test samples.

        Returns
        -------
        y: array of shape [n_samples] or [n_samples, n_outputs]
            Class labels for each data sample.
        """
        X = check_array(X, accept_sparse='csr')
        n_samples = X.shape[0]
        neigh_dist, neigh_ind = self.radius_neighbors(X)
        inliers = [i for i, nind in enumerate(neigh_ind) if len(nind) != 0]
        outliers = [i for i, nind in enumerate(neigh_ind) if len(nind) == 0]
        classes_ = self.classes_
        _y = self._y
        if not self.outputs_2d_:
            _y = self._y.reshape((-1, 1))
            classes_ = [self.classes_]
        n_outputs = len(classes_)
        if self.outlier_label is not None:
            neigh_dist[outliers] = 1e-06
        else:
            if outliers:
                raise ValueError('No neighbors found for test samples %r, you can try using larger radius, give a label for outliers, or consider removing them from your dataset.' % outliers)
            else:
                weights = _get_weights(neigh_dist, self.weights)
                y_pred = np.empty((n_samples, n_outputs), dtype=(classes_[0].dtype))
                for k, classes_k in enumerate(classes_):
                    pred_labels = np.zeros((len(neigh_ind)), dtype=object)
                    pred_labels[:] = [_y[(ind, k)] for ind in neigh_ind]
                    if weights is None:
                        mode = np.array([stats.mode(pl)[0] for pl in pred_labels[inliers]],
                          dtype=(np.int))
                    else:
                        mode = np.array([weighted_mode(pl, w)[0] for pl, w in zip(pred_labels[inliers], weights[inliers])],
                          dtype=(np.int))
                    mode = mode.ravel()
                    y_pred[(inliers, k)] = classes_k.take(mode)

                if outliers:
                    y_pred[outliers, :] = self.outlier_label
                y_pred = self.outputs_2d_ or y_pred.ravel()
            return y_pred