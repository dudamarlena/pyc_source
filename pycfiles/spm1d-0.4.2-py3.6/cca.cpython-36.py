# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/spm1d/stats/cca.py
# Compiled at: 2019-08-22 04:37:04
# Size of source mod 2**32: 4036 bytes
"""
CANONICAL CORRELATION ANALYSIS
"""
from math import sqrt, log
import numpy as np
from . import _mvbase, _spm

def cca_single_node(y, x):
    N = y.shape[0]
    X, Y = np.matrix(x.T).T, np.matrix(y)
    Z = np.matrix(np.ones(N)).T
    Rz = np.eye(N) - Z * np.linalg.inv(Z.T * Z) * Z.T
    XStar = Rz * X
    YStar = Rz * Y
    p, r = (1.0, 1.0)
    m = N - p - r
    H = YStar.T * XStar * np.linalg.inv(XStar.T * XStar) * XStar.T * YStar / p
    W = YStar.T * (np.eye(N) - XStar * np.linalg.inv(XStar.T * XStar) * XStar.T) * YStar / m
    F = np.linalg.inv(W) * H
    ff = np.linalg.eigvals(F)
    fmax = float(np.real(ff.max()))
    r2max = fmax * p / (m + fmax * p)
    rmax = sqrt(r2max)
    m = y.shape[1]
    x2 = -(N - 1 - 0.5 * (m + 2)) * log(1 - rmax ** 2)
    return x2


def _cca_single_node_efficient(y, x, Rz, XXXiX):
    N = y.shape[0]
    Y = np.matrix(y)
    YStar = Rz * Y
    p, r = (1.0, 1.0)
    m = N - p - r
    H = YStar.T * XXXiX * YStar / p
    W = YStar.T * (np.eye(N) - XXXiX) * YStar / m
    F = np.linalg.inv(W) * H
    ff = np.linalg.eigvals(F)
    fmax = float(np.real(ff.max()))
    r2max = fmax * p / (m + fmax * p)
    rmax = sqrt(r2max)
    m = y.shape[1]
    x2 = -(N - 1 - 0.5 * (m + 2)) * log(1 - rmax ** 2)
    return x2


def cca(Y, x, roi=None):
    """
        Canonical correlation analysis (CCA).
        
        :Parameters:
                - *Y* --- A list or tuple of (J x Q) numpy arrays
                - *x* --- (J x 1) list or array (independent variable)

        
        :Returns:
                - X2 : An **spm1d._spm.SPM_X2** instance
        
        :Note:
                -  Currently only a univariate 0D independent variable (x) is supported.
        """
    N = Y.shape[0]
    X = np.matrix(x.T).T
    Z = np.matrix(np.ones(N)).T
    Rz = np.eye(N) - Z * np.linalg.inv(Z.T * Z) * Z.T
    XStar = Rz * X
    XXXiX = XStar * np.linalg.inv(XStar.T * XStar) * XStar.T
    if Y.ndim == 2:
        X2 = _cca_single_node_efficient(Y, x, Rz, XXXiX)
        df = (1, Y.shape[1])
        return _spm.SPM0D_X2(X2, df)
    else:
        X2 = np.array([_cca_single_node_efficient(Y[:, q, :], x, Rz, XXXiX) for q in range(Y.shape[1])])
        X2 = X2 if roi is None else np.ma.masked_array(X2, np.logical_not(roi))
        R = _mvbase._get_residuals_regression(Y, x)
        fwhm = _mvbase._fwhm(R)
        resels = _mvbase._resel_counts(R, fwhm, roi=roi)
        df = (1, Y.shape[2])
        return _spm.SPM_X2(X2, df, fwhm, resels, None, None, R, roi=roi)