# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/odin/ml/plda.py
# Compiled at: 2019-08-13 03:55:05
# Size of source mod 2**32: 14749 bytes
""""
author: 'Omid Sadjadi, Timothee Kheyrkhah'
email: 'omid.sadjadi@nist.gov'
"""
import time, warnings
from numbers import Number
import numpy as np
from scipy.linalg import cholesky, eigh, inv, solve, svd
from six import string_types
from odin.backend import calc_white_mat, length_norm
from odin.ml.base import BaseEstimator, Evaluable, TransformerMixin
from odin.ml.scoring import VectorNormalizer, compute_class_avg, compute_within_cov
from odin.utils import unique

def logdet(A):
    u = cholesky(A)
    y = 2 * np.log(np.diag(u)).sum()
    return y


class PLDA(BaseEstimator, TransformerMixin, Evaluable):
    __doc__ = " Probabilistic LDA\n\n  Parameters\n  ----------\n  n_phi : int\n    number of dimension for the latent space\n\n  centering : bool (default: True)\n    mean normalization the data before EM\n\n  wccn : bool (default: True)\n    within class covariance normalization before EM\n\n  unit_length : bool (default: True)\n    normalize vector length of each sample to 1 before EM\n\n  n_iter : {integer, 'auto'}\n    if 'auto', keep iterating until no more improvement (i.e. reduction in `sigma` value)\n    compared to the `improve_threshold`\n\n  improve_threshold : scalar\n    Only used in case `n_iter='auto'`\n\n  labels : {list of string, or None} (default: None)\n    labels information for `evaluate` method\n\n  seed : int\n    random seed for reproducibility\n\n  verbose : int (default: 0)\n    verbose level, 0 for turning off all logging activities,\n    1 for basics notification, 2 for fitting progress.\n    if `2`, compute log-likelihood during fitting EM, this will\n    significantly slows down the process, only suggested for debugging\n\n  Attributes\n  ----------\n  Sigma_ : [feat_dim, feat_dim]\n  Phi_ : [feat_dim, n_phi]\n  Sb_ : [feat_dim, feat_dim]\n  St_ : [feat_dim, feat_dim]\n  Lambda : []\n  Uk : []\n  Q_hat : []\n  X_model_ : [num_class, feat_dim]\n    class-dependence feature vectors\n  "

    def __init__(self, n_phi=None, centering=True, wccn=True, unit_length=True, n_iter='auto', improve_threshold=0.1, labels=None, dtype='float64', random_state=None, verbose=0):
        super(PLDA, self).__init__()
        if n_phi is not None:
            n_phi = int(n_phi)
        else:
            self.n_phi_ = n_phi
            if isinstance(n_iter, string_types):
                n_iter = n_iter.lower()
                assert n_iter == 'auto', 'Invalid `n_iter` value: %s' % n_iter
            elif isinstance(n_iter, Number):
                assert n_iter > 0, '`n_iter` must greater than 0, but given: %d' % n_iter
            else:
                self.n_iter_ = n_iter
                self.improve_threshold_ = float(improve_threshold)
                self.feat_dim_ = None
                self._labels = labels
                self.verbose_ = int(verbose)
                self._normalizer = VectorNormalizer(centering=centering,
                  wccn=wccn,
                  unit_length=unit_length,
                  lda=False,
                  concat=False)
                self._dtype = np.dtype(dtype)
                if random_state is None:
                    self._rand_state = np.random.RandomState(None)
                else:
                    if isinstance(random_state, Number):
                        self._rand_state = np.random.RandomState(seed=random_state)
                    else:
                        if isinstance(random_state, np.random.RandomState):
                            self._rand_state = random_state
                        else:
                            raise ValueError('Invalid argument for `random_state`: %s' % str(random_state))
        self.Sigma_ = None
        self.Phi_ = None
        self.Sb_ = None
        self.St_ = None

    @property
    def dtype(self):
        return self._dtype

    @property
    def feat_dim(self):
        return self.feat_dim_

    @property
    def normalizer(self):
        return self._normalizer

    @property
    def labels(self):
        return self._labels

    @property
    def num_classes(self):
        return len(self._labels)

    @property
    def is_fitted(self):
        if not hasattr(self, 'Lambda_') or not hasattr(self, 'Uk_') or not hasattr(self, 'Q_hat_') or not hasattr(self, 'X_model_'):
            return False
        else:
            return True

    def __getstate__(self):
        if not self.is_fitted:
            raise RuntimeError('The PLDA have not been fitted, nothing to pickle!')
        return (
         self.n_phi_, self.n_iter_, self.feat_dim_, self._labels, self.verbose_,
         self._normalizer, self._dtype, self._rand_state,
         self.Sigma_, self.Phi_, self.Sb_, self.St_,
         self.Lambda_, self.Uk_, self.Q_hat_, self.X_model_)

    def __setstate__(self, states):
        self.n_phi_, self.n_iter_, self.feat_dim_, self._labels, self.verbose_, self._normalizer, self._dtype, self._rand_state, self.Sigma_, self.Phi_, self.Sb_, self.St_, self.Lambda_, self.Uk_, self.Q_hat_, self.X_model_ = states

    def initialize(self, X, labels):
        feat_dim = X.shape[1]
        if self.feat_dim is None or self._num_classes is None:
            self.feat_dim_ = int(feat_dim)
            if self._labels is None:
                self._labels = labels
            if self.feat_dim <= self.n_phi_:
                raise RuntimeError('`feat_dim=%d` must be greater than `n_phi=%d`' % (
                 self.feat_dim, self.n_phi_))
            self.Sigma_ = (1.0 / self.feat_dim * np.eye(self.feat_dim) + self._rand_state.randn(self.feat_dim, self.feat_dim)).astype(self.dtype)
            self.Phi_ = self.normalizer.transform(self._rand_state.randn(self.n_phi_, self.feat_dim)).T.astype(self.dtype)
            self.Sb_ = np.zeros((self.feat_dim, self.feat_dim), dtype=(self.dtype))
            self.St_ = np.zeros((self.feat_dim, self.feat_dim), dtype=(self.dtype))
        if self.feat_dim != feat_dim:
            raise ValueError('Mismatch the input feature dimension, %d != %d' % (
             self.feat_dim, feat_dim))
        if self.num_classes != len(labels):
            raise ValueError('Mismatch the number of output classes, %d != %d' % (
             self.num_classes, len(labels)))

    def _update_caches(self):
        iSt = inv(self.St_)
        iS = inv(self.St_ - np.dot(np.dot(self.Sb_, iSt), self.Sb_))
        Q = iSt - iS
        P = np.dot(np.dot(iSt, self.Sb_), iS)
        U, s, V = svd(P, full_matrices=False)
        self.Lambda_ = np.diag(s[:self.n_phi_])
        self.Uk_ = U[:, :self.n_phi_]
        self.Q_hat_ = np.dot(np.dot(self.Uk_.T, Q), self.Uk_)

    def fit_maximum_likelihood(self, X, y):
        if isinstance(X, (tuple, list)):
            X = np.asarray(X)
        else:
            if 'odin.fuel' in str(type(X)):
                X = X[:]
        if isinstance(y, (tuple, list)):
            y = np.asarray(y)
        X = self.normalizer.fit(X, y).transform(X)
        classes = np.unique(y)
        self.initialize(X, labels=classes)
        Sw = compute_within_cov(X, y, classes)
        self.St_ = np.cov(X.T)
        self.Sb_ = self.St_ - Sw
        self._update_caches()
        model_vecs = compute_class_avg(X, y, classes=classes)
        self.X_model_ = np.dot(model_vecs, self.Uk_)
        return self

    def fit(self, X, y):
        """
    Parameters
    ----------
    X : [num_samples, feat_dim]
    y : [num_samples]
    """
        if isinstance(X, (tuple, list)):
            X = np.asarray(X)
        else:
            if 'odin.fuel' in str(type(X)):
                X = X[:]
            else:
                if isinstance(y, (tuple, list)):
                    y = np.asarray(y)
                assert X.shape[0] == y.shape[0], 'Number of samples mismatch in `X` and `y`, %d != %d' % (
                 X.shape[0], y.shape[0])
            y_counts = np.bincount(y)
            classes = np.unique(y)
            X = self.normalizer.fit(X, y).transform(X)
            self.initialize(X, labels=classes)
            F = np.zeros((self.num_classes, self.feat_dim))
            for clz in np.unique(y):
                F[clz, :] = X[y == clz, :].sum(axis=0)

            if self.verbose_ > 0:
                print('Re-estimating the Eigenvoice subspace with {} factors ...'.format(self.n_phi_))
        X_sqr = np.dot(X.T, X)
        iter = 0
        last_llk_value = None
        while True:
            e_time = time.time()
            Ey, Eyy = self.expectation_plda(F, y_counts)
            e_time = time.time() - e_time
            m_time = time.time()
            self.maximization_plda(X, X_sqr, F, Ey, Eyy)
            m_time = time.time() - m_time
            llk = 'None'
            llk_value = None
            if self.verbose_ > 1 or isinstance(self.n_iter_, string_types):
                llk_value = self.compute_llk(X)
                llk = '%.2f' % llk_value
            if self.verbose_ > 0:
                print('#iter:%-3d \t [llk = %s] \t [E-step = %.2f s] [M-step = %.2f s]' % (
                 iter + 1, llk, e_time, m_time))
            iter += 1
            if isinstance(self.n_iter_, Number):
                if iter >= self.n_iter_:
                    break
            else:
                if iter > 2:
                    if last_llk_value is not None:
                        if llk_value - last_llk_value < self.improve_threshold_:
                            break
            last_llk_value = llk_value

        self.Sb_ = self.Phi_.dot(self.Phi_.T)
        self.St_ = self.Sb_ + self.Sigma_
        self._update_caches()
        model_vecs = compute_class_avg(X, y, classes=classes)
        self.X_model_ = np.dot(model_vecs, self.Uk_)

    def expectation_plda(self, F, cls_counts):
        """
    Parameters
    ----------
    F : [num_classes, feat_dim]
    cls_count : [num_classes]
    """
        num_classes = F.shape[0]
        Eyy = np.zeros(shape=(self.n_phi_, self.n_phi_))
        Ey_clz = np.zeros(shape=(num_classes, self.n_phi_))
        uniqFreqs = unique(cls_counts, keep_order=True)
        n_uniq = len(uniqFreqs)
        invTerms = np.empty(shape=(n_uniq, self.n_phi_, self.n_phi_))
        PhiT_invS = solve(self.Sigma_.T, self.Phi_).T
        PhiT_invS_Phi = np.dot(PhiT_invS, self.Phi_)
        I = np.eye(self.n_phi_)
        for ix in range(n_uniq):
            nPhiT_invS_Phi = uniqFreqs[ix] * PhiT_invS_Phi
            invTerms[ix] = inv(I + nPhiT_invS_Phi)

        for clz in range(num_classes):
            num_samples = cls_counts[clz]
            PhiT_invS_y = np.dot(PhiT_invS, F[clz, :])
            idx = np.flatnonzero(uniqFreqs == num_samples)[0]
            Cyy = invTerms[idx]
            Ey_clz[clz, :] = np.dot(Cyy, PhiT_invS_y)
            Eyy += num_samples * Cyy

        Eyy += np.dot((Ey_clz * cls_counts[:, None]).T, Ey_clz)
        return (Ey_clz, Eyy)

    def compute_llk(self, X):
        """
    Parameters
    ----------
    X : [num_samples, feat_dim]
    """
        num_samples = X.shape[0]
        S = np.dot(self.Phi_, self.Phi_.T) + self.Sigma_
        llk = -0.5 * (self.feat_dim * num_samples * np.log(2 * np.pi) + num_samples * logdet(S) + np.sum(X * solve(S, X.T).T))
        return llk

    def maximization_plda(self, X, X_sqr, F, Ey, Eyy):
        """
    ML re-estimation of the Eignevoice subspace and the covariance of the
    residual noise (full).

    Paremters
    ---------
    X : [num_samples, feat_dim]
    X_cov : [feat_dim, feat_dim]
    F : [num_classes, feat_dim]
    Ey : [num_classes, n_phi]
    Eyy : [n_phi, n_phi]
    """
        num_samples = X.shape[0]
        Ey_FT = np.dot(Ey.T, F)
        self.Phi_ = solve(Eyy.T, Ey_FT).T
        self.Sigma_ = 1.0 / num_samples * (X_sqr - np.dot(self.Phi_, Ey_FT))

    def transform(self, X):
        if not self.is_fitted:
            raise RuntimeError("This model hasn't been fitted!")
        if isinstance(X, (tuple, list)):
            X = np.asarray(X)
        else:
            if 'odin.fuel' in str(type(X)):
                X = X[:]
        X_norm = self.normalizer.transform(X)
        X_project = np.dot(X_norm, self.Uk_)
        return X_project

    def predict_log_proba(self, X, X_model=None):
        """
    Parameters
    ----------
    X : [num_samples, feat_dim]
    X_model : [num_classes, feat_dim]
      if None, use class average extracted based on fitted data

    Return
    ------
    log-probabilities matrix [num_samples, num_classes]
    """
        if not self.is_fitted:
            raise RuntimeError("This model hasn't been fitted!")
        else:
            if X_model is None:
                X_model = self.X_model_
            else:
                X_model = np.dot(self.normalizer.transform(X_model), self.Uk_)
            if X_model.shape[0] != self.num_classes:
                warnings.warn('The model matrix contains %d classes, but the fitted number of classes is %d' % (
                 X_model.shape[0], self.num_classes))
            if isinstance(X, (tuple, list)):
                X = np.asarray(X)
            elif 'odin.fuel' in str(type(X)):
                X = X[:]
        X = np.dot(self.normalizer.transform(X), self.Uk_)
        score_h1 = np.sum((np.dot(X_model, self.Q_hat_) * X_model), axis=1, keepdims=True)
        score_h2 = np.sum((np.dot(X, self.Q_hat_) * X), axis=1, keepdims=True)
        score_h1h2 = 2 * np.dot(X, np.dot(X_model, self.Lambda_).T)
        scores = score_h1h2 + score_h1.T + score_h2
        return scores