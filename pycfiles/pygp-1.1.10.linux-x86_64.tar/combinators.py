# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/pygp/covar/combinators.py
# Compiled at: 2013-04-10 06:45:39
"""
Covariance Function Combinators
-------------------------------

Each combinator is a covariance function (CF) itself. It combines one or several covariance function(s) into another. For instance, :py:class:`pygp.covar.combinators.SumCF` combines all given CFs into one sum; use this class to add noise.

"""
import scipy as sp, numpy, itertools, operator
from pygp.covar.dist import dist
from pygp.covar.covar_base import BayesianStatisticsCF, CovarianceFunction
import __future__

class SumCF(CovarianceFunction):
    """
    Sum Covariance function. This function adds
    up the given CFs and returns the resulting sum.

    *covars* : [:py:class:`pygp.covar.CovarianceFunction`]
    
        Covariance functions to sum up.
    """

    def __init__(self, covars, names=[], *args, **kw_args):
        super(SumCF, self).__init__(*args, **kw_args)
        self.n_params_list = []
        self.covars = []
        self.covars_theta_I = []
        self.covars_covar_I = []
        self.covars = covars
        if names and len(names) == len(self.covars):
            self.names = names
        else:
            if names:
                self.names = []
                print ('names provided, but shapes not matching (names:{}) (covars:{})').format(len(names), len(covars))
            else:
                self.names = []
            i = 0
            for nc in xrange(len(covars)):
                covar = covars[nc]
                assert isinstance(covar, CovarianceFunction), 'SumCF: SumCF is constructed from a list of covaraince functions'
                Nparam = covar.get_number_of_parameters()
                self.n_params_list.append(Nparam)
                self.covars_theta_I.append(sp.arange(i, i + covar.get_number_of_parameters()))
                self.covars_covar_I.extend(sp.repeat(nc, Nparam))
                i += covar.get_number_of_parameters()

        self.n_params_list = sp.array(self.n_params_list)
        self.n_hyperparameters = self.n_params_list.sum()

    def get_dimension_indices(self):
        """
        returns list of dimension indices for covariance functions
        """
        return numpy.array(reduce(numpy.append, map(lambda x: x.get_dimension_indices(), self.covars)), dtype='int')

    def get_n_dimensions(self):
        return reduce(operator.add, map(lambda x: x.get_n_dimensions(), self.covars))

    def get_hyperparameter_names(self):
        """return the names of hyperparameters to make identification easier"""
        return reduce(numpy.append, map(lambda x: x.get_hyperparameter_names(), self.covars))

    def get_theta_by_names(self, theta, names):
        theta_n = []
        for nc in xrange(len(self.covars)):
            _theta = theta[self.covars_theta_I[nc]]
            if self.names[nc] in names:
                theta_n.append(_theta)

        return reduce(numpy.append, theta_n)

    def get_reparametrized_theta_by_names(self, theta, names):
        return self.get_theta_by_names(self.get_reparametrized_theta(theta), names)

    def K(self, theta, x1, x2=None, names=[]):
        """
        Get Covariance matrix K with given hyperparameters
        theta and inputs x1 and x2. The result
        will be the sum covariance of all covariance
        functions combined in this sum covariance.

        **Parameters:**
        See :py:class:`pygp.covar.CovarianceFunction` 
        """
        assert theta.shape[0] == self.get_number_of_parameters(), 'K: theta has wrong shape'
        for nc in xrange(len(self.covars)):
            covar = self.covars[nc]
            _theta = theta[self.covars_theta_I[nc]]
            if not names or not self.names or self.names[nc] in names:
                K_ = covar.K(_theta, x1, x2)
                try:
                    K += K_
                except:
                    K = K_

        return K

    def Kgrad_theta(self, theta, x1, i):
        """
        The partial derivative of the covariance matrix with
        respect to i-th hyperparameter.

        **Parameters:**
        See :py:class:`pygp.covar.CovarianceFunction`
        """
        assert theta.shape[0] == self.n_hyperparameters, 'K: theta has wrong shape'
        nc = self.covars_covar_I[i]
        covar = self.covars[nc]
        d = self.covars_theta_I[nc].min()
        j = i - d
        return covar.Kgrad_theta(theta[self.covars_theta_I[nc]], x1, j)

    def Kgrad_x(self, theta, x1, x2, d):
        assert theta.shape[0] == self.n_hyperparameters, 'K: theta has wrong shape'
        RV = sp.zeros([x1.shape[0], x1.shape[0]])
        for nc in xrange(len(self.covars)):
            covar = self.covars[nc]
            _theta = theta[self.covars_theta_I[nc]]
            RV += covar.Kgrad_x(_theta, x1, x2, d)

        return RV

    def Kgrad_xdiag(self, theta, x1, d):
        assert theta.shape[0] == self.n_hyperparameters, 'K: theta has wrong shape'
        RV = sp.zeros([x1.shape[0]])
        for nc in xrange(len(self.covars)):
            covar = self.covars[nc]
            _theta = theta[self.covars_theta_I[nc]]
            RV += covar.Kgrad_xdiag(_theta, x1, d)

        return RV

    def get_reparametrized_theta(self, theta):
        return numpy.concatenate([ covar.get_reparametrized_theta(theta[nc]) for covar, nc in zip(self.covars, self.covars_theta_I) ])

    def get_de_reparametrized_theta(self, theta):
        return numpy.concatenate([ covar.get_de_reparametrized_theta(theta[nc]) for covar, nc in zip(self.covars, self.covars_theta_I) ])

    def get_ard_dimension_indices(self):
        return numpy.int_(reduce(numpy.append, [ covar.get_ard_dimension_indices() for covar in self.covars ]))


