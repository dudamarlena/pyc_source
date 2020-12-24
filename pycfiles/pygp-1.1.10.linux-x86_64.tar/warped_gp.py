# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/pygp/gp/warped_gp.py
# Compiled at: 2013-04-10 06:45:39
"""
Warped Gaussian processes base class, overriding gp_base
"""
from pygp.covar.bias import BiasCF
from pygp.gp.gp_base import GP
from pygp.optimize.optimize_base import opt_hyper
import logging as LG, scipy as SP
from pygp.likelihood.likelihood_base import GaussLikISO
from numpy.linalg import linalg

class MeanFunction(object):
    """
    abstract base clase for mean functions
    """

    def __init__(self):
        pass

    def f(self, psi):
        pass

    def fgrad_psi(self, psi):
        pass


class LinMeanFunction(MeanFunction):

    def __init__(self, X):
        self.X = X

    def f(self, psi):
        return SP.dot(self.X, psi)[:, SP.newaxis]

    def fgrad_psi(self, psi):
        return self.X


class WarpingFunction(object):
    """
    abstract function for warping
    z = f(y) 
    """

    def __init__(self):
        pass

    def f(self, y, psi):
        """function transformation
        y is a list of values (GP training data) of shpape [N,1]
        """
        pass

    def fgrad_y(self, y, psi):
        """gradient of f w.r.t to y"""
        pass

    def fgrad_y_psi(self, y, psi):
        """gradient of f w.r.t to y"""
        pass

    def f_inv(self, z, psi):
        """inverse function transformation"""
        pass

    def get_bounds(self, bounds_dict):
        """ returns the optimization bounds for the warping function """
        pass


class TanhWarpingFunction(WarpingFunction):
    """implementaiton of the tanh warping fuction thing from Ed Snelson"""

    def __init__(self, n_terms=3):
        """n_terms specifies the number of tanh terms to be used"""
        self.n_terms = n_terms

    def f(self, y, psi):
        r"""transform y with f using parameter vector psi
        psi = [[a,b,c]]
        f = \sum_{terms} a * tanh(b*(y+c))
        """
        assert psi.shape[0] == self.n_terms, 'inconsistent parameter dimensions'
        assert psi.shape[1] == 3, 'inconsistent parameter dimensions'
        mpsi = psi.copy()
        mpsi[:, 0:2] = SP.exp(mpsi[:, 0:2])
        z = y.copy()
        for i in range(len(mpsi)):
            a, b, c = mpsi[i]
            z += a * SP.tanh(b * (y + c))

        return z

    def f_inv(self, y, psi, iterations=10):
        """
        calculate the numerical inverse of f

        == input ==
        iterations: number of N.R. iterations
        
        """
        y = y.copy()
        z = self.f(y, psi)
        for i in range(iterations):
            y -= (self.f(y, psi) - z) / self.fgrad_y(y, psi)

        return y

    def fgrad_y(self, y, psi, return_precalc=False):
        """
        gradient of f w.r.t to y ([N x 1])
        returns: Nx1 vector of derivatives, unless return_precalc is true,
        then it also returns the precomputed stuff
        """
        mpsi = psi.copy()
        mpsi[:, 0:2] = SP.exp(mpsi[:, 0:2])
        s = SP.zeros((len(psi), y.shape[0], y.shape[1]))
        r = SP.zeros((len(psi), y.shape[0], y.shape[1]))
        d = SP.zeros((len(psi), y.shape[0], y.shape[1]))
        grad = 1
        for i in range(len(mpsi)):
            a, b, c = mpsi[i]
            s[i] = b * (y + c)
            r[i] = SP.tanh(s[i])
            d[i] = 1 - r[i] ** 2
            grad += a * b * d[i]

        S = (mpsi[:, 1] * (y + mpsi[:, 2])).T
        R = SP.tanh(S)
        D = 1 - R ** 2
        GRAD = (1 + (mpsi[:, 0:1] * mpsi[:, 1:2] * D).sum(axis=0))[:, SP.newaxis]
        if return_precalc:
            return (GRAD, S, R, D)
        return grad

    def fgrad_y_psi(self, y, psi, return_covar_chain=False):
        """
        gradient of f w.r.t to y and psi

        returns: NxIx3 tensor of partial derivatives

        """
        mpsi = psi.copy()
        mpsi[:, 0:2] = SP.exp(mpsi[:, 0:2])
        w, s, r, d = self.fgrad_y(y, psi, return_precalc=True)
        gradients = SP.zeros((y.shape[0], len(mpsi), 3))
        for i in range(len(mpsi)):
            a, b, c = mpsi[i]
            gradients[:, i, 0] = a * (b * (1.0 / SP.cosh(s[i])) ** 2).flatten()
            gradients[:, i, 1] = b * (a * (1 - 2 * s[i] * r[i]) * (1.0 / SP.cosh(s[i])) ** 2).flatten()
            gradients[:, i, 2] = (-2 * a * b ** 2 * r[i] * (1.0 / SP.cosh(s[i])) ** 2).flatten()

        covar_grad_chain = SP.zeros((y.shape[0], len(mpsi), 3))
        import numpy as NP
        for i in range(len(mpsi)):
            a, b, c = mpsi[i]
            covar_grad_chain[:, i, 0] = a * r[i]
            covar_grad_chain[:, i, 1] = b * (a * (c + y[:, 0]) * (1.0 / SP.cosh(s[i])) ** 2)
            covar_grad_chain[:, i, 2] = a * b * ((1.0 / SP.cosh(s[i])) ** 2).flatten()

        if return_covar_chain:
            return (gradients, covar_grad_chain)
        return gradients

    def get_bounds(self, bounds_dict=None):
        """
        Optimization bounds for the warping function. Returns a dictionary
        that contains (n_terms*3, 2) bounds (flattened)

        Input:

        bounds_dict -> dictionary containing existing bounds (default None)
        
        """
        if bounds_dict == None:
            bounds_dict = {}
        bounds = SP.zeros((self.n_terms, 3, 2))
        bounds[:, :, 0] = -SP.inf
        bounds[:, :, 1] = +SP.inf
        bounds[:, 1, 0] = -SP.inf
        bounds[:, 1, 1] = SP.log(20)
        bounds = bounds.reshape((bounds.shape[0] * bounds.shape[1], 2))
        bounds_dict['warping'] = bounds.tolist()
        return bounds_dict


