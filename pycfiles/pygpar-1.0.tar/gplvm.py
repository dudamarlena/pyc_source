# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/pygp/gp/gplvm.py
# Compiled at: 2013-04-10 06:45:39
__doc__ = '\nBase class for Gaussian process latent variable models\nThis is really not ready for release yet but is used by the gpasso model\n'
import sys
from pygp.gp.gp_base import GP
sys.path.append('./../..')
from pygp.optimize.optimize_base import opt_hyper
import scipy as SP, scipy.linalg as linalg

def PCA(Y, components):
    """run PCA, retrieving the first (components) principle components
    return [s0, eig, w0]
    s0: factors
    w0: weights
    """
    sv = linalg.svd(Y, full_matrices=0)
    s0, w0 = sv[0][:, 0:components], SP.dot(SP.diag(sv[1]), sv[2]).T[:, 0:components]
    v = s0.std(axis=0)
    s0 /= v
    w0 *= v
    return [
     s0, w0]


class GPLVM(GP):
    """
    derived class form GP offering GPLVM specific functionality
    
    
    """
    __slots__ = [
     'gplvm_dimensions']

    def __init__(self, gplvm_dimensions=None, **kw_args):
        """gplvm_dimensions: dimensions to learn using gplvm, default -1; i.e. all"""
        self.gplvm_dimensions = gplvm_dimensions
        super(GPLVM, self).__init__(**kw_args)

    def setData(self, gplvm_dimensions=None, **kw_args):
        GP.setData(self, **kw_args)
        if self.gplvm_dimensions is None and gplvm_dimensions is None:
            self.gplvm_dimensions = SP.arange(self._x.shape[1])
        elif gplvm_dimensions is not None:
            self.gplvm_dimensions = gplvm_dimensions
        return

    def _update_inputs(self, hyperparams):
        """update the inputs from gplvm models if supplied as hyperparms"""
        if 'x' in hyperparams.keys():
            self._x[:, self.gplvm_dimensions] = self._get_filtered(hyperparams['x'])

    def LML(self, hyperparams, priors=None, **kw_args):
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
        self._update_inputs(hyperparams)
        LML = self._LML_covar(hyperparams)
        if priors is not None:
            plml = self._LML_prior(hyperparams, priors=priors, **kw_args)
            LML -= SP.array([ p[0, :].sum() for p in plml.values() ]).sum()
        return LML

    def LMLgrad(self, hyperparams, priors=None, **kw_args):
        """
        Returns the log Marginal likelihood for the given logtheta.

        **Parameters:**

        hyperparams : {'covar':CF_hyperparameters, ...}
            The hyperparameters which shall be optimized and derived

        priors : [:py:class:`lnpriors`]
            The hyperparameters which shall be optimized and derived

        """
        self._update_inputs(hyperparams)
        RV = self._LMLgrad_covar(hyperparams)
        if self.likelihood is not None:
            RV.update(self._LMLgrad_lik(hyperparams))
        RV_ = self._LMLgrad_x(hyperparams)
        RV.update(RV_)
        if priors is not None:
            plml = self._LML_prior(hyperparams, priors=priors, **kw_args)
            for key in RV.keys():
                RV[key] -= plml[key][1]

        return RV

    def _LMLgrad_x(self, hyperparams):
        """GPLVM derivative w.r.t. to latent variables
        """
        if 'x' not in hyperparams:
            return {}
        dlMl = SP.zeros([self.n, len(self.gplvm_dimensions)])
        W = self._covar_cache['W']
        for i in xrange(len(self.gplvm_dimensions)):
            d = self.gplvm_dimensions[i]
            dKx = self.covar.Kgrad_x(hyperparams['covar'], self._x, self._x, d)
            dKx_diag = self.covar.Kgrad_xdiag(hyperparams['covar'], self._x, d)
            dKx.flat[::dKx.shape[1] + 1] = dKx_diag
            WK = W * dKx
            dlMl[:, i] = 0.5 * (2 * WK.sum(axis=1) - WK.diagonal())

        RV = {'x': self._get_filtered_zeros(dlMl, SP.zeros((self._xcache.shape[0], len(self.gplvm_dimensions))))}
        return RV


if __name__ == '__main__':
    from pygp.covar import linear, noise, fixed, combinators
    import logging as LG
    LG.basicConfig(level=LG.DEBUG)
    SP.random.seed(1)
    N = 100
    K = 3
    D = 10
    S = SP.random.randn(N, K)
    W = SP.random.randn(D, K)
    Y = SP.dot(W, S.T).T
    Y += 0.5 * SP.random.randn(N, D)
    Spca, Wpca = PCA(Y, K)
    Y_ = SP.dot(Spca, Wpca.T)
    linear_cf = linear.LinearCFISO(n_dimensions=K)
    noise_cf = noise.NoiseCFISO()
    mu_cf = fixed.FixedCF(SP.ones([N, N]))
    covariance = combinators.SumCF((mu_cf, linear_cf, noise_cf))
    X = Spca.copy()
    gplvm = GPLVM(covar_func=covariance, x=X, y=Y)
    gpr = GP(covar_func=covariance, x=X, y=Y[:, 0])
    covar = SP.log([0.1, 1.0, 0.1])
    X_ = X.copy()
    hyperparams = {'covar': covar, 'x': X_}
    lml = gplvm.LML(hyperparams=hyperparams)
    opt_model_params, opt_lml = opt_hyper(gplvm, hyperparams, gradcheck=False)
    Xo = opt_model_params['x']
    for k in xrange(K):
        print SP.corrcoef(Spca[:, k], S[:, k])

    print '=================='
    for k in xrange(K):
        print SP.corrcoef(Xo[:, k], S[:, k])