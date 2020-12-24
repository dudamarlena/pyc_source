# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/pygp/gp/gp_base.py
# Compiled at: 2013-07-02 10:08:30
__doc__ = '\nGaussian Process Package\n========================\n\nHolds all Gaussian Process classes, which hold all informations for a Gaussian Process to work porperly.\n\n.. class **GP**: basic class for GP regression:\n   * claculation of log marginal likelihood\n   * prediction\n   * data rescaling\n   * transformation into log space\n\n\n'
import copy, numpy.linalg as linalg
from pygp.linalg.linalg_matrix import jitChol, solve_chol
import logging, numpy
from scipy.linalg import lapack

class GP(object):
    """
    Gaussian Process regression class. Holds all information
    for the GP regression to take place.

    **Parameters:**

    covar_func : :py:class:`pygp.covar`
        The covariance function, which calculates the covariance
        of the outputs

    x : [double]
        training inputs (might be high dimensional,
        depending on which covariance function is chosen)
        Note: x must be of dimension `(-1,d)`

    y : [double]
        training targets of dimension `(-1,1)`

    Detailed descriptions of the fields of this class:

    ================================ ============ ===========================================
    Data                             Type/Default Explanation
    ================================ ============ ===========================================
    x                                array([])    inputs
    t                                array([])    targets
    n                                0            size of training data
    mean                             0            mean of the data

    **Settings:**

    **Covariance:**
    covar                            None         Covariance function

    **caching of covariance-stuff:**
    alpha                            None         cached alpha
    L                                None         chol(K)
    Nlogtheta                        0            total number of hyperparameters
                                                  for set kernel etc.
                                                  which if av. will be used
                                                  for predictions
    ================================ ============ ===========================================
    """
    __slots__ = [
     '_x', '_y', 'n', 'd', 'covar', 'likelihood',
     '_covar_cache', '_active_set_indices', '_active_set_indices_changed',
     '_xcache', '_ycache', '_finite_filter']

    def __init__(self, covar_func=None, likelihood=None, x=None, y=None):
        """GP(covar_func,likleihood,Smean=True,_x=None,_y=None)
        covar_func: Covariance
        likelihood: likelihood model
        _x/_y:        training input/targets
        """
        self._invalidate_cache()
        if x is not None and y is not None:
            self.setData(x=x, y=y)
        self.covar = covar_func
        self.likelihood = likelihood
        return

    def getData(self):
        """ Returns the data [x,y], currently set for this GP"""
        return [
         self._x, self._y]

    def setData(self, x, y):
        """
        setData(_x,t) with **Parameters:**

        x : inputs: [N x D]

        y : targets/outputs [N x d]
        #note d dimensional data structure only make sense for GPLVM
        """
        self._invalidate_cache()
        if x.ndim <= 1:
            x = x[:, None]
        if y.ndim <= 1:
            y = y[:, None]
        self._xcache = x
        self._ycache = y
        self._finite_filter = self._get_finite_filter(x, y)
        self._x = self._get_filtered(x)
        self._y = self._get_filtered(y)
        assert self._x.shape[0] == self._y.shape[0], 'input/target shape missmatch'
        self.n = self._x.shape[0]
        self.d = self._y.shape[1]
        return

    def set_active_set_indices(self, active_set_indices):
        if active_set_indices is None:
            active_set_indices = slice(None)
        self._active_set_indices_changed = True
        self._active_set_indices = active_set_indices
        if self._xcache is not None and self._ycache is not None:
            self._finite_filter = self._get_finite_filter(self._xcache, self._ycache)
        return

    def LML(self, hyperparams, priors=None):
        """
        Calculate the log Marginal likelihood
        for the given logtheta.

        **Parameters:**

        hyperparams : {'covar':CF_hyperparameters, ... }
            The hyperparameters for the log marginal likelihood.

        priors : [:py:class:`pygp.priors`]
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
        LML = self._LML_covar(hyperparams)
        if priors is not None:
            plml = self._LML_prior(hyperparams, priors=priors)
            LML -= numpy.array([ p[0, :].sum() for p in plml.values() ]).sum()
        return LML

    def LMLgrad(self, hyperparams, priors=None, **kw_args):
        """
        Returns the gradient of the log Marginal likelihood for the given hyperparameters hyperparams.

        **Parameters:**

        hyperparams : {'covar':CF_hyperparameters, ...}
            The hyperparameters which shall be optimized and derived

        priors : [:py:class:`pygp.priors`]
            Priors which shall be optimized and derived

        """
        RV = self._LMLgrad_covar(hyperparams)
        if self.likelihood is not None:
            RV.update(self._LMLgrad_lik(hyperparams))
        if priors is not None:
            plml = self._LML_prior(hyperparams, priors=priors, **kw_args)
            for key in RV.keys():
                RV[key] -= plml[key][1, :]

        return RV

    def get_covariances(self, hyperparams):
        """
        Return the Cholesky decompositions L and alpha::

            K
            L     = chol(K)
            alpha = solve(L,t)
            return [covar_struct] = get_covariances(hyperparam)

        **Parameters:**

        hyperparams: dict
            The hyperparameters for cholesky decomposition

        _x, _y: [double]
            input x and output _y for cholesky decomposition.
            If one/both is/are set, there will be no chaching allowed

        """
        if self._is_cached(hyperparams) and not self._active_set_indices_changed:
            pass
        else:
            Knoise = 0
            if self.likelihood is not None:
                Knoise = self.likelihood.K(hyperparams['lik'], self._x)
            K = self.covar.K(hyperparams['covar'], self._x)
            K += Knoise
            L = jitChol(K)[0].T
            alpha = solve_chol(L, self._y)
            Linv = lapack.dpotri(L)[0]
            Kinv = Linv.copy()
            numpy.fill_diagonal(Linv, 0)
            Kinv += Linv.T
            self._covar_cache = {'K': K, 'L': L, 'alpha': alpha, 'Kinv': Kinv}
            self._covar_cache['hyperparams'] = copy.deepcopy(hyperparams)
            self._active_set_indices_changed = False
        return self._covar_cache

    def predict(self, hyperparams, xstar, output=0, var=True):
        """
        Predict mean and variance for given **Parameters:**

        hyperparams : {}
            hyperparameters in logSpace

        xstar    : [double]
            prediction inputs

        var      : boolean
            return predicted variance

        interval_indices : [ int || bool ]
            Either numpy array-like of boolean indicators,
            or numpy array-like of integer indices, denoting
            which x indices to predict from data.

        output   : output dimension for prediction (0)
        """
        KV = self.get_covariances(hyperparams)
        Kstar = self.covar.K(hyperparams['covar'], self._x, xstar)
        mu = numpy.dot(Kstar.transpose(), KV['alpha'][:, output])
        if var:
            Kss_diag = self.covar.Kdiag(hyperparams['covar'], xstar)
            if self.likelihood is not None:
                Kss_diag += self.likelihood.Kdiag(hyperparams['lik'], xstar)
            v = linalg.solve(KV['L'], Kstar)
            S2 = Kss_diag - sum(v * v, 0).transpose()
            S2 = abs(S2)
            return [
             mu, S2]
        else:
            return mu
            return

    def _LML_covar(self, hyperparams):
        """

        log marginal likelihood contributions from covariance hyperparameters

        """
        try:
            KV = self.get_covariances(hyperparams)
        except linalg.LinAlgError:
            logging.error('exception caught (%s)' % str(hyperparams))
            return 1000000.0

        lml_quad = 0.5 * (KV['alpha'] * self._y).sum()
        lml_det = self._get_target_dimension() * numpy.log(KV['L'].diagonal()).sum()
        lml_const = 0.5 * self._get_target_dimension() * self._get_input_dimension() * numpy.log(2 * numpy.pi)
        return lml_quad + lml_det + lml_const

    def _LMLgrad_covar(self, hyperparams):
        logtheta = hyperparams['covar']
        try:
            KV = self.get_covariances(hyperparams)
        except linalg.LinAlgError:
            logging.error('exception caught (%s)' % str(hyperparams))
            return {'covar': numpy.zeros(len(logtheta))}

        alpha = KV['alpha']
        W = self._get_target_dimension() * KV['Kinv'] - numpy.dot(alpha, alpha.transpose())
        self._covar_cache['W'] = W
        LMLgrad = numpy.zeros(len(logtheta))
        for i in xrange(len(logtheta)):
            Kd = self.covar.Kgrad_theta(hyperparams['covar'], self._x, i)
            LMLgrad[i] = 0.5 * (W * Kd).sum()

        RV = {'covar': LMLgrad}
        return RV

    def _LMLgrad_lik(self, hyperparams):
        """derivative of the likelihood parameters"""
        logtheta = hyperparams['lik']
        KV = self._covar_cache
        W = KV['W']
        LMLgrad = numpy.zeros(len(logtheta))
        for i in xrange(len(logtheta)):
            Kd = self.likelihood.Kgrad_theta(logtheta, self._x, i)
            LMLgrad[i] = 0.5 * (W * Kd).sum()

        RV = {'lik': LMLgrad}
        return RV

    def _invalidate_cache(self):
        """reset cache structure"""
        self._active_set_indices = slice(None)
        self._active_set_indices_changed = False
        self._covar_cache = {}
        self._xcache = None
        self._ycache = None
        return

    def _LML_prior(self, hyperparams, priors={}):
        """calculate the prior contribution to the log marginal likelihood"""
        if priors is None:
            priors = {}
        RV = {}
        for key, value in hyperparams.iteritems():
            LL = list(value.shape)
            LL.insert(0, 2)
            pvalues = numpy.zeros(LL)
            if key == 'x':
                if key in priors:
                    plist = priors[key]
                    theta = hyperparams[key]
                    lng, dlng = plist[0](theta, plist[1])
                    pvalues[0] = lng
                    pvalues[1] = dlng
            elif key in priors:
                plist = priors[key]
                theta = copy.deepcopy(hyperparams[key])
                for i in xrange(len(theta)):
                    pvalues[:, i] = plist[i][0](theta[i], plist[i][1])

            RV[key] = pvalues

        return RV

    def _is_cached(self, hyperparams, keys=None):
        """check whether model parameters are cached"""
        if self._covar_cache is None:
            return False
        else:
            if 'hyperparams' not in self._covar_cache.keys():
                return False
            else:
                if keys is None:
                    keys = hyperparams.keys()
                for key in keys:
                    if not numpy.alltrue(self._covar_cache['hyperparams'][key] == hyperparams[key]):
                        return False

                return True

            return

    def _get_filtered(self, x):
        return x[self._active_set_indices][self._finite_filter, :]

    def _get_filtered_zeros(self, x, newx=None):
        if newx is None:
            newx = numpy.zeros_like(self._xcache)
        newx[self._active_set_indices][self._finite_filter, :] = x
        return newx

    def _get_finite_filter(self, x, y):
        return (~(~numpy.isfinite(x[self._active_set_indices])).any(1) * ~(~numpy.isfinite(y[self._active_set_indices])).any(1)).flatten()

    def _get_target_dimension(self):
        return self._y.shape[1]

    def _get_input_dimension(self):
        return self._x.shape[1]

    def plot(self, hyperparams):
        """
        plot current state of the model
        """
        raise NotImplementedError('Plotting not yet implemented')