class WARPEDGP(GP):
    __slots__ = [
     'warping_function', 'mean_function']

    def __init__(self, warping_function=None, mean_function=None, **kw_args):
        """warping_function: warping function of type WarpingFunction"""
        self.warping_function = warping_function
        self.mean_function = mean_function
        super(WARPEDGP, self).__init__(**kw_args)

    def _get_y(self, hyperparams):
        """get_y return the effect y being used"""
        y_ = self._get_active_set(self.y)
        if self.warping_function is not None:
            y_ = self.warping_function.f(y_, hyperparams['warping'])
        if self.mean_function is not None:
            y_ = y_ - self.mean_function.f(hyperparams['mean'])
        return y_

    def LML(self, hyperparams, *args, **kw_args):
        """
        Calculate the log Marginal likelihood
        for the given logtheta.

        **Parameters:**

        hyperparams : {'covar':CF_hyperparameters, ... }
            The hyperparameters for the log marginal likelihood.

        priors : [:py:class:`lnpriors`]
            the prior beliefs for the hyperparameter values

        Ifilter : [bool]
            Denotes which hyperparameters shall be optimized.
            Thus ::

                Ifilter = [0,1,0]

            has the meaning that only the second
            hyperparameter shall be optimized.

        kw_args :
            All other arguments, explicitly annotated
            when necessary.  
        """
        LML = super(WARPEDGP, self).LML(hyperparams, *args, **kw_args)
        if self.warping_function is not None:
            warping_grad_y = self.warping_function.fgrad_y(self._get_active_set(self.y), hyperparams['warping'])
            LML -= SP.log(warping_grad_y).sum()
        return LML

    def LMLgrad(self, hyperparams, *args, **kw_args):
        RV = super(WARPEDGP, self).LMLgrad(hyperparams, *args, **kw_args)
        if self.warping_function is not None:
            RV.update(self._LMLgrad_warping(hyperparams))
        if self.mean_function is not None:
            RV.update(self._LMLgrad_mean(hyperparams))
        return RV

    def predict(self, hyperparams, xstar, output=0, var=True):
        R = super(WARPEDGP, self).predict(hyperparams, xstar, output, var)
        if self.mean_function is not None:
            mean = self.mean_function.f(hyperparams['mean'])
            if var:
                R[0] += mean[:, 0]
            else:
                R += mean[:, 0]
        return R

    def _LMLgrad_mean(self, hyperparams):
        grad_f_psi = self.mean_function.fgrad_psi(hyperparams['mean'])
        Kiy = super(WARPEDGP, self).get_covariances(hyperparams)['alpha']
        mean_grad_quad = -1.0 * SP.dot(grad_f_psi.T, Kiy[:, 0]).T
        RV = {'mean': mean_grad_quad}
        return RV

    def _LMLgrad_warping(self, hyperparams):
        """gradient with respect to warping function parameters"""
        grad_y = self.warping_function.fgrad_y(self._get_active_set(self.y), hyperparams['warping'])
        grad_y_psi, grad_psi = self.warping_function.fgrad_y_psi(self._get_active_set(self.y), hyperparams['warping'], return_covar_chain=True)
        Igrad_y_psi = SP.tile((1.0 / grad_y)[:, :, SP.newaxis], (1, grad_psi.shape[1], grad_psi.shape[2]))
        warp_grad_det = -(Igrad_y_psi * grad_y_psi).sum(axis=0)
        Kiy = super(WARPEDGP, self).get_covariances(hyperparams)['alpha']
        warp_grad_quad = SP.dot(grad_psi.T, Kiy[:, 0]).T
        RV = {'warping': warp_grad_quad + warp_grad_det}
        return RV


