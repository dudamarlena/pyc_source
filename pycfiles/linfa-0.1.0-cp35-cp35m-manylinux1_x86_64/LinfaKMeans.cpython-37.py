# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/luca/Documents/code/linfa-python/linfa/LinfaKMeans.py
# Compiled at: 2019-11-18 17:28:19
# Size of source mod 2**32: 5979 bytes
from sklearn.base import BaseEstimator, ClusterMixin, TransformerMixin
from sklearn.utils.validation import check_is_fitted
from sklearn.metrics.pairwise import euclidean_distances, pairwise_distances_argmin_min
from sklearn.utils.extmath import row_norms
import numpy as np
from .linfa import WrappedKMeans

class KMeans(BaseEstimator, ClusterMixin, TransformerMixin):
    __doc__ = "K-Means clustering using a Rust's `linfa` crate.\n    Parameters\n    ----------\n    n_clusters : int, optional, default: 8\n        The number of clusters to form as well as the number of\n        centroids to generate.\n    max_iter : int, default: 300\n        Maximum number of iterations of the k-means algorithm for a\n        single run.\n    tol : float, default: 1e-4\n        Relative tolerance with regards to inertia to declare convergence\n    random_state : int or None (default)\n        Determines random number generation for centroid initialization. Use\n        an int to make the randomness deterministic.\n        See :term:`Glossary <random_state>`.\n    Attributes\n    ----------\n    cluster_centers_ : array, [n_clusters, n_features]\n        Coordinates of cluster centers.\n    Examples\n    --------\n    >>> from linfa import KMeans\n    >>> import numpy as np\n    >>> X = np.array([[1, 2], [1, 4], [1, 0],\n    ...               [10, 2], [10, 4], [10, 0]])\n    >>> kmeans = KMeans(n_clusters=2, random_state=0).fit(X)\n    >>> kmeans.predict([[0, 0], [12, 3]])\n    array([1, 0], dtype=int32)\n    >>> kmeans.cluster_centers_\n    array([[10.,  2.],\n           [ 1.,  2.]])\n    "

    def __init__(self, n_clusters=8, max_iter=300, tol=0.0001, random_state=None):
        self.model_ = WrappedKMeans(n_clusters, random_state, tol, max_iter)
        self.cluster_centers_ = None

    def fit(self, X, y=None):
        """Compute k-means clustering.
        Parameters
        ----------
        X : NumPy array, shape=(n_samples, n_features)
            Training instances to cluster.
        y : Ignored
            not used, present here for API consistency by convention.
        """
        self.model_.fit(X)
        self.cluster_centers_ = self.model_.centroids()
        return self

    def fit_predict(self, X, y=None):
        """Compute cluster centers and predict cluster index for each sample.
        Convenience method; equivalent to calling fit(X) followed by
        predict(X).
        Parameters
        ----------
        X : NumPy array, shape=(n_samples, n_features)
            Training instances to cluster.
        y : Ignored
            not used, present here for API consistency by convention.
        Returns
        -------
        labels : array, shape [n_samples,]
            Index of the cluster each sample belongs to.
        """
        return self.fit(X).predict(X)

    def fit_transform(self, X, y=None):
        """Compute clustering and transform X to cluster-distance space.
        Equivalent to fit(X).transform(X), but more efficiently implemented.
        Parameters
        ----------
        X : NumPy array, shape=(n_samples, n_features)
            Training instances to cluster.
        y : Ignored
            not used, present here for API consistency by convention.
        Returns
        -------
        X_new : array, shape [n_samples, k]
            X transformed in the new space.
        """
        return self.fit(X)._transform(X)

    def transform(self, X):
        """Transform X to a cluster-distance space.
        In the new space, each dimension is the distance to the cluster
        centers.
        Parameters
        ----------
        X : NumPy array, shape=(n_samples, n_features)
            Training instances to cluster.
        Returns
        -------
        X_new : array, shape [n_samples, k]
            X transformed in the new space.
        """
        check_is_fitted(self, 'cluster_centers_')
        return self._transform(X)

    def _transform(self, X):
        """guts of transform method; no input validation"""
        return self.model_.predict(X)

    def predict(self, X):
        """Predict the closest cluster each sample in X belongs to.
        In the vector quantization literature, `cluster_centers_` is called
        the code book and each value returned by `predict` is the index of
        the closest code in the code book.
        Parameters
        ----------
        X : NumPy array, shape=(n_samples, n_features)
            Training instances to cluster.
        Returns
        -------
        labels : array, shape [n_samples,]
            Index of the cluster each sample belongs to.
        """
        check_is_fitted(self, 'cluster_centers_')
        return self.model_.predict(X)

    def save(self, path):
        self.model_.save(path)

    @classmethod
    def load(cls, path):
        model_ = WrappedKMeans.load(path)
        cluster_centers_ = model_.centroids()
        model = super().__new__(cls)
        model.model_ = model_
        model.cluster_centers_ = cluster_centers_
        return model

    def score(self, X, y=None):
        """Opposite of the value of X on the K-means objective.
        Parameters
        ----------
        X : {array-like, sparse matrix}, shape = [n_samples, n_features]
            New data.
        y : Ignored
            not used, present here for API consistency by convention.
        Returns
        -------
        score : float
            Opposite of the value of X on the K-means objective.
        """
        check_is_fitted(self, 'cluster_centers_')
        x_squared_norms = row_norms(X, squared=True)
        return -_labels_inertia(X, x_squared_norms, self.cluster_centers_)[1]


def _labels_inertia(X, x_squared_norms, centers):
    labels, distances = pairwise_distances_argmin_min(X=X,
      Y=centers,
      metric='euclidean',
      metric_kwargs={'squared': True})
    labels = labels.astype((np.int32), copy=False)
    inertia = distances.sum()
    return (labels, inertia)