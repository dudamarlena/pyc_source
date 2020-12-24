# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/pygp/demo/demo_gpr.py
# Compiled at: 2013-04-10 06:45:39
__doc__ = '\nApplication Example of GP regression\n====================================\n\nThis Example shows the Squared Exponential CF\n(:py:class:`covar.se.SEARDCF`) combined with noise\n:py:class:`covar.noise.noiseCF` by summing them up\n(using :py:class:`covar.combinators.sumCF`).\n'
import logging as LG, numpy.random as random
from pygp.covar import se, noise, combinators
import pygp.plot.gpr_plot as gpr_plot, pygp.priors.lnpriors as lnpriors, pylab as PL, scipy as SP
from pygp.likelihood.likelihood_base import GaussLikISO
from pygp.gp.gp_base import GP
from pygp.optimize.optimize_base import opt_hyper
import sys

def create_toy_data():
    n = 14
    xmin = 1
    xmax = 2.5 * SP.pi
    x = SP.linspace(xmin, xmax, n)
    C = 2
    sigma = 0.01
    b = 0
    y = b * x + C + 1 * SP.sin(x)
    y += sigma * random.randn(y.shape[0])
    y -= y.mean()
    x = x[:, SP.newaxis]
    x[SP.random.randint(n)] = SP.nan
    y[SP.random.randint(n)] = SP.nan
    return [
     x, y]


def run_demo():
    LG.basicConfig(level=LG.INFO)
    random.seed(1)
    x, y = create_toy_data()
    n_dimensions = 1
    X = SP.linspace(0, 10, 200)[:, SP.newaxis]
    likelihood = GaussLikISO()
    covar_parms = SP.log([1, 1])
    hyperparams = {'covar': covar_parms, 'lik': SP.log([1])}
    SECF = se.SqexpCFARD(n_dimensions=n_dimensions)
    covar = SECF
    covar_priors = []
    covar_priors.append([lnpriors.lnGammaExp, [1, 2]])
    covar_priors.extend([ [lnpriors.lnGammaExp, [1, 1]] for i in xrange(n_dimensions) ])
    lik_priors = []
    lik_priors.append([lnpriors.lnGammaExp, [1, 1]])
    priors = {'covar': covar_priors, 'lik': lik_priors}
    gp = GP(covar, likelihood=likelihood, x=x, y=y)
    gp.set_active_set_indices(slice(0, -2))
    opt_model_params = opt_hyper(gp, hyperparams, priors=priors, gradcheck=True, messages=False)[0]
    M, S = gp.predict(opt_model_params, X)
    gpr_plot.plot_sausage(X, M, SP.sqrt(S))
    gpr_plot.plot_training_data(x, y)
    PL.show()


if __name__ == '__main__':
    run_demo()