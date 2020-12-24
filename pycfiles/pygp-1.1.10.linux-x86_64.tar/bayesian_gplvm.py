# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/pygp/gp/bayesian_gplvm.py
# Compiled at: 2013-04-10 06:45:39
"""
Created on 4 Apr 2012

@author: maxz
"""
from copy import deepcopy
from pygp.gp.gp_base import GP
from pygp.linalg.linalg_matrix import jitChol
import numpy, scipy, copy, itertools
from scipy.linalg import LinAlgError
from pygp.util.pca import PCA
from pygp.optimize.optimize_base import opt_hyper
mean_id = 'x'
vars_id = 'S'
ivar_id = 'Xm'

class BayesianGPLVM(GP):
    """Bayesian GPLVM"""

    def __init__(self, y, covar_func, gplvm_dimensions=None, n_inducing_variables=10, **kw_args):
        """gplvm_dimensions: dimensions to learn using gplvm, default -1; i.e. all"""
        super(BayesianGPLVM, self).__init__(covar_func=covar_func, y=y, **kw_args)
        self.setData(y, gplvm_dimensions=gplvm_dimensions, n_inducing_variables=n_inducing_variables, **kw_args)
        self.constant_jitter = 0.0
        self.constant_jitter_Atilde = 0.0

    def predict(self, hyperparams, xstar, var=True):
        self.update_stats(hyperparams)
        hyperparams_star = copy.deepcopy(hyperparams)
        hyperparams_star[mean_id] = xstar
        hyperparams_star[vars_id] = numpy.log(numpy.sqrt(numpy.ones_like(xstar) * 1e-24))
        N = xstar.shape[0]
        self.covar.update_stats(hyperparams_star['covar'], hyperparams_star[mean_id], hyperparams_star[vars_id], hyperparams_star[ivar_id])
        psi0_star, psi1_star, psi2_star = self.covar.psi()
        Ainv = numpy.dot(self._P1.T, self._P1)
        alpha = numpy.dot(Ainv, numpy.dot(self._psi_1.T, self._y))
        mean = numpy.dot(psi1_star, alpha)
        varsigma = numpy.zeros((N, self.d))
        if var:
            KinvK = self._KmmInv - numpy.dot(self._beta_inv, Ainv)
            for i in xrange(N):
                self.covar.update_stats(hyperparams_star['covar'], hyperparams_star[mean_id][i:i + 1, :], hyperparams_star[vars_id][i:i + 1, :], hyperparams_star[ivar_id])
                psi0_star, psi1_star, psi2_star = self.covar.psi()
                vars = psi0_star - (KinvK * psi2_star).sum()
                for j in xrange(self.d):
                    varsigma[(i, j)] = numpy.dot(alpha[:, j:j + 1].T, numpy.dot(psi2_star, alpha[:, j]))
                    varsigma[(i, j)] -= mean[(i, j)] ** 2

                varsigma[i, :] += vars

            varsigma = varsigma + self._beta_inv
            self.covar.update_stats(hyperparams['covar'], hyperparams[mean_id], hyperparams[vars_id], hyperparams[ivar_id])
            return (
             mean, varsigma)
        self.covar.update_stats(hyperparams['covar'], hyperparams[mean_id], hyperparams[vars_id], hyperparams[ivar_id])
        return mean

    def setData(self, y, x=None, gplvm_dimensions=None, n_inducing_variables=None, training_labels=None, **kw_args):
        self.gplvm_dimensions = gplvm_dimensions
        self._y = y
        if x is not None:
            self._x = x
        self.n = self._y.shape[0]
        self.d = self._y.shape[1]
        self._invalidate_cache()
        if n_inducing_variables is not None:
            self.m = n_inducing_variables
        self.TrYY = numpy.trace(numpy.dot(y, y.T))
        return

    def LML(self, hyperparams, priors=None, **kw_args):
        """
        For Bayesian GPLVM we introduce a lower bound on
        the marginal likelihood approximating the true
        marginal likelihood through a variational distribution q
        """
        is_cached = self._is_cached(hyperparams)
        if is_cached and not self._active_set_indices_changed and 'bound' in self._covar_cache.keys():
            pass
        else:
            if not is_cached:
                self.update_stats(hyperparams)
            var_bound = self._compute_variational_bound(hyperparams)
            kl_bound = self._compute_kl_divergence(hyperparams)
            bound = var_bound + kl_bound
            self._covar_cache['bound'] = -bound
        bound = self._covar_cache['bound']
        return bound

    def LMLgrad(self, hyperparams, hyperparam_keys=None, add_KLgrad=True, *args, **kw_args):
        """
        gradients w.r.t elements in gradient_keys.
        If gradient_keys is None all gradients will be returned!
        """
        is_cached = self._is_cached(hyperparams)
        if is_cached and not self._active_set_indices_changed and 'grad' in hyperparams.keys():
            pass
        else:
            if not is_cached:
                self.update_stats(hyperparams)
            if not self._covar_cache.has_key('grad'):
                self._covar_cache['grad'] = dict.fromkeys(hyperparams.keys(), 0)
            LMLgrad = self._covar_cache['grad']
            if hyperparam_keys is None:
                hyperparam_keys = hyperparams.keys()
            for k in hyperparam_keys:
                LMLgrad[k] = getattr(self, '_LMLgrad_%s' % k)(hyperparams)
                if add_KLgrad:
                    LMLgrad[k] += getattr(self, '_KLgrad_%s' % k)()

            self._covar_cache['grad'] = LMLgrad
        return self._covar_cache['grad']

    def optimize(self, initial_hyperparams, bounds=None, burniniter=200, gradient_tolerance=1e-15, maxiter=15000.0, release_beta=True):
        ifilter = self.get_filter(initial_hyperparams)
        for key in ifilter.iterkeys():
            if key.startswith('beta'):
                ifilter[key][:] = 0

        hyperparams, _ = opt_hyper(self, initial_hyperparams, gradient_tolerance=gradient_tolerance, maxiter=burniniter, Ifilter=ifilter, bounds=bounds)
        if release_beta:
            hyperparams, _ = opt_hyper(self, hyperparams, gradient_tolerance=gradient_tolerance, bounds=bounds, maxiter=maxiter)
        return hyperparams

    def get_filter(self, hyperparams):
        filter_ = {}
        for key, val in hyperparams.iteritems():
            filter_[key] = numpy.ones_like(val)

        return filter_

    def get_bounds(self, hyperparams, beta=(1.0, 150.0)):
        covar = self.covar
        bounds = {}
        if 'beta' in hyperparams.keys():
            bounds['beta'] = [
             beta]
        if vars_id in hyperparams.keys():
            bounds[vars_id] = [
             (
              0.5 * numpy.log(1e-08), 0.5 * numpy.log(10))] * hyperparams[vars_id].size
        covar_lower_bounds = [1e-08] * covar.get_number_of_parameters()
        covar_lower_bounds[-1] = 0.001
        covar_lower_bounds = covar.get_de_reparametrized_theta(numpy.array(covar_lower_bounds))
        covar_upper_bounds = [
         10] * covar.get_number_of_parameters()
        covar_upper_bounds = covar.get_de_reparametrized_theta(numpy.array(covar_upper_bounds))
        covar_bounds = numpy.array(zip(covar_lower_bounds, covar_upper_bounds))
        covar_bounds.sort(1)
        bounds['covar'] = covar_bounds
        return bounds

    def inithyperparams(self, Qlearn, beta=75.0):
        covar = self.covar
        M = self.m
        Y = self._y
        p = PCA(Y)
        mean = p.project(Y, Qlearn)
        variance = 0.5 * numpy.log(0.5 * numpy.ones(mean.shape))
        inducing_variables = (numpy.random.rand(M, Qlearn) - 0.5) * (mean.max() - mean.min())
        covar_hyp = 0.3 + 0.6 * numpy.random.rand(covar.get_number_of_parameters())
        covar_hyp[covar.get_ard_dimension_indices()] = p.fracs
        hyperstart = {'covar': covar.get_de_reparametrized_theta(covar_hyp), 'beta': numpy.array([float(beta)]), 
           mean_id: mean, 
           vars_id: variance, 
           ivar_id: inducing_variables}
        return hyperstart

    def _LMLgrad_wrt(self, Kgrad, psi_0grad, psi_1grad, psi_2grad, psi1ax1=-1, psi1ax2=-1):
        betahalf = self._beta / 2.0
        gKern0 = -betahalf * self.d * psi_0grad
        gKern1 = self._beta * (psi_1grad.T * self._yB.T[None, None, :, :]).sum(psi1ax1).sum(psi1ax2).T
        gKern2 = betahalf * (psi_2grad.T * self._T1.T[None, None, :, :]).sum(-1).sum(-1).T
        gKern3 = 0.5 * (Kgrad.T * self._T1minusT2.T[None, None, :, :]).sum(-1).sum(-1).T
        return -(gKern0 + gKern1 + gKern2 + gKern3)

    def _LMLgrad_Xm(self, hyperparams):
        return self._LMLgrad_wrt(self._Kmmgrad_inducing_variables(hyperparams['covar'], hyperparams[ivar_id]), psi1ax1=(-1), psi1ax2=(-1), *self.covar.psigrad_inducing_variables())

    def _LMLgrad_covar(self, hyperparams):
        inducing_variables = hyperparams[ivar_id]
        theta = hyperparams['covar'].copy()
        return self._LMLgrad_wrt(self._Kmmgrad_theta(theta, inducing_variables), *self.covar.psigrad_theta())

    def _LMLgrad_beta(self, hyperparams):
        LATildeInfTP = numpy.dot(self._LAtildeInv.T, self._P)
        gBeta = 0.5 * (self.d * (numpy.trace(self._C) + (self.n - self.m) * self._beta_inv - self._psi_0) - self.TrYY + self._TrPP + self._beta_inv ** 2 * self.d * numpy.sum(self._LAtildeInv * self._LAtildeInv) + self._beta_inv * numpy.sum(LATildeInfTP ** 2))
        return -gBeta

    def _LMLgrad_x(self, hyperparams):
        gBound = self._LMLgrad_wrt(numpy.array(0), psi1ax1=1, psi1ax2=1, *self.covar.psigrad_mean())
        return gBound

    def _LMLgrad_S(self, hyperparams):
        gBound = self._LMLgrad_wrt(numpy.array(0), psi1ax1=1, psi1ax2=1, *self.covar.psigrad_variance())
        return gBound

    def _KLgrad_Xm(self):
        return 0

    def _KLgrad_covar(self):
        return 0

    def _KLgrad_beta(self):
        return 0

    def _KLgrad_x(self):
        return self.covar._filter_x(self._x)

    def _KLgrad_S(self):
        return -(1 - self.covar._filter_x(self._variance))

    def _compute_variational_bound(self, hyperparams):
        logDAtilde = 2 * numpy.sum(numpy.log(numpy.diag(self._LAtilde)))
        p11 = self.d * (-(self.n - self.m) * numpy.log(self._beta) + logDAtilde)
        p12 = -self._beta * (self._TrPP - self.TrYY)
        p13 = self.d * self._beta * (self._psi_0 - numpy.trace(self._C))
        p1 = -0.5 * (p11 + p12 + p13)
        p2 = -(self.n * self.d / 2.0) * numpy.log(2 * numpy.pi)
        return p1 + p2

    def _compute_kl_divergence(self, hyperparams):
        mean = self._x
        variational_mean = numpy.sum(mean * mean)
        variational_variance = numpy.sum(self._variance - numpy.log(self._variance))
        return -0.5 * (variational_mean + variational_variance) + 0.5 * mean.shape[1] * self.n

    def update_stats(self, hyperparams):
        max_tries = 10
        self._x = hyperparams[mean_id]
        self._beta = max(hyperparams['beta'][0], 1e-05)
        self._beta_inv = 1.0 / self._beta
        self._variance = numpy.exp(2 * hyperparams[vars_id].copy())
        self.covar.update_stats(hyperparams['covar'].copy(), self._x.copy(), hyperparams[vars_id].copy(), hyperparams[ivar_id].copy())
        self._psi_0, self._psi_1, self._psi_2 = self.covar.psi()
        self._Kmm = self.covar.K(hyperparams['covar'].copy(), hyperparams[ivar_id]) + numpy.eye(self.m) * self.constant_jitter
        try:
            Lm, self.constant_jitter = jitChol(self._Kmm, warning=True, maxTries=max_tries)
            self._Lm = numpy.triu(Lm).T
        except LinAlgError:
            Lm, _ = jitChol(self._Kmm, warning=False, maxTries=max_tries * 2)
            self._Lm = numpy.triu(Lm).T
            try:
                import ipdb
                ipdb.set_trace()
            except:
                import pdb
                pdb.set_trace()

        self._LmInv = scipy.lib.lapack.flapack.dtrtri(self._Lm.T)[0].T
        self._KmmInv = numpy.dot(self._LmInv.T, self._LmInv)
        self._C = numpy.dot(numpy.dot(self._LmInv, self._psi_2), self._LmInv.T)
        self._Atilde = self._beta_inv * numpy.eye(self.m) + self._C
        self._Atilde += numpy.eye(self.m) * self.constant_jitter_Atilde
        try:
            LAtilde, self.constant_jitter_Atilde = jitChol(self._Atilde, warning=True, maxTries=max_tries)
            self._LAtilde = numpy.triu(LAtilde).T
        except LinAlgError:
            LAtilde, _ = jitChol(self._Atilde, warning=False, maxTries=max_tries * 2)
            self._LAtilde = numpy.triu(LAtilde).T
            try:
                import ipdb
                ipdb.set_trace()
            except:
                import pdb
                pdb.set_trace()

        self._LAtildeInv = scipy.lib.lapack.flapack.dtrtri(self._LAtilde.T)[0].T
        self._P1 = numpy.dot(self._LAtildeInv, self._LmInv)
        y = self._y
        self._P = numpy.dot(self._P1, numpy.dot(self._psi_1.T, y))
        self._B = numpy.dot(self._P1.T, self._P)
        self._yB = numpy.dot(y, self._B.T)
        Tb = self._beta_inv * self.d * numpy.dot(self._P1.T, self._P1)
        Tb += numpy.dot(self._B, self._B.T)
        self._T1 = self.d * self._KmmInv - Tb
        T2 = self._beta * self.d * numpy.dot(self._LmInv.T, numpy.dot(self._C, self._LmInv))
        self._T1minusT2 = self._T1 - T2
        self._TrPP = numpy.sum(self._P * self._P)
        self._covar_cache['hyperparams'] = deepcopy(hyperparams)
        self._active_set_indices_changed = False

    def _Kmmgrad_inducing_variables(self, theta, inducing_variables):
        K_ = numpy.array([ self.covar.Kgrad_x(theta, inducing_variables, inducing_variables, i) for i in itertools.chain(self.covar.get_dimension_indices())
                         ])
        prod = numpy.eye(self.m)[:, None, :, None] * K_.T
        return prod.swapaxes(0, 1) + prod

    def _Kmmgrad_theta(self, theta, inducing_variables):
        Kmmgrad_theta = numpy.array([ self.covar.Kgrad_theta(theta, inducing_variables, i) for i in xrange(theta.shape[0])
                                    ])
        return Kmmgrad_theta[None, :, :, :].T

    def plot_scales(self, hyperparams, hyper_filter=None, figure_num='scales', **barkwargs):
        self._active_set_indices_changed = True
        self.update_stats(hyperparams)
        n_params = self.covar.get_number_of_parameters() + 1
        if hyper_filter is None:
            hyper_filter = numpy.arange(n_params)
        opt_covar = self.covar.get_reparametrized_theta(hyperparams['covar']).copy()
        opt_covar = numpy.append(opt_covar, self._beta_inv)
        names = numpy.array(self.covar.get_hyperparameter_names()).copy()
        names = numpy.append(names, ['Beta Inverse'])
        import pylab
        if n_params > 15:
            fig_pcolor = pylab.figure(figsize=(16, 6), num=figure_num)
        else:
            fig_pcolor = pylab.figure(figsize=(8, 6), num=figure_num)
        ard_param_indices = self.covar.get_ard_dimension_indices()
        non_ard_param_indices = numpy.setxor1d(ard_param_indices, hyper_filter, False)
        s = numpy.argsort(opt_covar[ard_param_indices])[::-1]
        append_indices = numpy.append(ard_param_indices[s], non_ard_param_indices[self.covar.get_ard_dimension_indices().min():])
        opt_covar = opt_covar[append_indices]
        names = names[append_indices]
        pylab.bar((numpy.arange(len(opt_covar)) + 0.1), opt_covar, 0.8, **barkwargs)
        pylab.xticks(numpy.arange(len(opt_covar)) + 0.5, names, rotation=17, size=12)
        pylab.xlim(0, len(opt_covar))
        fig_pcolor.autofmt_xdate()
        pylab.subplots_adjust(left=0.11, bottom=0.18, right=0.97, top=0.9, wspace=None, hspace=0.53)
        return fig_pcolor

    def plot_scatter(self, hyperparams, size=35, marker='o', color='b', cmap='gray_r', lbls=None, figure_num='scatter', labels=None):
        import pylab
        cmap = pylab.get_cmap(cmap)
        self._active_set_indices_changed = True
        self.update_stats(hyperparams)
        opt_covar = self.covar.get_reparametrized_theta(hyperparams['covar']).copy()
        opt_covar = numpy.append(opt_covar, self._beta_inv)
        mean = self._x
        inducing_variables = hyperparams[ivar_id]
        Q = mean.shape[1]
        ard_param_indices = self.covar.get_ard_dimension_indices()
        s = numpy.argsort(opt_covar[ard_param_indices])[::-1]
        fig_scales = pylab.figure(num=figure_num)
        ax = pylab.subplot(111)
        ax.autoscale(False)
        plots = []
        extent = (
         mean[:, s[0]].min() - 0.1 * numpy.abs(mean[:, s[0]].min()),
         mean[:, s[0]].max() + 0.1 * numpy.abs(mean[:, s[0]].max()),
         mean[:, s[1]].min() - 0.1 * numpy.abs(mean[:, s[1]].min()),
         mean[:, s[1]].max() + 0.1 * numpy.abs(mean[:, s[1]].max()))
        N_star = 50
        x = numpy.linspace(extent[0], extent[1], N_star)
        y = numpy.linspace(extent[2], extent[3], N_star)
        X, Y = numpy.meshgrid(x, y)
        X_ = numpy.zeros((N_star, Q))
        Z = numpy.zeros((N_star, N_star))
        for n in xrange(N_star):
            X_[:, s[0]] = X[:, n]
            X_[:, s[1]] = Y[:, n]
            _, Z_ = self.predict(hyperparams, X_)
            Z[:, n] += Z_[:, 0]

        plots.append(pylab.imshow(Z, origin='lower', cmap=cmap, extent=extent, interpolation='bilinear', aspect='auto'))
        plots.append(pylab.scatter(inducing_variables[:, s[0]], inducing_variables[:, s[1]], s=size, marker=(5,
                                                                                                             1), alpha=0.4, color='magenta'))
        if labels is not None:
            if lbls is None:
                lbls = numpy.arange(labels.shape[1])
            mark = marker
            col = color
            for i in xrange(labels.shape[1]):
                mean_i = mean[labels[:, i], :]
                if len(marker) == labels.shape[1]:
                    mark = marker[i]
                if len(color) == labels.shape[1]:
                    col = color[i]
                plots.append(pylab.scatter(mean_i[:, s[0]], mean_i[:, s[1]], s=size, marker=mark, color=col, label=lbls[i]))

        else:
            plots.append(pylab.scatter(mean[:, s[0]], mean[:, s[1]], s=size, marker=marker, c=color))
        pylab.xlabel('${\\bf X}_{:,0}$')
        pylab.ylabel('${\\bf X}_{:,1}$')
        pylab.xlim(extent[0], extent[1])
        pylab.ylim(extent[2], extent[3])
        return fig_scales

    def plot(self, hyperparams, size=35, marker='o', color='b', cmap='gray_r', first_two_dim=True, hyper_filter=None, suptitle='', lbls=None, figure_nums=('scales', 'scatter'), labels=None):
        raise DeprecationWarning('please use plot_scales and plot_scatter')
        import pylab
        cmap = pylab.get_cmap('gray_r')
        self._active_set_indices_changed = True
        self.update_stats(hyperparams)
        n_params = self.covar.get_number_of_parameters() + 1
        if hyper_filter is None:
            hyper_filter = numpy.arange(n_params)
        opt_covar = self.covar.get_reparametrized_theta(hyperparams['covar']).copy()
        opt_covar = numpy.append(opt_covar, self._beta_inv)
        names = numpy.array(self.covar.get_hyperparameter_names()).copy()
        names = numpy.append(names, ['Beta Inverse'])
        mean = self._x
        variance = hyperparams[vars_id]
        inducing_variables = hyperparams[ivar_id]
        N = mean.shape[0]
        Q = mean.shape[1]
        if n_params > 15:
            fig_pcolor = pylab.figure(figsize=(16, 6), num=figure_nums[0])
        else:
            fig_pcolor = pylab.figure(figsize=(8, 6), num=figure_nums[0])
        ard_param_indices = self.covar.get_ard_dimension_indices()
        non_ard_param_indices = numpy.setxor1d(ard_param_indices, hyper_filter, False)
        s = numpy.argsort(opt_covar[ard_param_indices])[::-1]
        append_indices = numpy.append(ard_param_indices[s], non_ard_param_indices[self.covar.get_ard_dimension_indices().min():])
        opt_covar = opt_covar[append_indices]
        names = names[append_indices]
        pylab.bar(numpy.arange(len(opt_covar)) + 0.1, opt_covar, 0.8, color=color)
        pylab.xticks(numpy.arange(len(opt_covar)) + 0.5, names, rotation=17, size=12)
        pylab.xlim(0, len(opt_covar))
        fig_pcolor.autofmt_xdate()
        pylab.subplots_adjust(left=0.11, bottom=0.18, right=0.97, top=0.9, wspace=None, hspace=0.53)
        pylab.suptitle(suptitle)
        if not first_two_dim:
            return [fig_pcolor]
        else:
            fig_scales = pylab.figure(num=figure_nums[1])
            ax = pylab.subplot(111)
            ax.autoscale(False)
            plots = []
            extent = (
             mean[:, s[0]].min() - 0.1 * numpy.abs(mean[:, s[0]].min()),
             mean[:, s[0]].max() + 0.1 * numpy.abs(mean[:, s[0]].max()),
             mean[:, s[1]].min() - 0.1 * numpy.abs(mean[:, s[1]].min()),
             mean[:, s[1]].max() + 0.1 * numpy.abs(mean[:, s[1]].max()))
            N_star = 50
            x = numpy.linspace(extent[0], extent[1], N_star)
            y = numpy.linspace(extent[2], extent[3], N_star)
            X, Y = numpy.meshgrid(x, y)
            X_ = numpy.zeros((N_star, Q))
            Z = numpy.zeros((N_star, N_star))
            for n in xrange(N_star):
                X_[:, s[0]] = X[:, n]
                X_[:, s[1]] = Y[:, n]
                _, Z_ = self.predict(hyperparams, X_)
                Z[:, n] += Z_[:, 0]

            plots.append(pylab.imshow(Z, origin='lower', cmap=cmap, extent=extent, interpolation='bilinear', aspect='auto'))
            plots.append(pylab.scatter(inducing_variables[:, s[0]], inducing_variables[:, s[1]], s=size, marker=(5,
                                                                                                                 1), alpha=0.4, color='magenta'))
            if labels is not None:
                if lbls is None:
                    lbls = numpy.arange(labels.shape[1])
                mark = marker
                col = color
                for i in xrange(labels.shape[1]):
                    mean_i = mean[labels[:, i], :]
                    if len(marker) == labels.shape[1]:
                        mark = marker[i]
                    if len(color) == labels.shape[1]:
                        col = color[i]
                    plots.append(pylab.scatter(mean_i[:, s[0]], mean_i[:, s[1]], s=size, marker=mark, color=col, label=lbls[i]))

            else:
                plots.append(pylab.scatter(mean[:, s[0]], mean[:, s[1]], s=size, marker=marker, c=color))
            pylab.xlabel('${\\bf X}_{:,0}$')
            pylab.ylabel('${\\bf X}_{:,1}$')
            pylab.xlim(extent[0], extent[1])
            pylab.ylim(extent[2], extent[3])
            pylab.suptitle(suptitle)
            return [fig_pcolor, fig_scales]