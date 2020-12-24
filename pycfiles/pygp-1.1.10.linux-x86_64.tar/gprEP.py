# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/pygp/gp/gprEP.py
# Compiled at: 2013-04-10 06:45:39
"""
Class for Gaussian Process Regression with arbitrary likelihoods
commonly we will use EP to obtain a Gaussian approximation to the likelihood function
"""
from numpy.linalg.linalg import LinAlgError
from pygp.linalg.linalg_matrix import solve_chol
import logging, scipy as SP
from pygp.gp.gp_base import GP
from numpy.linalg import linalg

class GPEP(GP):
    """Gaussian Process class with an arbitrary likelihood (likelihood) which will be approximiated
    using an EP approximation"""

    def __init__(self, likelihood=None, Nep=3, *argin, **kwargin):
        super(GPEP, self).__init__(*argin, **kwargin)
        self.likelihood = likelihood
        self.Nep = Nep
        Nk = self.covar.get_number_of_parameters()
        Nl = self.likelihood.get_number_of_parameters()
        Nt = Nk + Nl
        self.Nlogtheta = Nt
        self.IlogthetaK = SP.zeros([Nt], dtype='bool')
        self.IlogthetaL = SP.zeros([Nt], dtype='bool')
        self.IlogthetaK[0:Nk] = True
        self.IlogthetaL[Nk:(Nk + Nl)] = True

    def updateEP(self, K, logthetaL=None):
        """update a kernel matrix K using Ep approximation
        [K,t,C0] = updateEP(K,logthetaL)
        logthetaL: likelihood hyperparameters
        t: new means of training targets
        K: new effective kernel matrix
        C0:0th moments
        """
        assert K.shape[0] == K.shape[1], 'Kernel matrix must be square'
        assert K.shape[0] == self.n, 'Kernel matrix has wrong dimension'
        g = SP.zeros([self.n, 2])
        g2 = SP.zeros([self.n, 2])
        z = SP.zeros([self.n])
        damp = SP.ones([self.n])
        K += SP.eye(K.shape[0]) * 1e-06
        Sigma = K.copy()
        KI = linalg.inv(K)
        mu = SP.zeros([self.n])
        n2mode = lambda x: SP.array([x[0] / x[1], 1 / x[1]])
        self.likelihood.setLogtheta(logthetaL)
        for nep in range(self.Nep):
            perm = SP.random.permutation(self.n)
            perm = SP.arange(self.n)
            for ni in perm:
                cav_np = n2mode([mu[ni], Sigma[(ni, ni)]]) - g[ni]
                cav_np[1] = abs(cav_np[1])
                ML = self.likelihood.calcExpectations(self.t[ni], cav_np, x=self.x[ni])
                gn = n2mode(ML[0:2]) - cav_np
                dg = gn - g[ni]
                ds2 = gn[1] - g[(ni, 1)]
                g[ni] = g[ni] + damp[ni] * dg
                if g[(ni, 1)] < 0:
                    g[(ni, 1)] = 1e-10
                z[ni] = ML[2]
                Sigma2 = Sigma
                Sigma = Sigma - ds2 / (1 + ds2 * Sigma[(ni, ni)]) * SP.outer(Sigma[:, ni], Sigma[ni, :])
                try:
                    Csigma = linalg.cholesky(Sigma)
                except LinAlgError:
                    logging.debug('damping')
                    Sigma = Sigma2
                    g[ni] = g2[ni]
                    damp[ni] *= 0.9

                mu = SP.dot(Sigma, g[:, 0])

            Sigma, mu, lml = self.epComputeParams(K, KI, g)
            g2 = g.copy()

        if nep == self.Nep - 1:
            pass
        self.muEP = g[:, 0] / g[:, 1]
        self.vEP = 1 / g[:, 1]

    def epComputeParams(self, K, KI, g):
        """calculate the ep Parameters
        K: plain kernel matrix
        g: [0,1]: natural parameter rep. [2]: 0. moment for lml
        """
        KepI = SP.diag(g[:, 1])
        Sigma = linalg.inv(KI + KepI)
        mu = SP.dot(Sigma, g[:, 0])
        lml = 0
        return [Sigma, mu, lml]

    def getCovariances(self, logtheta):
        """[L,Alpha] = getCovariances()
        - special overwritten version of getCovariance (gpr.py)
        - here: EP updates are employed"""
        if (logtheta == self.logtheta).all() and self.cached_L is not None:
            return [self.cached_L, self.cached_alpha]
        else:
            self.logtheta = logtheta.copy()
            assert self.Nlogtheta == logtheta.shape[0], 'incorrect shape of kernel parameter matrix'
            K = self.covar.K(logtheta[self.IlogthetaK], self.x)
            self.updateEP(K, logtheta[self.IlogthetaL])
            Keff = K + SP.diag(self.vEP)
            self.cached_L = linalg.cholesky(Keff)
            self.cached_alpha = solve_chol(self.cached_L.transpose(), self.muEP)
            return [self.cached_L, self.cached_alpha]