# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/odin/ml/decompositions.py
# Compiled at: 2019-08-13 03:43:57
# Size of source mod 2**32: 39427 bytes
from __future__ import absolute_import, division, print_function
import math
from multiprocessing import Array, Value
from numbers import Number
import numpy as np
from scipy import linalg
from six import string_types
from sklearn.decomposition import PCA, IncrementalPCA
from sklearn.utils import as_float_array, check_array, check_random_state, gen_batches
from sklearn.utils.extmath import _incremental_mean_and_var, randomized_svd, svd_flip
from sklearn.utils.validation import check_is_fitted
from odin.ml.base import BaseEstimator, TransformerMixin
from odin.utils import Progbar, batching, ctext, flatten_list
from odin.utils.mpi import MPI
__all__ = [
 'fast_pca',
 'MiniBatchPCA',
 'PPCA',
 'SupervisedPPCA']

def fast_pca(*x, n_components=None, algo='rpca', y=None, batch_size=1024, return_model=False, random_state=1234):
    """ A shortcut for many different PCA algorithms

  Parameters
  ----------
  x : {list, tuple}
    list of matrices for transformation, the first matrix will
    be used for training
  n_components : {None, int}
    number of PCA components
  algo : {'pca', 'ipca', 'ppca', 'sppca', 'plda', 'rpca'}
    different PCA algorithm:
      'ipca' - IncrementalPCA,
      'ppca' - Probabilistic PCA,
      'sppca' - Supervised Probabilistic PCA,
      'plda' - Probabilistic LDA,
      'rpca' - randomized PCA using randomized SVD
  y : {numpy.ndarray, None}
    required for labels in case of `sppca`
  batch_size : int (default: 1024)
    batch size, only used for IncrementalPCA
  return_model : bool (default: False)
    if True, return the trained PCA model as the FIRST return
  """
    batch_size = int(batch_size)
    algo = str(algo).lower()
    if algo not in ('pca', 'ipca', 'ppca', 'sppca', 'plda', 'rpca'):
        raise ValueError("`algo` must be one of the following: 'pca', 'ppca', 'plda', 'sppca', or 'rpca'; but given: '%s'" % algo)
    if algo in ('sppca', 'plda'):
        if y is None:
            raise RuntimeError("`y` must be not None if `algo='sppca'`")
    x = flatten_list(x, level=None)
    x_train = x[0]
    x_test = x[1:]
    input_shape = None
    if x_train.ndim > 2:
        input_shape = (-1, ) + x_train.shape[1:]
        new_shape = (-1, np.prod(input_shape[1:]))
        x_train = np.reshape(x_train, new_shape)
        x_test = [np.reshape(x, new_shape) for x in x_test]
        if n_components is not None:
            input_shape = None
    if algo == 'sppca':
        pca = SupervisedPPCA(n_components=n_components, random_state=random_state)
        pca.fit(x_train, y)
    else:
        if algo == 'plda':
            from odin.ml import PLDA
            pca = PLDA(n_phi=n_components, random_state=random_state)
            pca.fit(x_train, y)
        else:
            if algo == 'pca':
                pca = PCA(n_components=n_components, random_state=random_state)
                pca.fit(x_train)
            else:
                if algo == 'rpca':
                    pca = RandomizedPCA(n_components=n_components, iterated_power=2, random_state=random_state)
                    pca.fit(x_train)
                else:
                    if algo == 'ipca':
                        pca = IncrementalPCA(n_components=n_components, batch_size=batch_size)
                        prog = Progbar(target=(x_train.shape[0]), print_report=False,
                          print_summary=False,
                          name='Fitting PCA')
                        for start, end in batching(batch_size=batch_size, n=(x_train.shape[0]), seed=1234):
                            pca.partial_fit((x_train[start:end]), check_input=False)
                            prog.add(end - start)

                    else:
                        if algo == 'ppca':
                            pca = PPCA(n_components=n_components, random_state=random_state)
                            pca.fit(x_train)
    x_train = pca.transform(x_train)
    x_test = [pca.transform(x) for x in x_test]
    if input_shape is not None:
        x_train = np.reshape(x_train, input_shape)
        x_test = [np.reshape(x, input_shape) for x in x_test]
    if len(x_test) == 0:
        if not return_model:
            return x_train
        return (pca, x_train)
    else:
        if not return_model:
            return tuple([x_train] + x_test)
        return tuple([pca, x_train] + x_test)


