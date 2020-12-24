# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/vb_ihmm/model/continuous.py
# Compiled at: 2014-03-13 01:37:40
"""
Created on 6 Dec 2013

@author: James McInerney
"""
from numpy import *
from scipy.linalg import inv
from matplotlib.pyplot import *
from random import choice
from anim_particles.DrawParticles import KalmanAnim
import time
from util import logLikMVG

class KalmanFilter(object):

    def __init__(self, X, T, N, hyperparams=None, fixed=None):
        self._X = X
        self._T = T
        self._N = N
        self._hyperparams = hyperparams
        self._fixed = fixed
        self._activated = 1
        self._weightObs = ones(N)

    def loglik(self, LD):
        X, T = self._X, self._T
        NT = T.max() - T.min() + 1
        ll = zeros((NT, LD))
        for t in range(NT):
            ns, = where(T == t)
            for n in ns:
                x_n = self._X[n, :]
                if not any(isnan(x_n)):
                    ll0 = logLikMVG(x_n, self.expMu()[t, :], self.expCov()[t, :, :])
                    ll[(t, n % len(ns))] = ll0

        return ll

    def m(self):
        fixed = self._fixed
        if fixed is None:
            [ s.m(self._exp_z) for s in self._sensors ]
        return

    def e(self):
        if self._activated:
            self._do_e()

    def _do_e(self):
        self._exp_mu, self._exp_V = self._forwardsZ(self._X)

    def expMu(self):
        return self._exp_mu

    def expCov(self):
        return self._exp_V

    def _forwardsZ(self, X):
        fixed = self._fixed
        if fixed is not None:
            A = fixed['A']
            G = fixed['G']
            C = fixed['C']
            S = fixed['S']
            mu0 = fixed['mu0']
            V0 = fixed['V0']
        else:
            raise Exception('Not implemented')
        N = self._N
        T = self._T
        NT = max(T) + 1
        _, XDim = shape(X)
        mu = zeros((NT, XDim))
        V = zeros((NT, XDim, XDim))
        mu[0, :] = mu0
        V[0, :, :] = V0
        prevMu, prevV = mu[0, :], V[0, :, :]
        P_tm1 = V0
        t = T[0]
        for n in range(N):
            while t < T[n]:
                t += 1
                mu[t, :] = dot(A, mu[t - 1, :])
                P_tm1 = dot(A, dot(V[t - 1, :, :], A.T)) + G
                V[t, :, :] = P_tm1
                prevMu, prevV = mu[t, :], V[t, :, :]

            if not any(isnan(X[n, :])):
                K_n = dot(prevV, dot(C.T, inv(dot(C, dot(prevV, C.T)) + S)))
                mu[t, :] = prevMu + self._weightObs[n] * dot(K_n, X[n, :] - dot(C, dot(A, prevMu)))
                V[t, :, :] = prevV - dot(dot(K_n, C), prevV)
                prevMu, prevV = mu[t, :], V[t, :, :]

        return (mu, V)


def genKalman(NT=100, XDim=2, L=1, sparsity=0.5, fixObsCount=100000.0):
    X = zeros((NT, XDim))
    Y = []
    T = []
    A = lambda z: z
    C = lambda x: x
    G = 1.0 * eye(XDim)
    S = 0.01 * eye(XDim)
    mu0 = zeros(XDim)
    V0 = eye(XDim)
    IO = 1
    X[0, :] = random.multivariate_normal(mu0, V0)
    for n in range(IO):
        Y.append(random.multivariate_normal(C(X[0, :]), S))
        T.append(0)

    for n in range(1, NT):
        X[n, :] = random.multivariate_normal(A(X[n - 1, :]), G)
        c = 0
        while c < fixObsCount and random.uniform(0, 1) > sparsity:
            Y.append(random.multivariate_normal(A(X[n, :]), S))
            T.append(n)
            c += 1

    return (
     X, array(Y), array(T))


def testKalman(NT=20, XDim=2):
    L = 10
    X_grnd, Y, T = genKalman(NT=NT, XDim=XDim, L=L, sparsity=0.5)
    N = len(T)
    print 'shape(x_grnd)', shape(X_grnd)
    print 'shape(Y)', shape(Y)
    print 'shape(T)', shape(T)
    fixedParams = {'A': eye(XDim), 'G': 1.0 * eye(XDim), 
       'C': eye(XDim), 
       'S': 0.1 * eye(XDim), 
       'mu0': zeros(XDim), 
       'V0': 10.0 * eye(XDim)}
    KF = KalmanFilter(Y, T, N, fixed=fixedParams)
    KF.e()
    appl = lambda xs, ind, fn: fn([ fn(x[:, ind]) for x in xs ])
    As = [
     X_grnd, Y]
    x_min, x_max = appl(As, 0, min), appl(As, 0, max)
    y_min, y_max = appl(As, 1, min), appl(As, 1, max)
    pl = array([[x_min, x_max], [y_min, y_max]])
    kf_anim = KalmanAnim(T, KF, Y, grnd=X_grnd, plotLim=pl, F=0.1)
    print 'T', T
    for t in range(NT):
        kf_anim.update()
        time.sleep(5.0)


if __name__ == '__main__':
    testKalman()