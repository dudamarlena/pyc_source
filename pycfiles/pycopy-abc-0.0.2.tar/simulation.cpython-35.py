# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/pycopula/simulation.py
# Compiled at: 2018-11-08 17:34:30
# Size of source mod 2**32: 1775 bytes
import numpy as np, scipy.stats as stats
from scipy.linalg import sqrtm
from numpy.linalg import inv, cholesky
from scipy.stats import multivariate_normal, invgamma, t as student
import math

def simulate(copula, n):
    """
        Generates random variables with selected copula's structure.

        Parameters
        ----------
        copula : Copula
                The Copula to sample.
        n : integer
                The size of the sample.
        """
    d = copula.getDimension()
    X = []
    if type(copula).__name__ == 'GaussianCopula':
        Sigma = copula.getCovariance()
        D = sqrtm(np.diag(np.diag(Sigma)))
        Dinv = inv(D)
        P = np.dot(np.dot(Dinv, Sigma), Dinv)
        A = cholesky(P)
        for i in range(n):
            Z = np.random.normal(size=d)
            V = np.dot(A, Z)
            U = stats.norm.cdf(V)
            X.append(U)

    else:
        if type(copula).__name__ == 'ArchimedeanCopula':
            U = np.random.rand(n, d)
            LSinv = {'clayton': lambda theta: np.random.gamma(shape=1.0 / theta), 
             'gumbel': lambda theta: stats.levy_stable.rvs(1.0 / theta, 1.0, 0, math.cos(math.pi / (2 * theta)) ** theta), 
             'frank': lambda theta: stats.logser.rvs(1.0 - math.exp(-theta)), 
             'amh': lambda theta: stats.geom.rvs(theta)}
            for i in range(n):
                V = LSinv[copula.getFamily()](copula.getParameter())
                X_i = [copula.inverseGenerator(-np.log(u) / V) for u in U[i, :]]
                X.append(X_i)

        elif type(copula).__name__ == 'StudentCopula':
            nu = copula.getFreedomDegrees()
            Sigma = copula.getCovariance()
            for i in range(n):
                Z = multivariate_normal.rvs(size=1, cov=Sigma)
                W = invgamma.rvs(nu / 2.0, size=1)
                U = np.sqrt(W) * Z
                X_i = [student.cdf(u, nu) for u in U]
                X.append(X_i)

    return X