class SumCFPsiStat(SumCF, BayesianStatisticsCF):

    def __init__(self, *args, **kwargs):
        super(SumCFPsiStat, self).__init__(*args, **kwargs)

    def update_stats(self, theta, mean, variance, inducing_variables):
        super(SumCFPsiStat, self).update_stats(theta, mean, variance, inducing_variables)
        self.psi_list = []
        for covar, nc in zip(self.covars, self.covars_theta_I):
            covar.update_stats(theta[nc], mean, variance, inducing_variables)
            self.psi_list.append(covar.psi())

    def psi(self):
        psis = reduce(lambda x, y: [ numpy.add(a, b) for a, b in zip(x, y) ], self.psi_list)
        crossterms = 0
        for a, b in itertools.combinations([ p[1] for p in self.psi_list ], 2):
            prod = numpy.multiply(a, b).sum(0)
            crossterms += prod[None] + prod[:, None]

        psis[2] += crossterms
        return psis

    def psigrad_theta(self):
        psi0 = numpy.zeros((self.get_number_of_parameters(), 1))
        psi1 = numpy.zeros((self.N, self.M, self.get_number_of_parameters(), 1))
        psi2 = numpy.zeros((self.M, self.M, self.get_number_of_parameters(), 1))

        def append_at(covar, index):
            grads = covar.psigrad_theta()
            psi0[index] = grads[0]
            psi1[:, :, index] = grads[1]
            psi2[:, :, index] = grads[2]

        [ append_at(covar, index) for covar, index in zip(self.covars, self.covars_theta_I) ]
        for grad_index, psi1_index in itertools.permutations(range(len(self.psi_list)), 2):
            theta_index = self.covars_theta_I[grad_index]
            psi2_cross = (psi1[:, :, theta_index] * numpy.expand_dims(numpy.expand_dims(self.psi_list[psi1_index][1], -1), -1)).sum(0)
            psi2[:, :, theta_index] += psi2_cross[None] + psi2_cross[:, None]

        return (psi0, psi1, psi2)

    def psigrad_mean(self):
        psi_grads = [ covar.psigrad_mean() for covar in self.covars ]
        psi0 = numpy.zeros((self.N, self.get_n_dimensions()))
        psi1 = numpy.zeros((self.N, self.M, 1, self.get_n_dimensions()))
        psi2 = numpy.zeros((self.M, self.M, self.N, self.get_n_dimensions()))
        for covar, psigrad in zip(self.covars, psi_grads):
            dims = covar.get_dimension_indices()
            psi0[:, dims] = psi0[:, dims] + psigrad[0]
            psi1[:, :, :, dims] = psi1[:, :, :, dims] + psigrad[1]
            psi2[:, :, :, dims] = psi2[:, :, :, dims] + psigrad[2]

        psis = [psi0, psi1, psi2]
        for grad_index, psi1_index in itertools.permutations(range(len(self.psi_list)), 2):
            psi1 = numpy.expand_dims(numpy.expand_dims(self.psi_list[psi1_index][1], -1), -1)
            dims = self.covars[grad_index].get_dimension_indices()
            if dims.size > 0:
                psi2_cross = psi1 * psi_grads[grad_index][1]
                if len(psi2_cross.shape) == 4 and psi2_cross.shape[2] == 1:
                    psi2_cross = psi2_cross.swapaxes(0, 2)
                psi2_cross = psi2_cross.sum(0)
                psis[2][:, :, :, dims] = psis[2][:, :, :, dims] + (numpy.expand_dims(psi2_cross, 0) + numpy.expand_dims(psi2_cross, 1))

        return psis

    def psigrad_variance(self):
        psi_grads = [ covar.psigrad_variance() for covar in self.covars ]
        psi0 = numpy.zeros((self.N, self.get_n_dimensions()))
        psi1 = numpy.zeros((self.N, self.M, 1, self.get_n_dimensions()))
        psi2 = numpy.zeros((self.M, self.M, self.N, self.get_n_dimensions()))
        for covar, psigrad in zip(self.covars, psi_grads):
            dims = covar.get_dimension_indices()
            psi0[:, dims] = psi0[:, dims] + psigrad[0]
            psi1[:, :, :, dims] = psi1[:, :, :, dims] + psigrad[1]
            psi2[:, :, :, dims] = psi2[:, :, :, dims] + psigrad[2]

        psis = [psi0, psi1, psi2]
        for grad_index, psi1_index in itertools.permutations(range(len(self.psi_list)), 2):
            psi1 = numpy.expand_dims(numpy.expand_dims(self.psi_list[psi1_index][1], -1), -1)
            dims = self.covars[grad_index].get_dimension_indices()
            if dims.size > 0:
                psi2_cross = psi1 * psi_grads[grad_index][1]
                if len(psi2_cross.shape) == 4 and psi2_cross.shape[2] == 1:
                    psi2_cross = psi2_cross.swapaxes(0, 2)
                psi2_cross = psi2_cross.sum(0)
                psis[2][:, :, :, dims] = psis[2][:, :, :, dims] + (numpy.expand_dims(psi2_cross, 0) + numpy.expand_dims(psi2_cross, 1))

        return psis

    def psigrad_inducing_variables(self):
        psi_grads = [ covar.psigrad_inducing_variables() for covar in self.covars ]
        psi0 = numpy.zeros((self.M, self.get_n_dimensions()))
        psi1 = numpy.zeros((self.N, self.M, self.M, self.get_n_dimensions()))
        psi2 = numpy.zeros((self.M, self.M, self.M, self.get_n_dimensions()))
        for covar, psigrad in zip(self.covars, psi_grads):
            dims = covar.get_dimension_indices()
            psi0[:, dims] = psi0[:, dims] + psigrad[0]
            psi1[:, :, :, dims] = psi1[:, :, :, dims] + psigrad[1]
            psi2[:, :, :, dims] = psi2[:, :, :, dims] + psigrad[2]

        psis = [psi0, psi1, psi2]
        for grad_index, psi1_index in itertools.permutations(range(len(self.psi_list)), 2):
            psi1 = numpy.expand_dims(numpy.expand_dims(self.psi_list[psi1_index][1], -1), -1)
            dims = self.covars[grad_index].get_dimension_indices()
            if dims.size > 0:
                psi2_cross = psi1 * psi_grads[grad_index][1]
                if len(psi2_cross.shape) == 4 and psi2_cross.shape[2] == 1:
                    psi2_cross = psi2_cross.swapaxes(0, 2)
                psi2_cross = psi2_cross.sum(0)
                psis[2][:, :, :, dims] = psis[2][:, :, :, dims] + (numpy.expand_dims(psi2_cross, 0) + numpy.expand_dims(psi2_cross, 1))

        return psis


