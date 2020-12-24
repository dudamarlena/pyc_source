# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/zxh/ezLncPred/ezLncPred/models/longdist/bin/pca_attributes.py
# Compiled at: 2019-12-04 10:19:56
# Size of source mod 2**32: 1476 bytes
import numpy as np
from numpy import mean, cov, linalg

class PCAAttributes:

    def __init__(self, data, patterns):
        self.data = data
        self.patterns = [pattern for pattern in patterns if pattern not in ('fl', 'fp',
                                                                            'll',
                                                                            'lp')]

    def __calc_pca(self):
        data = np.array([list(r) for r in self.data[self.patterns]])
        self.loadings, self.eigenvalues = self.princomp(data)
        return self.loadings

    def attributes(self, size=50):
        self._PCAAttributes__calc_pca()
        norms = np.array([np.linalg.norm(x[:size]) for x in self.loadings])
        return sorted([self.patterns[i] for i in np.argsort(norms)[::-1][:size]])

    def princomp(self, A):
        """ performs principal components analysis
            (PCA) on the n-by-p data matrix A
            Rows of A correspond to observations, columns to variables.

        Returns :
         loadings :
           is a p-by-p matrix, each column containing coefficients
           for one principal component.
         latent :
           a vector containing the eigenvalues
           of the covariance matrix of A.
        """
        M = (A - mean((A.T), axis=1)).T
        latent, loadings = linalg.eig(cov(M))
        return (
         loadings, latent)