class PPCA(BaseEstimator, TransformerMixin):
    __doc__ = ' Probabilistic Principal Components Analysis\n\n  (C) Copyright University of Eastern Finland (UEF).\n  Ville Vestman, ville.vestman@uef.fi,\n  Tomi Kinnunen, tkinnu@cs.uef.fi.\n\n  Parameters\n  ----------\n  n_components : {int, None}\n    if None, keep the same dimensions as input features\n  bias : {vector, \'auto\'} [feat_dim,]\n    if \'auto\' take mean of training data\n  n_iter : {integer, \'auto\'}\n    if \'auto\', keep iterating until no more improvement (i.e. reduction in `sigma` value)\n    compared to the `improve_threshold`\n  improve_threshold : scalar\n    Only used in case `n_iter=\'auto\'`\n  solver : {\'traditional\', \'simple\'}\n  verbose: {0, 1}\n    showing logging information during fitting\n  random_state : {None, integer, numpy.random.RandomState}\n\n  Attributes\n  ----------\n  V_ : [feat_dim, n_components]\n    total variability matrix\n  bias_ : [feat_dim]\n    bias vector\n  sigma_ : scalar\n    variance of error term\n\n  References\n  ----------\n  [1] Ville Vestman and Tomi Kinnunen, "Supervector Compression\n  Strategies to Speed up i-vector System Development",\n  submitted to Speaker Odyssey 2018.\n\n  '

    def __init__(self, n_components=None, bias='auto', n_iter='auto', improve_threshold=0.001, solver='traditional', verbose=0, random_state=None):
        super(PPCA, self).__init__()
        if isinstance(n_components, Number):
            assert n_components > 0, '`n_components` must be greater than 0, but given: %d' % n_components
            n_components = int(n_components)
        else:
            if n_components is not None:
                raise ValueError('`n_components` can be None or integer')
            self.n_components_ = n_components
            if isinstance(bias, string_types):
                bias = bias.strip().lower()
                assert bias == 'auto', 'Invalid value for `bias`: %s' % bias
            elif not isinstance(bias, (np.ndarray, Number)):
                raise ValueError("`bias` can be 'auto', numpy.ndarray or a number")
        self.bias_ = bias
        if solver not in ('traditional', 'simple'):
            raise ValueError("`solver` must be: 'traditional', or 'simple'")
        else:
            self.solver_ = solver
            if isinstance(n_iter, string_types):
                n_iter = n_iter.lower()
                assert n_iter == 'auto', 'Invalid `n_iter` value: %s' % n_iter
            elif isinstance(n_iter, Number):
                assert n_iter > 0, '`n_iter` must greater than 0, but given: %d' % n_iter
            else:
                self.n_iter_ = n_iter
                if random_state is None:
                    rand = np.random.RandomState(seed=None)
                else:
                    if isinstance(random_state, Number):
                        rand = np.random.RandomState(seed=None)
                    else:
                        if isinstance(random_state, np.random.RandomState):
                            rand = random_state
                        else:
                            raise ValueError('No suppport for `random_state` value: %s' % str(random_state))
        self.random_state_ = rand
        self.improve_threshold_ = float(improve_threshold)
        self.feat_dim_ = None
        self.verbose_ = int(verbose)

    def fit(self, X, y=None):
        num_samples, feat_dim = X.shape
        n_components = feat_dim if self.n_components_ is None else self.n_components_
        if self.bias_ == 'auto':
            bias = np.mean(X, 0)
        else:
            if isinstance(self.bias_, Number):
                bias = np.full(shape=(feat_dim,), fill_value=(self.bias_))
            else:
                bias = self.bias_
        assert bias.shape == (feat_dim,), 'Invialid `bias` given shape: %s, require shape: %s' % (str(bias.shape), str((feat_dim,)))
        V = self.random_state_.rand(feat_dim, n_components)
        last_sigma = None
        sigma = 1
        centeredM = X - bias[np.newaxis, :]
        varianceM = np.sum(centeredM ** 2) / (num_samples * feat_dim)
        if self.verbose_:
            print('[PPCA]n_components: %d  n_sample: %d  feat_dim: %d  n_iter: %d  threshold: %f  solver: %s' % (
             n_components, num_samples, feat_dim,
             -1 if self.n_iter_ == 'auto' else self.n_iter_, self.improve_threshold_, self.solver_))
        curr_n_iter = 0
        while 1:
            B = (V * 1 / sigma).T
            Sigma = np.linalg.inv(np.eye(n_components) + np.dot(B, V))
            my = np.dot(np.dot(Sigma, B), centeredM.T)
            if self.solver_ == 'traditional':
                sumEmm = num_samples * Sigma + np.dot(my, my.T)
            else:
                if self.solver_ == 'simple':
                    sumEmm = np.dot(my, my.T)
            sumEmmInv = np.linalg.inv(sumEmm)
            V = np.dot(np.dot(centeredM.T, my.T), sumEmmInv)
            last_sigma = sigma
            sigma = varianceM - np.sum(sumEmm * np.dot(V.T, V)) / (feat_dim * num_samples)
            improvement = last_sigma - sigma
            if self.verbose_ > 0:
                print('Iteration: %d   sigma: %.3f   improvement: %.3f' % (curr_n_iter, sigma, improvement))
            curr_n_iter += 1
            if isinstance(self.n_iter_, Number):
                if curr_n_iter >= self.n_iter_:
                    break
                else:
                    if curr_n_iter > 1:
                        if improvement < self.improve_threshold_:
                            break

        self.feat_dim_ = feat_dim
        self.n_components_ = n_components
        self.V_ = V
        self.bias_ = bias
        self.sigma_ = sigma
        B = (V * 1 / sigma).T
        Sigma = np.linalg.inv(np.eye(n_components) + np.dot(B, V))
        self.extractorMatrix_ = np.dot(Sigma, B)

    def transform(self, X):
        """
    Parameters
    ----------
    X : matrix [num_samples, feat_dim]
    """
        if not hasattr(self, 'extractorMatrix_'):
            raise AssertionError("The model hasn't `fit` on data")
        elif not X.shape[1] == self.feat_dim_:
            raise AssertionError('Expect input matrix with shape: [?, %d], but give: %s' % (self.feat_dim_, str(X.shape)))
        ivec = np.dot(self.extractorMatrix_, (X - self.bias_[np.newaxis, :]).T)
        return ivec.T