class ProductCF(CovarianceFunction):
    """
    Product Covariance function. This function multiplies
    the given CFs and returns the resulting product.
    
    **Parameters:**
    
    covars : [CFs of type :py:class:`pygp.covar.CovarianceFunction`]
    
        Covariance functions to be multiplied.
        
    """

    def __init__(self, covars, *args, **kw_args):
        super(ProductCF, self).__init__()
        self.n_params_list = []
        self.covars = []
        self.covars_theta_I = []
        self.covars_covar_I = []
        self.covars = covars
        i = 0
        for nc in xrange(len(covars)):
            covar = covars[nc]
            Nparam = covar.get_number_of_parameters()
            self.n_params_list.append(Nparam)
            self.covars_theta_I.append(sp.arange(i, i + covar.get_number_of_parameters()))
            self.covars_covar_I.extend(sp.repeat(nc, Nparam))
            i += Nparam

        self.n_params_list = sp.array(self.n_params_list)
        self.n_hyperparameters = self.n_params_list.sum()

    def get_hyperparameter_names(self):
        """return the names of hyperparameters to make identificatio neasier"""
        names = []
        for covar in self.covars:
            names.extend(covar.get_hyperparameter_names())

        return names

    def K(self, theta, x1, x2=None):
        """
        Get Covariance matrix K with given hyperparameters
        theta and inputs x1 and x2. The result
        will be the product covariance of all covariance
        functions combined in this product covariance.

        **Parameters:**
        See :py:class:`pygp.covar.CovarianceFunction` 
        """
        assert theta.shape[0] == self.n_hyperparameters, 'ProductCF: K: theta has wrong shape'
        if x2 is None:
            K = sp.ones([x1.shape[0], x1.shape[0]])
        else:
            K = sp.ones([x1.shape[0], x2.shape[0]])
        for nc in xrange(len(self.covars)):
            covar = self.covars[nc]
            _theta = theta[self.covars_theta_I[nc]]
            K *= covar.K(_theta, x1, x2)

        return K

    def Kgrad_theta(self, theta, x, i):
        """The derivatives of the covariance matrix for
        the i-th hyperparameter.
        
        **Parameters:**
        See :py:class:`pygp.covar.CovarianceFunction`
        """
        assert theta.shape[0] == self.n_hyperparameters, 'ProductCF: K: theta has wrong shape'
        nc = self.covars_covar_I[i]
        covar = self.covars[nc]
        d = i - self.covars_theta_I[nc].min()
        Kd = covar.Kgrad_theta(theta[self.covars_theta_I[nc]], x, d)
        for ind in xrange(len(self.covars)):
            if ind != nc:
                _theta = theta[self.covars_theta_I[ind]]
                Kd *= self.covars[ind].K(_theta, x)

        return Kd

    def Kgrad_x(self, theta, x1, x2, d):
        assert theta.shape[0] == self.n_hyperparameters, 'Product CF: K: theta has wrong shape'
        x1, x2 = self._filter_input_dimensions(x1, x2)
        RV_sum = sp.zeros([x1.shape[0], x2.shape[0]])
        for nc in xrange(len(self.covars)):
            RV_prod = sp.ones([x1.shape[0], x2.shape[0]])
            for j in xrange(len(self.covars)):
                _theta = theta[self.covars_theta_I[j]]
                covar = self.covars[j]
                if j == nc:
                    RV_prod *= covar.Kgrad_x(_theta, x1, x2, d)
                else:
                    RV_prod *= covar.K(_theta, x1, x2)

            RV_sum += RV_prod

        return RV_sum

    def Kgrad_xdiag(self, theta, x1, d):
        assert theta.shape[0] == self.n_hyperparameters, 'K: theta has wrong shape'
        RV_sum = sp.zeros([x1.shape[0]])
        for nc in xrange(len(self.covars)):
            RV_prod = sp.ones([x1.shape[0]])
            for j in xrange(len(self.covars)):
                _theta = theta[self.covars_theta_I[j]]
                covar = self.covars[j]
                if j == nc:
                    RV_prod *= covar.Kgrad_xdiag(_theta, x1, d)
                else:
                    RV_prod *= covar.Kdiag(_theta, x1)

            RV_sum += RV_prod

        return RV_sum


