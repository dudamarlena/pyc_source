# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fynance/tools/filters.py
# Compiled at: 2019-09-18 09:26:31
# Size of source mod 2**32: 1459 bytes
import numpy as np
__all__ = [
 'kalman']

def kalman(X, distribution='normal'):
    """ Compute the Kalman filter.

    Kalman filter is computed as described in the paper by G. Welch and
    G. Bishop [1]_.

    Parameters
    ----------
    X : array_like
        Observed data.
    distribution : str, optional
        An available distribution in scipy library.

    Returns
    -------
    array_like
        Filter of kalman following the given distribution.

    References
    ----------
    .. [1] https://www.cs.unc.edu/~welch/media/pdf/kalman_intro.pdf

    """
    T, n = X.shape
    m_0 = 0
    C_0 = 1
    a = np.zeros([T, n])
    R = np.zeros([T, n])
    for t in range(1, T):
        a[t] = G[t] @ m[(t - 1)]
        R[t] = G[t] @ C[(t - 1)] @ G[t].T + W[t]
        A[t] = R[t] @ F[t] @ np.linalg.pinv(F[t] @ R[t] @ F[t].T + V[t])
        m[t] = a[t] + A[t] @ (X[t] - F[t].T @ a[t])
        C[t] = (np.identity(n) - A[t] @ F[t]) @ R[t]

    s_0 = 0
    x_0 = X[0]
    x_hat_1