class SupervisedPPCA(PPCA):
    __doc__ = " Supervised Probabilistic Principal Components Analysis\n\n  (C) Copyright University of Eastern Finland (UEF).\n  Ville Vestman, ville.vestman@uef.fi,\n  Tomi Kinnunen, tkinnu@cs.uef.fi.\n\n  Parameters\n  ----------\n  n_components : {int, None}\n    if None, keep the same dimensions as input features\n  bias : {vector, 'auto'} [feat_dim,]\n    if 'auto' take mean of training data\n  beta : scalar (default: 1)\n    a weight parameter (use beta = 1 as default)\n  n_iter : {integer, 'auto'}\n    if 'auto', keep iterating until no more improvement (i.e. reduction in `sigma` value)\n    compared to the `improve_threshold`\n  improve_threshold : scalar\n    Only used in case `n_iter='auto'`\n  solver : {'traditional', 'simple'}\n  extractor : {'supervised', 'unsupervised'}\n    'supervised' is the probabilistic partial least squares extractor using\n    both unsupervised and supervised information\n  verbose: {0, 1}\n    showing logging information during fitting\n  random_state : {None, integer, numpy.random.RandomState}\n\n  Attributes\n  ----------\n  V_ : [feat_dim, n_components]\n    total variability matrix\n  Q_ : [feat_dim, n_components]\n    matrix for mapping speaker-dependent supervectors to i-vectors\n  sigma_ : scalar\n    variance of error term\n  rho_ : scalar\n    variance of error term in speaker-dependent supervector model\n  bias_ : [feat_dim,]\n    bias vector\n  classBias_ : [feat_dim,]\n    mean of speaker-dependent supervectors\n\n  "

    def __init__(self, n_components=None, bias='auto', beta=1, n_iter='auto', improve_threshold=0.001, solver='traditional', extractor='supervised', verbose=0, random_state=None):
        super(SupervisedPPCA, self).__init__(n_components=n_components, bias=bias, n_iter=n_iter,
          solver=solver,
          improve_threshold=improve_threshold,
          verbose=verbose,
          random_state=random_state)
        self.beta_ = float(beta)
        extractor = str(extractor).lower()
        if extractor not in ('supervised', 'unsupervised'):
            raise ValueError("`extractor` can only be: 'unsupervised' or 'supervised'")
        self.extractor_ = extractor

    def fit(self, X, y, z=None):
        """
    Parameters
    ----------
    X : matrix [num_samples, feat_dim]
    y : vector (int) [num_samples,]
    z : matrix [num_classes, feat_dim]
      class-dependent feature vectors for each class from 0 to `num_classes - 1`
      (in this order).
    """
        num_samples, feat_dim = X.shape
        num_classes = z.shape[0] if z is not None else len(np.unique(y))
        n_components = feat_dim if self.n_components_ is None else self.n_components_
        if self.bias_ == 'auto':
            bias = np.mean(X, 0)
        else:
            if isinstance(self.bias_, Number):
                bias = np.full(shape=(feat_dim,), fill_value=(self.bias_))
            else:
                bias = self.bias_
                assert bias.shape == (feat_dim,), 'Invialid `bias` given shape: %s, require shape: %s' % (str(bias.shape), str((feat_dim,)))
                y = y.ravel().astype('int32')
                assert y.shape[0] == num_samples, 'Number of samples incosistent in `X`(%s) and `y`(%s)' % (str(X.shape), str(y.shape))
            if z is None:
                z = np.empty(shape=(max(np.max(y) + 1, num_classes), feat_dim), dtype=(X.dtype))
                for i in np.unique(y):
                    z[i, :] = np.mean((X[(y == i)]), axis=0, keepdims=True)

            elif not z.shape[0] == num_classes:
                raise AssertionError
        assert z.shape[1] == feat_dim
        V = self.random_state_.rand(feat_dim, n_components)
        Q = self.random_state_.rand(feat_dim, n_components)
        last_sigma = None
        sigma = 1
        last_rho = None
        rho = 1
        centeredM = X - bias[np.newaxis, :]
        varianceM = np.sum(centeredM ** 2) / (num_samples * feat_dim)
        centeredY = z[y]
        classBias = np.mean(centeredY, 0)
        centeredY = centeredY - classBias[np.newaxis, :]
        varianceY = np.sum(centeredY ** 2) / (num_samples * feat_dim)
        if self.verbose_:
            print('[S-PPCA]n_components: %d  n_sample: %d  feat_dim: %d  n_iter: %d  threshold: %f  solver: %s' % (
             n_components, num_samples, feat_dim,
             -1 if self.n_iter_ == 'auto' else self.n_iter_, self.improve_threshold_, self.solver_))
        curr_n_iter = 0
        while 1:
            B = (V * 1 / sigma).T
            C = (Q * self.beta_ * 1 / rho).T
            Sigma = np.linalg.inv(np.eye(n_components) + np.dot(B, V) + np.dot(C, Q))
            my = np.dot(Sigma, np.dot(B, centeredM.T) + np.dot(C, centeredY.T))
            if self.solver_ == 'traditional':
                sumEmm = num_samples * Sigma + np.dot(my, my.T)
            else:
                if self.solver_ == 'simple':
                    sumEmm = np.dot(my, my.T)
            sumEmmInv = np.linalg.inv(sumEmm)
            V = np.dot(np.dot(centeredM.T, my.T), sumEmmInv)
            Q = np.dot(np.dot(centeredY.T, my.T), sumEmmInv)
            last_sigma = sigma
            sigma = varianceM - np.sum(sumEmm * np.dot(V.T, V)) / (feat_dim * num_samples)
            improvement_sigma = last_sigma - sigma
            last_rho = rho
            rho = varianceY - np.sum(sumEmm * np.dot(Q.T, Q)) / (feat_dim * num_samples)
            improvement_rho = last_rho - rho
            if self.verbose_ > 0:
                print('Iteration: %d   sigma: %.3f   rho: %.3f    improvement: %.3f:%.3f' % (
                 curr_n_iter, sigma, rho, improvement_sigma, improvement_rho))
            curr_n_iter += 1
            if isinstance(self.n_iter_, Number):
                if curr_n_iter >= self.n_iter_:
                    break
                else:
                    if curr_n_iter > 1:
                        if improvement_sigma < self.improve_threshold_:
                            if improvement_rho < self.improve_threshold_:
                                break

        self.feat_dim_ = feat_dim
        self.n_components_ = n_components
        self.num_classes_ = num_classes
        self.V_ = V
        self.Q_ = Q
        self.bias_ = bias
        self.classBias_ = classBias
        self.sigma_ = sigma
        self.rho_ = rho
        B = (V * 1 / sigma).T
        Sigma = np.linalg.inv(np.eye(n_components) + np.dot(B, V))
        self.extractorMatrix_ = np.dot(Sigma, B)
        A = np.concatenate([V, Q], axis=0)
        B = np.concatenate([(V * 1 / sigma).T, (Q * 1 / rho).T], axis=(-1))
        sigmaW = np.linalg.inv(np.eye(n_components) + np.dot(B, A))
        self.extractorMatrixPPLS_ = np.dot(sigmaW, B)
        C = np.dot(V.T, V) + sigma * np.eye(n_components)
        self.labelMatrix_ = np.dot(Q, np.linalg.solve(C, V.T))

    def transform(self, X):
        if self.extractor_ == 'unsupervised':
            return super(SupervisedPPCA, self).transform(X)
        else:
            centeredM = X - self.bias_[np.newaxis, :]
            labels = np.dot(self.labelMatrix_, centeredM.T) + self.classBias_[:, np.newaxis]
            ivec = np.dot(self.extractorMatrixPPLS_, np.concatenate([X.T, labels], axis=0) - np.concatenate([self.bias_, self.classBias_])[:, np.newaxis])
            return ivec.T


