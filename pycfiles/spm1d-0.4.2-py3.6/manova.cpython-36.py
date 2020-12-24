# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/spm1d/stats/manova.py
# Compiled at: 2019-08-22 04:37:04
# Size of source mod 2**32: 3642 bytes
"""
MANOVA
"""
from math import sqrt, log
import numpy as np
from . import _mvbase, _spm
eps = np.finfo(float).eps

def manova1_single_node(Y, GROUP):
    u = np.unique(GROUP)
    nGroups = u.size
    nResponses = Y.shape[0]
    nComponents = Y.shape[1]
    X = np.zeros((nResponses, nGroups))
    ind0 = 0
    for i, uu in enumerate(u):
        n = (GROUP == uu).sum()
        X[ind0:ind0 + n, i] = 1
        ind0 += n

    Y, X = np.matrix(Y), np.matrix(X)
    b = np.linalg.pinv(X) * Y
    R = Y - X * b
    R = R.T * R
    X0 = np.matrix(np.ones(Y.shape[0])).T
    b0 = np.linalg.pinv(X0) * Y
    R0 = Y - X0 * b0
    R0 = R0.T * R0
    lam = np.linalg.det(R) / (np.linalg.det(R0) + eps)
    N, p, k = float(nResponses), float(nComponents), float(nGroups)
    x2 = -(N - 1 - 0.5 * (p + k)) * log(lam)
    df = p * (k - 1)
    return x2


def _manova1_single_node_efficient(Y, GROUP, X, Xi, X0, X0i, nGroups):
    Y = np.matrix(Y)
    b = Xi * Y
    R = Y - X * b
    R = R.T * R
    b0 = X0i * Y
    R0 = Y - X0 * b0
    R0 = R0.T * R0
    lam = np.linalg.det(R) / (np.linalg.det(R0) + eps)
    (N, p), k = Y.shape, float(nGroups)
    x2 = -(N - 1 - 0.5 * (p + k)) * log(lam)
    return x2


def manova1(Y, A, equal_var=True, roi=None):
    """
        Two-way repeated-measures ANOVA.
        
        :Parameters:
                - *Y* --- (J x Q x I) numpy array
                - *A* --- (J x 1) vector of integer labels for Factor A
                - *equal_var* --- If *True*, equal group variance will be assumed

        :Returns:
                - X2 : An **spm1d._spm.SPM_X2** instance

        :Note:
                - Non-sphericity correction not implemented. Equal variance must be assumed by setting "equal_var=True".
        """
    if equal_var is not True:
        raise UserWarning('Non-sphericity correction not implemented. To continue you must assume equal variance and set "equal_var=True".')
    u = np.unique(A)
    nGroups = u.size
    nResponses = Y.shape[0]
    X = np.zeros((nResponses, nGroups))
    ind0 = 0
    for i, uu in enumerate(u):
        X[(A == uu, i)] = 1

    X = np.matrix(X)
    Xi = np.linalg.pinv(X)
    X0 = np.matrix(np.ones(Y.shape[0])).T
    X0i = np.linalg.pinv(X0)
    if Y.ndim == 2:
        nComponents = Y.shape[1]
        X2 = _manova1_single_node_efficient(Y, A, X, Xi, X0, X0i, nGroups)
        df = nComponents * (nGroups - 1)
        return _spm.SPM0D_X2(X2, (1, df))
    else:
        nNodes = Y.shape[1]
        nComponents = Y.shape[2]
        X2 = np.array([_manova1_single_node_efficient(Y[:, i, :], A, X, Xi, X0, X0i, nGroups) for i in range(nNodes)])
        X2 = X2 if roi is None else np.ma.masked_array(X2, np.logical_not(roi))
        R = _mvbase._get_residuals_manova1(Y, A)
        fwhm = _mvbase._fwhm(R)
        resels = _mvbase._resel_counts(R, fwhm, roi=roi)
        df = nComponents * (nGroups - 1)
        return _spm.SPM_X2(X2, (1, df), fwhm, resels, None, None, R, roi=roi)