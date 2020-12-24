# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/litebo/model/base_model.py
# Compiled at: 2020-04-10 03:57:55
# Size of source mod 2**32: 9723 bytes
import typing, numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import MinMaxScaler
from sklearn.exceptions import NotFittedError

class AbstractModel(object):
    __doc__ = 'Abstract implementation of the Model API.\n\n    **Note:** The input dimensionality of Y for training and the output dimensions\n    of all predictions (also called ``n_objectives``) depends on the concrete\n    implementation of this abstract class.\n\n    Attributes\n    ----------\n    instance_features : np.ndarray(I, K)\n        Contains the K dimensional instance features\n        of the I different instances\n    pca : sklearn.decomposition.PCA\n        Object to perform PCA\n    pca_components : float\n        Number of components to keep or None\n    n_feats : int\n        Number of instance features\n    n_params : int\n        Number of parameters in a configuration (only available after train has\n        been called)\n    scaler : sklearn.preprocessing.MinMaxScaler\n        Object to scale data to be withing [0, 1]\n    var_threshold : float\n        Lower bound vor variance. If estimated variance < var_threshold, the set\n        to var_threshold\n    types : list\n        If set, contains a list with feature types (cat,const) of input vector\n    '

    def __init__(self, types: np.ndarray, bounds: typing.List[typing.Tuple[(float, float)]], instance_features: np.ndarray=None,
                 pca_components: float=None):
        """Constructor

        Parameters
        ----------
        types : np.ndarray (D)
            Specifies the number of categorical values of an input dimension where
            the i-th entry corresponds to the i-th input dimension. Let's say we
            have 2 dimension where the first dimension consists of 3 different
            categorical choices and the second dimension is continuous than we
            have to pass np.array([2, 0]). Note that we count starting from 0.
        bounds : list
            Specifies the bounds for continuous features.
        instance_features : np.ndarray (I, K)
            Contains the K dimensional instance features
            of the I different instances
        pca_components : float
            Number of components to keep when using PCA to reduce
            dimensionality of instance features. Requires to
            set n_feats (> pca_dims).
        """
        self.instance_features = instance_features
        self.pca_components = pca_components
        if instance_features is not None:
            self.n_feats = instance_features.shape[1]
        else:
            self.n_feats = 0
        self.n_params = None
        self.pca = None
        self.scaler = None
        if self.pca_components and self.n_feats > self.pca_components:
            self.pca = PCA(n_components=self.pca_components)
            self.scaler = MinMaxScaler()
        self.var_threshold = 1e-05
        self.bounds = bounds
        self.types = types
        self._initial_types = types.copy()

    def train(self, X: np.ndarray, Y: np.ndarray) -> 'AbstractModel':
        """Trains the Model on X and Y.

        Parameters
        ----------
        X : np.ndarray [n_samples, n_features (config + instance features)]
            Input data points.
        Y : np.ndarray [n_samples, n_objectives]
            The corresponding target values. n_objectives must match the
            number of target names specified in the constructor.

        Returns
        -------
        self : AbstractModel
        """
        self.types = self._initial_types.copy()
        if len(X.shape) != 2:
            raise ValueError('Expected 2d array, got %dd array!' % len(X.shape))
        if X.shape[1] != len(self.types):
            raise ValueError('Feature mismatch: X should have %d features, but has %d' % (X.shape[1], len(self.types)))
        if X.shape[0] != Y.shape[0]:
            raise ValueError('X.shape[0] (%s) != y.shape[0] (%s)' % (X.shape[0], Y.shape[0]))
        self.n_params = X.shape[1] - self.n_feats
        if self.pca and X.shape[0] > self.pca.n_components:
            X_feats = X[:, -self.n_feats:]
            X_feats = self.scaler.fit_transform(X_feats)
            X_feats = np.nan_to_num(X_feats)
            X_feats = self.pca.fit_transform(X_feats)
            X = np.hstack((X[:, :self.n_params], X_feats))
            if hasattr(self, 'types'):
                self.types = np.array(np.hstack((self.types[:self.n_params], np.zeros(X_feats.shape[1]))), dtype=np.uint)
        return self._train(X, Y)

    def _train(self, X: np.ndarray, Y: np.ndarray) -> 'AbstractModel':
        """Trains the random forest on X and y.

        Parameters
        ----------
        X : np.ndarray [n_samples, n_features (config + instance features)]
            Input data points.
        Y : np.ndarray [n_samples, n_objectives]
            The corresponding target values. n_objectives must match the
            number of target names specified in the constructor.

        Returns
        -------
        self
        """
        raise NotImplementedError

    def predict(self, X: np.ndarray) -> typing.Tuple[(np.ndarray, np.ndarray)]:
        """
        Predict means and variances for given X.

        Parameters
        ----------
        X : np.ndarray of shape = [n_samples, n_features (config + instance features)]
            Training samples

        Returns
        -------
        means : np.ndarray of shape = [n_samples, n_objectives]
            Predictive mean
        vars : np.ndarray  of shape = [n_samples, n_objectives]
            Predictive variance
        """
        if len(X.shape) != 2:
            raise ValueError('Expected 2d array, got %dd array!' % len(X.shape))
        if X.shape[1] != len(self._initial_types):
            raise ValueError('Rows in X should have %d entries but have %d!' % (len(self._initial_types), X.shape[1]))
        if self.pca:
            try:
                X_feats = X[:, -self.n_feats:]
                X_feats = self.scaler.transform(X_feats)
                X_feats = self.pca.transform(X_feats)
                X = np.hstack((X[:, :self.n_params], X_feats))
            except NotFittedError:
                pass

        if X.shape[1] != len(self.types):
            raise ValueError('Rows in X should have %d entries but have %d!' % (len(self.types), X.shape[1]))
        mean, var = self._predict(X)
        if len(mean.shape) == 1:
            mean = mean.reshape((-1, 1))
        if len(var.shape) == 1:
            var = var.reshape((-1, 1))
        return (mean, var)

    def _predict(self, X: np.ndarray) -> typing.Tuple[(np.ndarray, np.ndarray)]:
        """
        Predict means and variances for given X.

        Parameters
        ----------
        X : np.ndarray
            [n_samples, n_features (config + instance features)]

        Returns
        -------
        means : np.ndarray of shape = [n_samples, n_objectives]
            Predictive mean
        vars : np.ndarray  of shape = [n_samples, n_objectives]
            Predictive variance
        """
        raise NotImplementedError()

    def predict_marginalized_over_instances(self, X: np.ndarray) -> typing.Tuple[(np.ndarray, np.ndarray)]:
        """Predict mean and variance marginalized over all instances.

        Returns the predictive mean and variance marginalised over all
        instances for a set of configurations.

        Parameters
        ----------
        X : np.ndarray
            [n_samples, n_features (config)]

        Returns
        -------
        means : np.ndarray of shape = [n_samples, 1]
            Predictive mean
        vars : np.ndarray  of shape = [n_samples, 1]
            Predictive variance
        """
        if len(X.shape) != 2:
            raise ValueError('Expected 2d array, got %dd array!' % len(X.shape))
        if X.shape[1] != len(self.types):
            raise ValueError('Rows in X should have %d entries but have %d!' % (len(self.types), X.shape[1]))
        if self.instance_features is None or len(self.instance_features) == 0:
            mean, var = self.predict(X)
            var[var < self.var_threshold] = self.var_threshold
            var[np.isnan(var)] = self.var_threshold
            return (
             mean, var)
        n_instances = len(self.instance_features)
        mean = np.zeros(X.shape[0])
        var = np.zeros(X.shape[0])
        for i, x in enumerate(X):
            X_ = np.hstack((
             np.tile(x, (n_instances, 1)), self.instance_features))
            means, vars = self.predict(X_)
            var_x = np.sum(vars) / len(vars) ** 2
            if var_x < self.var_threshold:
                var_x = self.var_threshold
            var[i] = var_x
            mean[i] = np.mean(means)

        if len(mean.shape) == 1:
            mean = mean.reshape((-1, 1))
        if len(var.shape) == 1:
            var = var.reshape((-1, 1))
        return (mean, var)