class ProductCFPsiStat(ProductCF, BayesianStatisticsCF):

    def update_stats(self, theta, mean, variance, inducing_variables):
        super(ProductCFPsiStat, self).update_stats(theta, mean, variance, inducing_variables)
        self.psi_list = []
        for covar, nc in zip(self.covars, self.covars_theta_I):
            covar.update_stats(theta[nc], mean, variance, inducing_variables)
            self.psi_list.append(covar.psi())

    def psi(self):
        psis = reduce(lambda x, y: [ numpy.multiply(a, b) for a, b in zip(x, y) ], self.psi_list)
        return psis

    def psigrad_theta(self):
        return BayesianStatisticsCF.psigrad_theta(self)

    def psigrad_mean(self):
        return BayesianStatisticsCF.psigrad_mean(self)

    def psigrad_variance(self):
        return BayesianStatisticsCF.psigrad_variance(self)

    def psigrad_inducing_variables(self):
        return BayesianStatisticsCF.psigrad_inducing_variables(self)


class ShiftCF(CovarianceFunction):
    """
    Time Shift Covariance function. This covariance function depicts
    the time shifts induced by the data and covariance function given
    and passes the shifted inputs to the covariance function given.
    To calculate the shifts of the inputs make shure the covariance
    function passed implements the derivative after the input
    Kd_dx(theta, x).
    
    covar : CF of type :py:class:`pygp.covar.CovarianceFunction`
    
        Covariance function to be used to depict the time shifts.
    
    replicate_indices : [int]

        The indices of the respective replicates, corresponding to
        the inputs. For instance: An input with three replicates:

        ===================== ========= ========= =========
        /                     rep1      rep2      rep3
        ===================== ========= ========= =========
        input = [             -1,0,1,2, -1,0,1,2, -1,0,1,2]
        replicate_indices = [ 0,0,0,0,  1,1,1,1,  2,2,2,2]
        ===================== ========= ========= =========

            
        Thus, the replicate indices represent
        which inputs correspond to which replicate.
        
    """

    def __init__(self, covar, replicate_indices, *args, **kw_args):
        super(ShiftCF, self).__init__(*args, **kw_args)
        assert isinstance(covar, CovarianceFunction), 'ShiftCF: ShiftCF is constructed from a CovarianceFunction, which provides the partial derivative for the covariance matrix K with respect to input X'
        self.replicate_indices = replicate_indices
        self.n_replicates = len(sp.unique(replicate_indices))
        self.n_hyperparameters = covar.get_number_of_parameters() + self.n_replicates
        self.covar = covar

    def get_reparametrized_theta(self, theta):
        covar_n_hyper = self.covar.get_number_of_parameters()
        return sp.concatenate((self.covar.get_reparametrized_theta(theta[:covar_n_hyper]), theta[covar_n_hyper:]))

    def get_de_reparametrized_theta(self, theta):
        covar_n_hyper = self.covar.get_number_of_parameters()
        return sp.concatenate((self.covar.get_de_reparametrized_theta(theta[:covar_n_hyper]), theta[covar_n_hyper:]))

    def get_timeshifts(self, theta):
        covar_n_hyper = self.covar.get_number_of_parameters()
        return theta[covar_n_hyper:]

    def get_hyperparameter_names(self):
        """return the names of hyperparameters to make identificatio neasier"""
        return sp.concatenate((self.covar.get_hyperparameter_names(), [ 'Time-Shift rep%i' % i for i in sp.unique(self.replicate_indices) ]))

    def K(self, theta, x1, x2=None):
        """
        Get Covariance matrix K with given hyperparameters
        theta and inputs x1 and x2. The result
        will be the covariance of the covariance
        function given, calculated on the shifted inputs x1,x2.
        The shift is determined by the last n_replicate parameters of
        theta, where n_replicate is the number of replicates this
        CF conducts.

        **Parameters:**

        theta : [double]
            the hyperparameters of this CF. Its structure is as follows:
            [theta of covar, time-shift-parameters]
        
        Others see :py:class:`pygp.covar.CovarianceFunction` 
        """
        assert theta.shape[0] == self.n_hyperparameters, 'ShiftCF: K: theta has wrong shape'
        covar_n_hyper = self.covar.get_number_of_parameters()
        T = theta[covar_n_hyper:covar_n_hyper + self.n_replicates]
        shift_x1 = self._shift_x(x1.copy(), T)
        K = self.covar.K(theta[:covar_n_hyper], shift_x1, x2)
        return K

    def Kgrad_theta(self, theta, x, i):
        """
        Get Covariance matrix K with given hyperparameters
        theta and inputs x1 and x2. The result
        will be the covariance of the covariance
        function given, calculated on the shifted inputs x1,x2.
        The shift is determined by the last n_replicate parameters of
        theta, where n_replicate is the number of replicates this
        CF conducts.

        **Parameters:**

        theta : [double]
            the hyperparameters of this CF. Its structure is as follows::
            [theta of covar, time-shift-parameters]

        i : int
            the partial derivative of the i-th
            hyperparameter shal be returned. 
            
        """
        assert theta.shape[0] == self.n_hyperparameters, 'ShiftCF: K: theta has wrong shape'
        covar_n_hyper = self.covar.get_number_of_parameters()
        T = theta[covar_n_hyper:covar_n_hyper + self.n_replicates]
        shift_x = self._shift_x(x.copy(), T)
        if i >= covar_n_hyper:
            Kdx = self.covar.Kgrad_x(theta[:covar_n_hyper], shift_x, shift_x, 0)
            c = sp.array(self.replicate_indices == i - covar_n_hyper, dtype='int').reshape(-1, 1)
            cdist = dist(c, c)
            cdist = cdist.transpose(2, 0, 1)
            try:
                return Kdx * cdist
            except ValueError:
                return Kdx

        else:
            return self.covar.Kgrad_theta(theta[:covar_n_hyper], shift_x, i)

    def _shift_x(self, x, T):
        if x.shape[0] == self.replicate_indices.shape[0]:
            for i, ri in enumerate(sp.unique(self.replicate_indices)):
                x[(self.replicate_indices == ri)] -= T[i]

        return x