if __name__ == '__main__':
    import pylab as PL
    from pygp.covar import se
    import pygp.plot.gpr_plot as gpr_plot, pygp.priors.lnpriors as lnpriors, pygp.likelihood as lik, pygp.plot.gpr_plot as gpr_plot, pygp.priors.lnpriors as lnpriors
    LG.basicConfig(level=LG.DEBUG)
    SP.random.seed(10)
    n_dimensions = 1
    xmin, xmax = 1, 2.5 * SP.pi
    x = SP.linspace(xmin, xmax, 500)
    print len(x)
    X = SP.linspace(0, 10, 100)[:, SP.newaxis]
    b = 1
    C = 0
    SNR = 0.1
    y = b * x + C + 1 * SP.sin(x)
    sigma = SNR * (y.max() - y.mean())
    y += sigma * SP.random.randn(len(x))
    x = x[:, SP.newaxis]

    def trafo(y):
        return y ** float(3)


    def Itrafo(y):
        return y ** (1 / float(3))


    z = trafo(y)
    L = z.max() - z.min()
    z /= L
    n_terms = 3
    likelihood = GaussLikISO()
    covar_parms = SP.log([1, 1])
    hyperparams = {'covar': covar_parms, 'lik': SP.log([sigma])}
    SECF = se.SqexpCFARD(n_dimensions=n_dimensions)
    muCF = BiasCF(n_dimensions=n_dimensions)
    covar = SECF
    warping_function = None
    mean_function = None
    bounds = {}
    warping_function = TanhWarpingFunction(n_terms=n_terms)
    hyperparams['warping'] = 0.01 * SP.random.randn(n_terms, 3)
    bounds.update(warping_function.get_bounds())
    gp = WARPEDGP(warping_function=warping_function, mean_function=mean_function, covar_func=covar, likelihood=likelihood, x=x, y=z)
    if warping_function is not None:
        PL.figure(1)
        z_values = SP.linspace(z.min(), z.max(), 100)
        PL.plot(z_values, Itrafo(L * z_values))
        PL.plot(z_values, warping_function.f(z_values, hyperparams['warping']))
        PL.legend('real inverse', 'learnt inverse')
    lmld = gp.LMLgrad(hyperparams)
    print lmld
    opt_model_params = opt_hyper(gp, hyperparams, bounds=bounds, maxiter=10000, gradcheck=True)[0]
    PL.figure(2)
    z_values = SP.linspace(z.min(), z.max(), 100)
    PL.plot(Itrafo(gp.y))
    pred_inverse = warping_function.f_inv(gp.y, opt_model_params['warping'], iterations=10)
    PL.plot(pred_inverse)