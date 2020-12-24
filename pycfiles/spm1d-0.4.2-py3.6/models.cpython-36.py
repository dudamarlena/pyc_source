# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/spm1d/stats/anova/models.py
# Compiled at: 2019-08-22 04:37:04
# Size of source mod 2**32: 3338 bytes
"""
ANOVA computational core using an R-like linear model interface.
"""
import numpy as np
from ... import rft1d
eps = np.finfo(float).eps

class LinearModel(object):

    def __init__(self, Y, X, roi=None):
        Y = np.asarray(Y, dtype=float)
        self.dim = Y.ndim - 1
        self.Y = self._asmatrix(Y)
        self.X = np.matrix(X)
        self.J = self.X.shape[0]
        self.Q = self.Y.shape[1]
        self.QT = None
        self.eij = None
        self.roi = roi
        self._R = None
        self._beta = None
        self._rankR = None
        self._dfE = None
        self._SSE = None
        self._MSE = None
        if self.dim == 1:
            self.eij = None
            self.fwhm = None
            self.resels = None
        self.term_labels = None
        self.Fterms = None

    def _asmatrix(self, Y):
        if Y.ndim == 1:
            return np.matrix(Y).T
        else:
            return np.matrix(Y)

    def _rank(self, A, tol=None):
        """
                This is a slight modification of np.linalg.matrix_rank.
                The tolerance performs poorly for some matrices
                Here the tolerance is boosted by a factor of ten for improved performance.
                """
        M = np.asarray(A)
        S = np.linalg.svd(M, compute_uv=False)
        if tol is None:
            tol = 10 * S.max() * max(M.shape) * np.finfo(M.dtype).eps
        rank = sum(S > tol)
        return rank

    def fit(self, approx_residuals=None):
        Y, X, J = self.Y, self.X, self.J
        Xi = np.linalg.pinv(X)
        self._beta = Xi * Y
        self._R = np.eye(J) - X * Xi
        self._rankR = self._rank(self._R)
        self._SSE = np.diag(Y.T * self._R * Y)
        self._dfE = self._rankR
        if self._dfE > eps:
            self._MSE = self._SSE / self._dfE
        else:
            if approx_residuals is None:
                self.eij = np.asarray(self.Y - X * self._beta)
            else:
                C = approx_residuals
                A = X * C.T
                Ai = np.linalg.pinv(A)
                beta = Ai * Y
                self.eij = np.asarray(Y - A * beta)
        if self.dim == 1:
            self.fwhm = rft1d.geom.estimate_fwhm(self.eij)
            if self.roi is None:
                self.resels = rft1d.geom.resel_counts((self.eij), (self.fwhm), element_based=False)
            else:
                B = np.any((np.isnan(self.eij)), axis=0)
                B = np.logical_and(np.logical_not(B), self.roi)
                mask = np.logical_not(B)
                self.resels = rft1d.geom.resel_counts(mask, (self.fwhm), element_based=False)
        self.QT = np.linalg.qr(X)[0].T