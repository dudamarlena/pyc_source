# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/pygp/demo/demo_warped.py
# Compiled at: 2013-04-10 06:45:39
import logging as LG
from pygp.gp.warped_gp import WARPEDGP, TanhWarpingFunction, LinMeanFunction
from pygp.covar import se, combinators
import pygp.likelihood as lik, pygp.optimize as opt, pylab as PL, scipy as SP
from pygp.likelihood.likelihood_base import GaussLikISO
from pygp.covar.bias import BiasCF
from pygp.optimize.optimize_base import opt_hyper
from pygp.gp.gp_base import GP

def trafo(y):
    return y ** float(3)


def Itrafo(y):
    return y ** (1 / float(3))


def create_toy_data():
    xmin, xmax = 1, 2.5 * SP.pi
    x = SP.linspace(xmin, xmax, 500)
    print len(x)
    X = SP.linspace(0, 10, 100)[:, SP.newaxis]
    b = 1
    C = 2
    SNR = 0.1
    y = b * x + C + 1 * SP.sin(x)
    sigma = SNR * (y.max() - y.mean())
    y += sigma * SP.random.randn(len(x))
    x = x[:, SP.newaxis]
    z = trafo(y)
    L = z.max() - z.min()
    z /= L
    return (
     x, y, z, sigma, X, Itrafo(z), L)


def run_demo():
    LG.basicConfig(level=LG.DEBUG)
    SP.random.seed(10)
    x, y, z, sigma, X, actual_inv, L = create_toy_data()
    n_dimensions = 1
    n_terms = 3
    likelihood = GaussLikISO()
    covar_parms = SP.log([1, 1, 1e-05])
    hyperparams = {'covar': covar_parms, 'lik': SP.log([sigma]), 'warping': 0.01 * SP.random.randn(n_terms, 3)}
    SECF = se.SqexpCFARD(n_dimensions=n_dimensions)
    covar = combinators.SumCF([SECF, BiasCF(n_dimensions=n_dimensions)])
    warping_function = TanhWarpingFunction(n_terms=n_terms)
    mean_function = LinMeanFunction(X=SP.ones([x.shape[0], 1]))
    hyperparams['mean'] = 0.01 * SP.randn(1)
    bounds = {}
    bounds.update(warping_function.get_bounds())
    gp = WARPEDGP(warping_function=warping_function, mean_function=mean_function, covar_func=covar, likelihood=likelihood, x=x, y=z)
    opt_model_params = opt_hyper(gp, hyperparams, bounds=bounds, gradcheck=True)[0]
    print 'WARPED GP (neg) likelihood: ', gp.LML(hyperparams)
    PL.figure()
    PL.plot(z)
    PL.plot(warping_function.f(y, hyperparams['warping']))
    PL.legend(['real function', 'larnt function'])
    PL.figure()
    PL.plot(actual_inv)
    PL.plot(warping_function.f_inv(gp.y, hyperparams['warping']))
    PL.legend(['real inverse', 'learnt inverse'])
    hyperparams.pop('warping')
    hyperparams.pop('mean')
    gp = GP(covar, likelihood=likelihood, x=x, y=y)
    opt_model_params = opt_hyper(gp, hyperparams, gradcheck=False)[0]
    print 'GP (neg) likelihood: ', gp.LML(hyperparams)


if __name__ == '__main__':
    run_demo()