# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/pygp/gp/shared_latent_bayesian_gplvm.py
# Compiled at: 2013-04-10 06:45:39
__doc__ = '\nCreated on 23 Aug 2012\n\n@author: maxz\n'
from pygp.gp.bayesian_gplvm import BayesianGPLVM, mean_id, vars_id, ivar_id
import numpy
from pygp.gp.gp_base import GP
from copy import deepcopy

class SharedLatentBayesianGPLVM(GP):

    def __init__(self, y, covar_func, gplvm_dimensions=None, n_inducing_variables=10, **kw_args):
        """
        Initialize the model:

        Parameters:
            _y : [y_i for i in number of datasets]
            List of datasets to be compared by a shared latent space

            covar_func : CovarianceFunction
            Either a list of covariance functions for each dataset, or one covariance function for all datasets

        """
        assert isinstance(y, (list, tuple)), 'Please provide the datasets Y as list: [Y_1, ..., Y_n]'
        self.gplvm_list = []
        self.setData(y, None, gplvm_dimensions, n_inducing_variables)
        if isinstance(covar_func, (list, tuple)):
            self.covar = covar_func
        else:
            self.covar = [ deepcopy(covar_func) for _ in y ]
        for i, y_i in enumerate(y):
            self.gplvm_list.append(BayesianGPLVM(y_i, self.covar[i], gplvm_dimensions=None, n_inducing_variables=n_inducing_variables))

        return

    def LML(self, hyperparams_all, priors=None, **kw_args):
        var_bound = 0
        for i, gplvm in enumerate(self.gplvm_list):
            hyperparams = self._filter_hyperparams(hyperparams_all, i)
            if not gplvm._is_cached(hyperparams):
                gplvm.update_stats(hyperparams)
            var_bound += gplvm._compute_variational_bound(hyperparams)

        kl_bound = self.gplvm_list[0]._compute_kl_divergence(hyperparams)
        bound = var_bound + kl_bound
        return -bound

    def LMLgrad(self, hyperparams_all, priors=None, **kw_args):
        LMLgrad = dict.fromkeys(hyperparams_all.keys(), 0)
        for i, gplvm in enumerate(self.gplvm_list):
            hyperparams = self._filter_hyperparams(hyperparams_all, i)
            unique_parameter_keys_to_gplvm = [
             'covar', ivar_id, 'beta']
            grad = gplvm.LMLgrad(hyperparams, add_KLgrad=i == 0)
            for unique_name in unique_parameter_keys_to_gplvm:
                LMLgrad[('{0}_{1}').format(unique_name, i)] = grad[unique_name]

            summation_parameter_keys_to_gplvm = [
             mean_id, vars_id]
            for key in summation_parameter_keys_to_gplvm:
                LMLgrad[key] += grad[key]

        return LMLgrad

    def _filter_hyperparams(self, hyperparams, index):
        hyperparams_filtered = {}
        hyperparams_filtered['covar'] = hyperparams[('covar_%i' % index)].copy()
        hyperparams_filtered[ivar_id] = hyperparams[('{0}_{1}').format(ivar_id, index)]
        hyperparams_filtered[mean_id] = hyperparams[mean_id]
        hyperparams_filtered[vars_id] = hyperparams[vars_id]
        hyperparams_filtered['beta'] = hyperparams[('beta_%i' % index)]
        return hyperparams_filtered

    def setData(self, y, x=None, gplvm_dimensions=None, n_inducing_variables=None, training_labels=None, **kw_args):
        self.gplvm_dimensions = gplvm_dimensions
        self._y = y
        if x is not None:
            self._x = x
        self.n = self._y[0].shape[0]
        self.d = [ y.shape[1] for y in self._y ]
        self._invalidate_cache()
        if n_inducing_variables is not None:
            self.m = n_inducing_variables
        return

    def plot_betas(self, hyperparams, groupnames=None, fignum='slbgplvm betas'):
        ngroups = len(self.covar)
        if groupnames is None:
            groupnames = [ ('Group {}').format(i + 1) for i in range(ngroups) ]
        betainvs = [ 1.0 / hyperparams[('beta_{}').format(i)] for i in range(ngroups) ]
        import pylab
        pylab.figure(fignum)
        pylab.clf()
        pylab.bar(numpy.arange(ngroups) + 0.1, betainvs, 0.8)
        pylab.xticks(numpy.arange(ngroups) + 0.5, groupnames)
        pylab.draw()
        pylab.tight_layout()
        return

    def plot_scatter(self, hyperparams):
        X = hyperparams[mean_id]

    def plot_scales(self, hyperparams, groupnames=None, colors=None, nonzerothreshold=1e-05, fignum='slbgplvm scales', xlabel='Latent Dimension', ylabel='Fraction of $\\alpha$'):
        ngroups = len(self.covar)
        if colors is None:
            from matplotlib.cm import jet
            colors = [ jet(float(i) / float(ngroups)) for i in range(ngroups) ]
        from matplotlib.colors import colorConverter
        dcolors = numpy.apply_along_axis(lambda x: numpy.clip(x - 0.3, 0, 1), 0, colorConverter.to_rgba_array(colors))
        dcolors[:, -1] = 1.0
        if groupnames is None:
            groupnames = [ ('Group {}').format(i + 1) for i in range(ngroups) ]
        ardparams, completesort, ardnames, ardindices = self.sorteddimensiongroups(hyperparams, nonzerothreshold)
        ardparamscumsum = ardparams.cumsum(0)
        ardparamscumsum = ardparamscumsum[:, completesort]
        ardnames = ardnames[(0, completesort)]
        ardindices = ardindices[(0, completesort)]
        import pylab
        pylab.figure(fignum)
        pylab.clf()
        left = numpy.arange(ardparams.shape[1]) + 0.1
        pylab.bar(left, ardparamscumsum[0], 0.8, 0, color=colors[0], label=groupnames[0])
        for i in range(ngroups - 1):
            c = colors[(i + 1)]
            dc = dcolors[(i + 1)]
            pylab.bar(left, ardparamscumsum[(i + 1)], 0.8, ardparamscumsum[i], facecolor=c, edgecolor=dc, label=groupnames[(i + 1)])

        pylab.xticks(left + 0.4, [ ('${}$').format(int(x)) for x in completesort ])
        pylab.xlabel(xlabel)
        pylab.ylabel(ylabel)
        pylab.xlim(0, ardparams.shape[1])
        leg = pylab.legend(loc=2, bbox_to_anchor=(1, 1), borderaxespad=0.0, prop={'size': 12})
        pylab.draw()
        bbox = leg.get_window_extent()
        bbox2 = bbox.transformed(leg.axes.transAxes.inverted())
        pylab.draw()
        pylab.tight_layout(pad=1.04, rect=(0, 0, 1 - bbox2.bounds[2] + 0.04, 1))
        return

    def dimensiongroupindices(self, ardparams, nonzerothreshold=1e-05):
        """
        returns
        ------- 
        indices: [ array([int]) ] in {Q _x N-indices}:

            which groups are active in dimension q.
            if indices[q] is empty    -> dimension q switched off
            elif len(indices[q]) == 1 -> dimension q private for group indices[q]
            else                      -> dimension q shared by all groups indices[q]            
        """
        nonzero = ardparams > nonzerothreshold
        sharedindices = [ numpy.where(x)[0] for x in nonzero.T ]
        return sharedindices

    def hyperparamstoardparamsarray(self, hyperparams):
        ngroups = len(self.covar)
        ardnames = numpy.array([ self.covar[i].get_hyperparameter_names()[self.covar[i].get_ard_dimension_indices()] for i in range(ngroups) ])
        ardindices = numpy.array([ self.covar[i].get_ard_dimension_indices() for i in range(ngroups) ])
        ardparams = numpy.array([ self.covar[i].get_reparametrized_theta(hyperparams[('covar_{:}').format(i)])[ardindices[i]] for i in range(ngroups)
                                ])
        ardparams /= ardparams.sum(1)[:, None] * ardparams.shape[0]
        return (
         ardparams, ardindices, ardnames)

    def sortsharedprivateoff(self, dimensiongroupindices, ardparams):
        lendimensiongroupindices = numpy.array(map(len, dimensiongroupindices))
        ardoff = numpy.where(lendimensiongroupindices == 0)[0]
        ardpriv = numpy.where(lendimensiongroupindices == 1)[0]
        ardsh = numpy.where(lendimensiongroupindices > 1)[0]
        offsort = numpy.argsort(ardparams[ardoff])[::-1]
        privsort = numpy.argsort(ardparams[ardpriv])[:-1]
        shsort = numpy.argsort(ardparams[ardsh])[::-1]
        completesort = numpy.concatenate([ardsh[shsort], ardpriv[privsort], ardoff[offsort]])
        return completesort

    def sorteddimensiongroups(self, hyperparams, nonzerothreshold=1e-05):
        ardparams, ardindices, ardnames = self.hyperparamstoardparamsarray(hyperparams)
        dimensiongroupindices = self.dimensiongroupindices(ardparams, nonzerothreshold=nonzerothreshold)
        completesort = self.sortsharedprivateoff(dimensiongroupindices, ardparams.sum(0))
        return (
         ardparams, completesort, ardnames, ardindices)