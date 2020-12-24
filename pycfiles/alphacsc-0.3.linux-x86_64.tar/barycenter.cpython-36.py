# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tom/.local/miniconda/lib/python3.6/site-packages/alphacsc/other/sdtw/barycenter.py
# Compiled at: 2019-06-04 04:10:26
# Size of source mod 2**32: 1860 bytes
import numpy as np
from scipy.optimize import minimize
from sdtw import SoftDTW
from sdtw.distance import SquaredEuclidean

def sdtw_barycenter(X, barycenter_init, gamma=1.0, weights=None, method='L-BFGS-B', tol=0.001, max_iter=50):
    """
    Compute barycenter (time series averaging) under the soft-DTW geometry.

    Parameters
    ----------
    X: list
        List of time series, numpy arrays of shape [len(X[i]), d].

    barycenter_init: array, shape = [length, d]
        Initialization.

    gamma: float
        Regularization parameter.
        Lower is less smoothed (closer to true DTW).

    weights: None or array
        Weights of each X[i]. Must be the same size as len(X).

    method: string
        Optimization method, passed to `scipy.optimize.minimize`.
        Default: L-BFGS.

    tol: float
        Tolerance of the method used.

    max_iter: int
        Maximum number of iterations.
    """
    if weights is None:
        weights = np.ones(len(X))
    weights = np.array(weights)

    def _func(Z):
        Z = (Z.reshape)(*barycenter_init.shape)
        G = np.zeros_like(Z)
        obj = 0
        for i in range(len(X)):
            D = SquaredEuclidean(Z, X[i])
            sdtw = SoftDTW(D, gamma=gamma)
            value = sdtw.compute()
            E = sdtw.grad()
            G_tmp = D.jacobian_product(E)
            G += weights[i] * G_tmp
            obj += weights[i] * value

        return (obj, G.ravel())

    res = minimize(_func, (barycenter_init.ravel()), method=method, jac=True, tol=tol,
      options=dict(maxiter=max_iter, disp=False))
    return (res.x.reshape)(*barycenter_init.shape)