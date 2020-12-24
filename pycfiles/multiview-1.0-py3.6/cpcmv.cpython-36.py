# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\multiview\cpcmv.py
# Compiled at: 2017-12-21 13:53:05
# Size of source mod 2**32: 4963 bytes
"""
CPC computes Common principal components of a set of matrices.

This file uses a variation of Trendafilov (2010) method to compute
the k first common principal components of a set of matrices in an
efficient way
"""
import numpy as np, warnings
from sklearn.base import BaseEstimator
import scipy.sparse.linalg as sparse

def cpc(x, k=0):
    n_g = np.array([x.shape[1]] * x.shape[0])
    p = x.shape[1]
    mcas = x.shape[0]
    iterator = 15
    n = n_g / np.sum(n_g)
    D = np.zeros((k, mcas))
    CPC = np.zeros((p, k))
    Qw = np.eye(p)
    s = np.zeros((p, p))
    for m in np.arange(mcas):
        s += n[m] * x[m]

    if k == p:
        res_vals, res_vectors = np.linalg.eigh(s)
    else:
        res_vals, res_vectors = sparse.eigsh(s, k=k)
    q0 = res_vectors[:, ::-1]
    for ncomp in np.arange(k):
        q = q0[:, ncomp]
        q = np.array(q0[:, ncomp]).reshape(len(q), 1)
        d = np.zeros((1, mcas))
        for m in np.arange(mcas):
            d[:, m] = np.dot(np.dot(q.T, x[m]), q)

        for _ in np.arange(iterator):
            s = np.zeros((p, p))
            for m in np.arange(mcas):
                s += n_g[m] * x[m] / d[:, m]

            w = np.dot(s, q)
            if ncomp != 0:
                w = np.dot(Qw, w)
            q = w / np.sqrt(np.dot(w.T, w))
            for m in np.arange(mcas):
                d[:, m] = np.dot(np.dot(q.T, x[m]), q)

        D[ncomp, :] = d
        CPC[:, ncomp] = q[:, 0]
        Qw -= np.dot(q, q.T)

    return (D, CPC)


class MVCPC(BaseEstimator):
    __doc__ = 'Compute common principal components of x.\n\n    Parameters\n    ----------\n\n    k : int, default 0\n        Number of components to extract (0 means all p components).\n\n    Attributes\n    ----------\n    eigenvalues_ : ndarray\n        Stores the eigenvalues computed in the algorithm.\n    eigenvectors_ : ndarray\n        Stores the eigenvectors computed in the algorithm.\n\n    References\n    ----------\n\n        Trendafilov, N. (2010). Stepwise estimation of common principal\n        components. *Computational Statistics and Data Analysis*, 54,\n        3446–3457.\n    '

    def __init__(self, k=0):
        self.k = k

    def fit(self, x):
        """Compute k common principal components of x.

        Parameters
        ----------

        x : array_like or ndarray
            A set of n matrices of dimension pxp given as a n x p x p  matrix.

        """
        self.fit_transform(x)
        return self

    def fit_transform(self, x):
        """Compute k common principal components of x, and return those
        components.

        Parameters
        ----------

        x : array_like or ndarray
            A set of n matrices of dimension pxp given as a n x p x p  matrix.

        Returns
        -------
        values : tuple
            Tuple with two elements:

            the eigenvalues

            the common eigenvectors

        Raises
        ------

            ValueError: Matrices are not square matrices or k value is
            negative.

        Examples
        --------

        >>> import numpy as np
        >>> x = np.array([[[2, 1, 8], [4, 5, 6], [3, 7, 9]],
                      [[1, 4, 7], [2, 5, 8], [3, 6, 9]]])
        >>> mv_cpc = MVCPC(k=3)
        >>> mv_cpc.fit_transform(x)
        (array([[ 16.09601677,  16.21849616],
                [ -0.11903382,  -0.85516505],
                [  0.02301705,  -0.3633311 ]]),
                array([[ 0.45139369, -0.88875921,  0.07969196],
                [ 0.55811719,  0.35088538,  0.75192065],
                [ 0.69623914,  0.29493478, -0.65441923]]))
        >>>
        """
        if x.shape[1] != x.shape[2]:
            raise ValueError('matrices have different size from mx n x n. Size found instead is %d x %d x %d' % x.shape)
        if self.k == 0:
            self.k = x.shape[1]
        else:
            if self.k > x.shape[1]:
                self.k = x.shape[1]
                warnings.warn('k is greater than matrix dimension. Maximum possible number of components is computed instead.')
            else:
                if self.k < 0:
                    raise ValueError('k value must be between 0 and number of samples of data matrix.')
        D, CPC = cpc(x, self.k)
        self.eigenvalues_ = D
        self.eigenvectors_ = CPC
        return (self.eigenvalues_, self.eigenvectors_)