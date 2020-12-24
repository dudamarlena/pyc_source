# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/pygp/demo/demo_gplvm.py
# Compiled at: 2013-04-10 06:45:39
"""
Demo Application for Gaussian process latent variable models
====================================

"""
import logging as LG, numpy as NP
from pygp.gp import gplvm
from pygp.covar import linear, se
from pygp.util.pca import PCA
from pygp.likelihood.likelihood_base import GaussLikISO
from pygp.optimize.optimize_base import opt_hyper
import copy, scipy as SP, pylab
from pygp.priors import lnpriors
N = 20
K = 3
D = 500

def run_demo():
    LG.basicConfig(level=LG.INFO)
    SP.random.seed(1)
    t = SP.linspace(0, 2 * SP.pi, N)[:, None]
    t = SP.tile(t, K)
    t += SP.linspace(SP.pi / 4.0, 3.0 / 4.0 * SP.pi, K)
    S = 0.5 * t + 1.2 + SP.sin(t)
    W = SP.random.randn(K, D)
    Y = SP.dot(S, W)
    Y += 0.2 * SP.random.randn(N, D)
    pc = PCA(Y)
    Spca = pc.project(Y, K)
    covariance = linear.LinearCF(n_dimensions=K)
    hyperparams = {'covar': SP.log([2] * K)}
    X0 = SP.random.randn(N, K)
    hyperparams['x'] = copy.deepcopy(X0)
    priors = {'x': [lnpriors.lnFobgp, [10000]]}
    likelihood = GaussLikISO()
    hyperparams['lik'] = SP.log(SP.sqrt([0.5]))
    g = gplvm.GPLVM(covar_func=covariance, likelihood=likelihood, x=copy.deepcopy(X0), y=Y, gplvm_dimensions=SP.arange(X0.shape[1]))
    bounds = {}
    bounds['lik'] = SP.array([[-10.0, 10.0]])
    hyperparams['x'] = X0
    print 'running standard gplvm'
    Ifilter = {}
    Ifilter['covar'] = SP.array([False])
    Ifilter['lik'] = SP.ones(hyperparams['lik'].shape, dtype='bool')
    Ifilter['x'] = SP.ones(hyperparams['x'].shape, dtype='bool')
    Ifilter = None
    opt_hyperparams, opt_lml2 = opt_hyper(g, copy.deepcopy(hyperparams), messages=True, gradcheck=False, priors=priors, bounds=bounds, Ifilter=Ifilter)
    Sgplvm = opt_hyperparams['x']
    K_learned = covariance.K(opt_hyperparams['covar'], Sgplvm)
    vmax = None
    vmin = None
    cmap = pylab.get_cmap('gray')
    pylab.ion()
    ax1 = pylab.subplot(131)
    pylab.title('Truth')
    pylab.imshow(SP.dot(S, S.T), cmap=cmap, interpolation='bilinear', vmin=vmin, vmax=vmax, aspect='auto')
    pylab.xlabel('Sample')
    pylab.ylabel('Sample')
    ax2 = pylab.subplot(132, sharex=ax1, sharey=ax1)
    pylab.title('GPLVM')
    pylab.imshow(K_learned, cmap=cmap, interpolation='bilinear', vmin=vmin, vmax=vmax, aspect='auto')
    pylab.xlabel('Sample')
    pylab.setp(ax2.get_yticklabels(), visible=False)
    ax3 = pylab.subplot(133, sharex=ax1, sharey=ax1)
    pylab.title('PCA')
    pylab.imshow(SP.dot(Spca, Spca.T), cmap=cmap, interpolation='bilinear', vmin=vmin, vmax=vmax, aspect='auto')
    pylab.xlabel('Sample')
    pylab.setp(ax3.get_yticklabels(), visible=False)
    pylab.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.05, hspace=None)
    return (
     g, hyperparams, opt_hyperparams, S, Spca, Sgplvm)


if __name__ == '__main__':
    pylab.close('all')
    g, hyperparams, opt_hyperparams, S, Spca, Sgplvm = run_demo()
    pearson_pca = SP.zeros((K, K))
    pearson_gplvm = SP.zeros((K, K))
    import scipy.stats
    for k in xrange(K):
        for kprime in xrange(K):
            pearson_pca[(k, kprime)] = scipy.stats.pearsonr(S[:, k], Spca[:, kprime])[0]
            pearson_gplvm[(k, kprime)] = scipy.stats.pearsonr(S[:, k], Sgplvm[:, kprime])[0]

    print 'PCA correlations:\t', SP.absolute(pearson_pca).max(0)
    print 'GPLVM correlations:\t', SP.absolute(pearson_gplvm).max(0)
    X = opt_hyperparams['x']