class RandomizedPCA(BaseEstimator, TransformerMixin):
    __doc__ = 'Principal component analysis (PCA) using randomized SVD\n\n  Linear dimensionality reduction using approximated Singular Value\n  Decomposition of the data and keeping only the most significant\n  singular vectors to project the data to a lower dimensional space.\n\n  Parameters\n  ----------\n  n_components : int, optional\n      Maximum number of components to keep. When not given or None, this\n      is set to n_features (the second dimension of the training data).\n\n  copy : bool\n      If False, data passed to fit are overwritten and running\n      fit(X).transform(X) will not yield the expected results,\n      use fit_transform(X) instead.\n\n  iterated_power : int, default=2\n      Number of iterations for the power method.\n\n  whiten : bool, optional\n      When True (False by default) the `components_` vectors are multiplied\n      by the square root of (n_samples) and divided by the singular values to\n      ensure uncorrelated outputs with unit component-wise variances.\n\n      Whitening will remove some information from the transformed signal\n      (the relative variance scales of the components) but can sometime\n      improve the predictive accuracy of the downstream estimators by\n      making their data respect some hard-wired assumptions.\n\n  random_state : int, RandomState instance or None, optional, default=None\n      If int, random_state is the seed used by the random number generator;\n      If RandomState instance, random_state is the random number generator;\n      If None, the random number generator is the RandomState instance used\n      by `np.random`.\n\n  Attributes\n  ----------\n  components_ : array, shape (n_components, n_features)\n      Components with maximum variance.\n\n  explained_variance_ratio_ : array, shape (n_components,)\n      Percentage of variance explained by each of the selected components.\n      If k is not set then all components are stored and the sum of explained\n      variances is equal to 1.0.\n\n  singular_values_ : array, shape (n_components,)\n      The singular values corresponding to each of the selected components.\n      The singular values are equal to the 2-norms of the ``n_components``\n      variables in the lower-dimensional space.\n\n  mean_ : array, shape (n_features,)\n      Per-feature empirical mean, estimated from the training set.\n\n  Examples\n  --------\n  >>> import numpy as np\n  >>> from sklearn.decomposition import RandomizedPCA\n  >>> X = np.array([[-1, -1], [-2, -1], [-3, -2], [1, 1], [2, 1], [3, 2]])\n  >>> pca = RandomizedPCA(n_components=2)\n  >>> pca.fit(X)                 # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE\n  RandomizedPCA(copy=True, iterated_power=2, n_components=2,\n         random_state=None, whiten=False)\n  >>> print(pca.explained_variance_ratio_)  # doctest: +ELLIPSIS\n  [ 0.99244...  0.00755...]\n  >>> print(pca.singular_values_)  # doctest: +ELLIPSIS\n  [ 6.30061...  0.54980...]\n\n  References\n  ----------\n\n  .. [Halko2009] `Finding structure with randomness: Stochastic algorithms\n    for constructing approximate matrix decompositions Halko, et al., 2009\n    (arXiv:909)`\n\n  .. [MRT] `A randomized algorithm for the decomposition of matrices\n    Per-Gunnar Martinsson, Vladimir Rokhlin and Mark Tygert`\n\n  '

    def __init__(self, n_components=None, copy=True, iterated_power=2, whiten=False, random_state=None):
        self.n_components = n_components
        self.copy = copy
        self.iterated_power = iterated_power
        self.whiten = whiten
        self.random_state = random_state

    def fit(self, X, y=None):
        """Fit the model with X by extracting the first principal components.

    Parameters
    ----------
    X : array-like, shape (n_samples, n_features)
        Training data, where n_samples in the number of samples
        and n_features is the number of features.

    y : Ignored.

    Returns
    -------
    self : object
        Returns the instance itself.
    """
        self._fit(check_array(X))
        return self

    def _fit(self, X):
        """Fit the model to the data X.

    Parameters
    ----------
    X : array-like, shape (n_samples, n_features)
        Training vector, where n_samples in the number of samples and
        n_features is the number of features.

    Returns
    -------
    X : ndarray, shape (n_samples, n_features)
        The input data, copied, centered and whitened when requested.
    """
        random_state = check_random_state(self.random_state)
        X = np.atleast_2d(as_float_array(X, copy=(self.copy)))
        n_samples = X.shape[0]
        self.mean_ = np.mean(X, axis=0)
        X -= self.mean_
        if self.n_components is None:
            n_components = X.shape[1]
        else:
            n_components = self.n_components
        U, S, V = randomized_svd(X, n_components, n_iter=(self.iterated_power),
          random_state=random_state)
        self.explained_variance_ = exp_var = S ** 2 / (n_samples - 1)
        full_var = np.var(X, ddof=1, axis=0).sum()
        self.explained_variance_ratio_ = exp_var / full_var
        self.singular_values_ = S
        if self.whiten:
            self.components_ = V / S[:, np.newaxis] * math.sqrt(n_samples)
        else:
            self.components_ = V
        return X

    def transform(self, X):
        """Apply dimensionality reduction on X.

    X is projected on the first principal components previous extracted
    from a training set.

    Parameters
    ----------
    X : array-like, shape (n_samples, n_features)
        New data, where n_samples in the number of samples
        and n_features is the number of features.

    Returns
    -------
    X_new : array-like, shape (n_samples, n_components)

    """
        check_is_fitted(self, 'mean_')
        X = check_array(X)
        if self.mean_ is not None:
            X = X - self.mean_
        X = np.dot(X, self.components_.T)
        return X

    def fit_transform(self, X, y=None):
        """Fit the model with X and apply the dimensionality reduction on X.

    Parameters
    ----------
    X : array-like, shape (n_samples, n_features)
        New data, where n_samples in the number of samples
        and n_features is the number of features.

    y : Ignored.

    Returns
    -------
    X_new : array-like, shape (n_samples, n_components)

    """
        X = check_array(X)
        X = self._fit(X)
        return np.dot(X, self.components_.T)

    def inverse_transform(self, X):
        """Transform data back to its original space.

    Returns an array X_original whose transform would be X.

    Parameters
    ----------
    X : array-like, shape (n_samples, n_components)
        New data, where n_samples in the number of samples
        and n_components is the number of components.

    Returns
    -------
    X_original array-like, shape (n_samples, n_features)

    Notes
    -----
    If whitening is enabled, inverse_transform does not compute the
    exact inverse operation of transform.
    """
        check_is_fitted(self, 'mean_')
        X_original = np.dot(X, self.components_)
        if self.mean_ is not None:
            X_original = X_original + self.mean_
        return X_original


