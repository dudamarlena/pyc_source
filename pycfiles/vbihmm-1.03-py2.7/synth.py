# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/vb_ihmm/testing/synth.py
# Compiled at: 2013-10-31 11:59:11
"""
Created on 3 Oct 2013

@author: James McInerney
"""
from numpy import *

def genHMM(N, K, XDim=2, mu_sd_factor=1, L=10, sequential=1):
    X = zeros((N, XDim))
    Y = zeros((N, L))
    Z = zeros((N, K))
    alpha = 0.05 * ones((K, K)) + eye(K)
    beta = 10.0
    mu0 = zeros(XDim)
    muC0 = eye(XDim)
    C0a, C0b = (1.0, 0.9)
    pik = random.dirichlet(beta * ones(K))
    A = alpha / reshape(alpha.sum(axis=1), (K, 1))
    mu = array([ random.multivariate_normal(zeros(XDim), mu_sd_factor * eye(XDim)) for _ in range(K) ])
    C = array([ 0.1 * eye(XDim) for _ in range(K) ])
    pr_y = array([ random.dirichlet(0.1 * ones(L)) for _ in range(K) ])
    for n in range(N):
        if not sequential or n == 0:
            Z[n, :] = random.multinomial(1, pik)
        else:
            prev_z = Z[n - 1, :].argmax()
            Z[n, :] = random.multinomial(1, A[prev_z, :])
        z_n = Z[n, :].argmax()
        X[n, :] = random.multivariate_normal(mu[z_n, :], C[z_n, :, :])
        Y[n, :] = random.multinomial(1, pr_y[z_n, :])

    print 'ground latent states', Z.argmax(axis=1)
    return (X, Y, mu)


def genHMM1(N, K, XDim=2, mu_sd_factor=1):
    X = zeros((N, XDim))
    Z = zeros((N, K))
    alpha = 0.05 * ones((K, K)) + eye(K)
    beta = 0.1
    mu0 = zeros(XDim)
    muC0 = eye(XDim)
    C0a, C0b = (1.0, 0.9)
    pik = random.dirichlet(beta * ones(K))
    A = alpha / reshape(alpha.sum(axis=1), (K, 1))
    mu = array([ random.multivariate_normal(zeros(XDim), mu_sd_factor * eye(XDim)) for _ in range(K) ])
    C = array([ 0.1 * eye(XDim) for _ in range(K) ])
    for n in range(N):
        if n == 0:
            Z[n, :] = random.multinomial(1, pik)
        else:
            prev_z = Z[n - 1, :].argmax()
            Z[n, :] = random.multinomial(1, A[prev_z, :])
        z_n = Z[n, :].argmax()
        X[n, :] = random.multivariate_normal(mu[z_n, :], C[z_n, :, :])

    return (X, Z, A, mu)