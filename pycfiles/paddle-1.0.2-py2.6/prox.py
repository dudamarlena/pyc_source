# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/paddle/prox.py
# Compiled at: 2011-01-27 08:44:27
"""
Implementation of the proximity operators for various convex functions.

The functions are named with the following convention: operator_args,
where operator at the moment is only norm1, while args can be X or XA,
X being the variable and A a constant.

Refs: Combettes and Pesquet, Proximal Splitting Methods in Signal Processing, arXiv:0912.3522v2
"""
import warnings, scipy as sp, scipy.linalg as la, common

def _st(X, mu):
    r"""
    Soft-thresholding.

    For all elements x of the matrix ``X`` computes their soft-thresholded
    value :math:`sign(x)\max\{0,|x|-\mu\}`

    Parameters
    ----------
    X : ndarray
        Input 
    mu : float
        Threshold
    
    Returns
    -------
    X : ndarray
        Soft-thresholded matrix
    """
    X = sp.sign(X) * sp.clip(sp.absolute(X) - mu, 0, sp.inf)
    return X


norm1_X = _st

def norm1_XA(X, A, gamma, maxiter=1000, rtol=0.001):
    (K, d) = X.shape
    N = A.shape[1]
    V = sp.zeros((K, N), sp.float32)
    if N > d:
        sigma = 2 * la.norm(sp.dot(A, A.T))
    else:
        sigma = 2 * la.norm(sp.dot(A.T, A))
    X = X / gamma
    E = ((sp.dot(V, A.T) - X) ** 2).mean()
    E0 = E
    for i in xrange(maxiter):
        Vnew = V - sp.dot(sp.dot(V, A.T) - X, A) / sigma
        Vnew = sp.where(sp.absolute(Vnew) > 1, sp.sign(Vnew), Vnew)
        Enew = ((sp.dot(Vnew, A.T) - X) ** 2).mean()
        rdelta = sp.absolute(E - Enew) / E0
        V = Vnew
        if rdelta < rtol:
            break
        E = Enew

    if i + 1 == maxiter:
        msg = 'Maximum number of iterations (%d) has been reached.'
        warnings.warn(msg % maxiter)
    PX = sp.dot(V, A.T)
    return gamma * (X - PX)


if __name__ == '__main__':
    (d, N, s, K) = (5, 20, 2, 10)
    (A, D, U) = common.gendata(d, N, s, K)
    X0 = sp.ones(D.T.shape, sp.float32)
    X0 /= sp.sqrt(sp.sum(X0 ** 2, 1)).reshape((-1, 1))
    X0A = sp.dot(X0, A)
    E0 = sp.absolute(X0A).sum()
    rtol = 1e-08
    maxiter = 100
    X, E = X0, E0
    for i in xrange(maxiter):
        X = norm1_XA(X, A, 1.0, maxiter=10000, rtol=rtol)
        X /= sp.sqrt(sp.sum(X ** 2, 1)).reshape((-1, 1))
        XA = sp.dot(X, A)
        Enew = sp.absolute(XA).sum()
        if (E - Enew) / E < 1e-12:
            print 'update smaller than relative tolerance'
            break
        E = Enew

    print 'after %d iterations' % i
    print Enew / E0
    print common.sparsity(X0A).mean()
    print common.sparsity(XA).mean()
    print la.norm(X0A), la.norm(XA)
    print XA
    print X
    print la.norm(sp.dot(X0, A) - U) / la.norm(U)
    print la.norm(sp.dot(X, A) - U) / la.norm(U)
    print la.norm(sp.dot(la.pinv(D.T).T, A) - U) / la.norm(U)