class MiniBatchPCA(IncrementalPCA):
    __doc__ = ' A modified version of IncrementalPCA to effectively\n  support multi-processing (but not work)\n  Original Author: Kyle Kastner <kastnerkyle@gmail.com>\n                   Giorgio Patrini\n  License: BSD 3 clause\n\n  Incremental principal components analysis (IPCA).\n\n  Linear dimensionality reduction using Singular Value Decomposition of\n  centered data, keeping only the most significant singular vectors to\n  project the data to a lower dimensional space.\n\n  Depending on the size of the input data, this algorithm can be much more\n  memory efficient than a PCA.\n\n  This algorithm has constant memory complexity, on the order\n  of ``batch_size``, enabling use of np.memmap files without loading the\n  entire file into memory.\n\n  The computational overhead of each SVD is\n  ``O(batch_size * n_features ** 2)``, but only 2 * batch_size samples\n  remain in memory at a time. There will be ``n_samples / batch_size`` SVD\n  computations to get the principal components, versus 1 large SVD of\n  complexity ``O(n_samples * n_features ** 2)`` for PCA.\n\n  Read more in the :ref:`User Guide <IncrementalPCA>`.\n\n  Parameters\n  ----------\n  n_components : int or None, (default=None)\n      Number of components to keep. If ``n_components `` is ``None``,\n      then ``n_components`` is set to ``min(n_samples, n_features)``.\n\n  batch_size : int or None, (default=None)\n      The number of samples to use for each batch. Only used when calling\n      ``fit``. If ``batch_size`` is ``None``, then ``batch_size``\n      is inferred from the data and set to ``5 * n_features``, to provide a\n      balance between approximation accuracy and memory consumption.\n\n  copy : bool, (default=True)\n      If False, X will be overwritten. ``copy=False`` can be used to\n      save memory but is unsafe for general use.\n\n  whiten : bool, optional\n      When True (False by default) the ``components_`` vectors are divided\n      by ``n_samples`` times ``components_`` to ensure uncorrelated outputs\n      with unit component-wise variances.\n\n      Whitening will remove some information from the transformed signal\n      (the relative variance scales of the components) but can sometimes\n      improve the predictive accuracy of the downstream estimators by\n      making data respect some hard-wired assumptions.\n\n  Attributes\n  ----------\n  components_ : array, shape (n_components, n_features)\n      Components with maximum variance.\n\n  explained_variance_ : array, shape (n_components,)\n      Variance explained by each of the selected components.\n\n  explained_variance_ratio_ : array, shape (n_components,)\n      Percentage of variance explained by each of the selected components.\n      If all components are stored, the sum of explained variances is equal\n      to 1.0\n\n  mean_ : array, shape (n_features,)\n      Per-feature empirical mean, aggregate over calls to ``partial_fit``.\n\n  var_ : array, shape (n_features,)\n      Per-feature empirical variance, aggregate over calls to\n      ``partial_fit``.\n\n  noise_variance_ : float\n      The estimated noise covariance following the Probabilistic PCA model\n      from Tipping and Bishop 1999. See "Pattern Recognition and\n      Machine Learning" by C. Bishop, 12.2.1 p. 574 or\n      http://www.miketipping.com/papers/met-mppca.pdf.\n\n  n_components_ : int\n      The estimated number of components. Relevant when\n      ``n_components=None``.\n\n  n_samples_seen_ : int\n      The number of samples processed by the estimator. Will be reset on\n      new calls to fit, but increments across ``partial_fit`` calls.\n\n  Notes\n  -----\n  Implements the incremental PCA model from:\n  `D. Ross, J. Lim, R. Lin, M. Yang, Incremental Learning for Robust Visual\n  Tracking, International Journal of Computer Vision, Volume 77, Issue 1-3,\n  pp. 125-141, May 2008.`\n  See http://www.cs.toronto.edu/~dross/ivt/RossLimLinYang_ijcv.pdf\n\n  This model is an extension of the Sequential Karhunen-Loeve Transform from:\n  `A. Levy and M. Lindenbaum, Sequential Karhunen-Loeve Basis Extraction and\n  its Application to Images, IEEE Transactions on Image Processing, Volume 9,\n  Number 8, pp. 1371-1374, August 2000.`\n  See http://www.cs.technion.ac.il/~mic/doc/skl-ip.pdf\n\n  We have specifically abstained from an optimization used by authors of both\n  papers, a QR decomposition used in specific situations to reduce the\n  algorithmic complexity of the SVD. The source for this technique is\n  `Matrix Computations, Third Edition, G. Holub and C. Van Loan, Chapter 5,\n  section 5.4.4, pp 252-253.`. This technique has been omitted because it is\n  advantageous only when decomposing a matrix with ``n_samples`` (rows)\n  >= 5/3 * ``n_features`` (columns), and hurts the readability of the\n  implemented algorithm. This would be a good opportunity for future\n  optimization, if it is deemed necessary.\n\n  For `multiprocessing`, you can do parallelized `partial_fit` or `transform`\n  but you cannot do `partial_fit` in one process and `transform` in the others.\n\n  Application\n  -----------\n  In detail, in order for PCA to work well, informally we require that\n  (i) The features have approximately zero mean, and\n  (ii) The different features have similar variances to each other.\n  With natural images, (ii) is already satisfied even without variance\n  normalization, and so we won’t perform any variance normalization.\n  (If you are training on audio data—say, on spectrograms—or on text data—say,\n  bag-of-word vectors—we will usually not perform variance normalization\n  either.)\n\n  By using PCA, we aim for:\n  (i) the features are less correlated with each other, and\n  (ii) the features all have the same variance.\n\n\n  Original link: http://ufldl.stanford.edu/tutorial/unsupervised/PCAWhitening/\n\n  References\n  ----------\n  D. Ross, J. Lim, R. Lin, M. Yang. Incremental Learning for Robust Visual\n      Tracking, International Journal of Computer Vision, Volume 77,\n      Issue 1-3, pp. 125-141, May 2008.\n\n  G. Golub and C. Van Loan. Matrix Computations, Third Edition, Chapter 5,\n      Section 5.4.4, pp. 252-253.\n\n  See also\n  --------\n  PCA\n  RandomizedPCA\n  KernelPCA\n  SparsePCA\n  TruncatedSVD\n  '

    def __init__(self, n_components=None, whiten=False, copy=True, batch_size=None):
        super(MiniBatchPCA, self).__init__(n_components=n_components, whiten=whiten,
          copy=copy,
          batch_size=batch_size)
        self.n_samples_seen_ = 0
        self.mean_ = 0.0
        self.var_ = 0.0
        self.components_ = None
        self._cache_batches = []
        self._nb_cached_samples = 0

    @property
    def is_fitted(self):
        return self.components_ is not None

    def fit(self, X, y=None):
        """Fit the model with X, using minibatches of size batch_size.

    Parameters
    ----------
    X: array-like, shape (n_samples, n_features)
        Training data, where n_samples is the number of samples and
        n_features is the number of features.

    y: Passthrough for ``Pipeline`` compatibility.

    Returns
    -------
    self: object
        Returns the instance itself.
    """
        X = check_array(X, copy=(self.copy), dtype=[np.float64, np.float32])
        n_samples, n_features = X.shape
        if self.batch_size is None:
            batch_size = 12 * n_features
        else:
            batch_size = self.batch_size
        for batch in gen_batches(n_samples, batch_size):
            x = X[batch]
            self.partial_fit(x, check_input=False)

        return self

    def partial_fit(self, X, y=None, check_input=True):
        """Incremental fit with X. All of X is processed as a single batch.

    Parameters
    ----------
    X: array-like, shape (n_samples, n_features)
        Training data, where n_samples is the number of samples and
        n_features is the number of features.

    Returns
    -------
    self: object
        Returns the instance itself.
    """
        if check_input:
            X = check_array(X, copy=(self.copy), dtype=[np.float64, np.float32])
        else:
            n_samples, n_features = X.shape
            if self.n_components is None:
                self.n_components_ = n_features
            else:
                if not 1 <= self.n_components <= n_features:
                    raise ValueError('n_components=%r invalid for n_features=%d, need more rows than columns for IncrementalPCA processing' % (
                     self.n_components, n_features))
                else:
                    self.n_components_ = self.n_components
            if n_samples < n_features or self._nb_cached_samples > 0:
                self._cache_batches.append(X)
                self._nb_cached_samples += n_samples
                if self._nb_cached_samples < n_features:
                    return
                X = np.concatenate((self._cache_batches), axis=0)
                self._cache_batches = []
                self._nb_cached_samples = 0
            n_samples = X.shape[0]
            if self.components_ is not None and self.components_.shape[0] != self.n_components_:
                raise ValueError('Number of input features has changed from %i to %i between calls to partial_fit! Try setting n_components to a fixed value.' % (
                 self.components_.shape[0], self.n_components_))
        col_mean, col_var, n_total_samples = _incremental_mean_and_var(X, last_mean=(self.mean_), last_variance=(self.var_),
          last_sample_count=(self.n_samples_seen_))
        total_var = np.sum(col_var * n_total_samples)
        if total_var == 0:
            return self
        else:
            if self.n_samples_seen_ == 0:
                X -= col_mean
            else:
                col_batch_mean = np.mean(X, axis=0)
                X -= col_batch_mean
                mean_correction = np.sqrt(self.n_samples_seen_ * n_samples / n_total_samples) * (self.mean_ - col_batch_mean)
                X = np.vstack((
                 self.singular_values_.reshape((-1, 1)) * self.components_, X, mean_correction))
            U, S, V = linalg.svd(X, full_matrices=False)
            U, V = svd_flip(U, V, u_based_decision=False)
            explained_variance = S ** 2 / n_total_samples
            explained_variance_ratio = S ** 2 / total_var
            self.n_samples_seen_ = n_total_samples
            self.components_ = V[:self.n_components_]
            self.singular_values_ = S[:self.n_components_]
            self.mean_ = col_mean
            self.var_ = col_var
            self.explained_variance_ = explained_variance[:self.n_components_]
            self.explained_variance_ratio_ = explained_variance_ratio[:self.n_components_]
            if self.n_components_ < n_features:
                self.noise_variance_ = explained_variance[self.n_components_:].mean()
            else:
                self.noise_variance_ = 0.0
            return self

    def transform(self, X, n_components=None):
        if n_components is not None:
            if n_components < 1.0:
                _ = np.cumsum(self.explained_variance_ratio_)
                n_components = (_ > n_components).nonzero()[0][0] + 1
            else:
                n_components = int(n_components)
        else:
            n = X.shape[0]
            if self.batch_size is None:
                batch_size = 12 * len(self.mean_)
            else:
                batch_size = self.batch_size
        X_transformed = []
        for start, end in batching(n=n, batch_size=batch_size):
            x = super(MiniBatchPCA, self).transform(X=(X[start:end]))
            if n_components is not None:
                x = x[:, :n_components]
            X_transformed.append(x)

        return np.concatenate(X_transformed, axis=0)

    def invert_transform(self, X):
        return super(MiniBatchPCA, self).inverse_transform(X=X)

    def transform_mpi(self, X, keep_order=True, ncpu=4, n_components=None):
        """ Sample as transform but using multiprocessing """
        n = X.shape[0]
        if self.batch_size is None:
            batch_size = 12 * len(self.mean_)
        else:
            batch_size = self.batch_size
        batch_list = [(i, min(i + batch_size, n)) for i in range(0, n + batch_size, batch_size) if i < n]

        def map_func(batch):
            start, end = batch
            x = super(MiniBatchPCA, self).transform(X=(X[start:end]))
            if n_components is not None:
                x = x[:, :n_components]
            yield (start, x)

        mpi = MPI(batch_list, func=map_func, ncpu=ncpu,
          batch=1,
          hwm=(ncpu * 12),
          backend='python')
        X_transformed = []
        for start, x in mpi:
            X_transformed.append((start, x))

        if keep_order:
            X_transformed = sorted(X_transformed, key=(lambda x: x[0]))
        X_transformed = np.concatenate([x[(-1)] for x in X_transformed], axis=0)
        return X_transformed

    def __str__(self):
        if self.is_fitted:
            explained_vars = ';'.join([ctext('%.2f' % i, 'cyan') for i in self.explained_variance_ratio_[:8]])
        else:
            explained_vars = 0
        s = '%s(batch_size=%s, #components=%s, #samples=%s, vars=%s)' % (
         ctext('MiniBatchPCA', 'yellow'),
         ctext(self.batch_size, 'cyan'),
         ctext(self.n_components, 'cyan'),
         ctext(self.n_samples_seen_, 'cyan'),
         explained_vars)
        return s