# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/pycopula/math_misc.py
# Compiled at: 2018-11-06 09:45:21
# Size of source mod 2**32: 1699 bytes
import numpy as np
from math import *

def _getAplus(A):
    eigval, eigvec = np.linalg.eig(A)
    Q = np.matrix(eigvec)
    xdiag = np.matrix(np.diag(np.maximum(eigval, 0)))
    return Q * xdiag * Q.T


def _getPs(A, W=None):
    W05 = np.matrix(W ** 0.5)
    return W05.I * _getAplus(W05 * A * W05) * W05.I


def _getPu(A, W=None):
    Aret = np.array(A.copy())
    Aret[W > 0] = np.array(W)[(W > 0)]
    return np.matrix(Aret)


def nearPD(A, nit=10):
    n = A.shape[0]
    W = np.identity(n)
    deltaS = 0
    Yk = A.copy()
    for k in range(nit):
        Rk = Yk - deltaS
        Xk = _getPs(Rk, W=W)
        deltaS = Xk - Rk
        Yk = _getPu(Xk, W=W)

    return Yk


def multivariate_t_distribution(x, mu, Sigma, df, d):
    """
    Multivariate t-student density:
    output:
        the density of the given element
    input:
        x = parameter (d dimensional numpy array or scalar)
        mu = mean (d dimensional numpy array or scalar)
        Sigma = scale matrix (dxd numpy array)
        df = degrees of freedom
        d: dimension
    """
    Num = gamma(1.0 * (d + df) / 2)
    Denom = gamma(1.0 * df / 2) * pow(df * pi, 1.0 * d / 2) * pow(np.linalg.det(Sigma), 0.5) * pow(1 + 1.0 / df * np.dot(np.dot(x - mu, np.linalg.inv(Sigma)), x - mu), 1.0 * (d + df) / 2)
    d = 1.0 * Num / Denom
    return d


def derivativeOf(fun, x, order):
    import scipy.special, scipy.misc
    h = 1e-08
    res = 0
    res = sum([(-1) ** (k + 1) * scipy.special.binom(order, k) * fun(x + k * h) for k in range(order + 1)])
    return scipy.misc.derivative(fun, 2, n=order, order=order + order % 2 + 1)
    return res / h ** order