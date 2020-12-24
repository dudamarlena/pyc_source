# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/pygp/covar/se.py
# Compiled at: 2013-04-10 06:45:39
"""
Squared Exponential Covariance functions
========================================

This class provides some ready-to-use implemented squared exponential covariance functions (SEs).
These SEs do not model noise, so combine them by a :py:class:`pygp.covar.combinators.SumCF`
or :py:class:`pygp.covar.combinators.ProductCF` with the :py:class:`pygp.covar.noise.NoiseISOCF`, if you want noise to be modelled by this GP.
"""
import numpy
from pygp.covar.covar_base import BayesianStatisticsCF, CovarianceFunction
from pygp.covar import dist

class SqexpCFARD(CovarianceFunction):
    """
    Standart Squared Exponential Covariance function.

    **Parameters:**
    
    - dimension : int
        The dimension of this SE. For instance a 2D SE has
        hyperparameters like::
        
          covar_hyper = [Amplitude,1stD Length-Scale, 2ndD Length-Scale]

    - dimension_indices : [int]
        Optional: The indices of the get_n_dimensions() in the input.
        For instance the get_n_dimensions() of inputs are in 2nd and
        4th dimension dimension_indices would have to be [1,3].

    """

    def __init__(self, *args, **kwargs):
        super(SqexpCFARD, self).__init__(*args, **kwargs)
        self.n_hyperparameters = self.get_n_dimensions() + 1

    def get_hyperparameter_names(self):
        """
        return the names of hyperparameters to
        make identification easier
        """
        names = []
        names.append('SECF Amplitude')
        for dim in self.get_dimension_indices():
            names.append(('{0!s:>%is}D Length-Scale' % len(str(self.get_dimension_indices().max()))).format(dim))

        return names

    def get_number_of_parameters(self):
        """
        Return the number of hyperparameters this CF holds.
        """
        return self.get_n_dimensions() + 1

    def K(self, theta, x1, x2=None):
        r"""
        Get Covariance matrix K with given hyperparameters
        and inputs X=x1 and X\`*`=x2.

        **Parameters:**
        See :py:class:`pygp.covar.CovarianceFunction`
        """
        x1, x2 = self._filter_input_dimensions(x1, x2)
        V0 = numpy.exp(2 * theta[0])
        L = numpy.exp(theta[1:1 + self.get_n_dimensions()])
        sqd = dist.sq_dist(x1 / L, x2 / L)
        rv = V0 * numpy.exp(-0.5 * sqd)
        return rv

    def Kdiag(self, theta, x1):
        """
        Get diagonal of the (squared) covariance matrix.

        **Parameters:**
        See :py:class:`pygp.covar.CovarianceFunction`
        """
        x1 = self._filter_x(x1)
        V0 = numpy.exp(2 * theta[0])
        return V0 * numpy.exp(0) * numpy.ones([x1.shape[0]])

    def Kgrad_theta(self, theta, x1, i):
        """
        The derivatives of the covariance matrix for
        each hyperparameter, respectively.

        **Parameters:**
        See :py:class:`pygp.covar.CovarianceFunction`
        """
        x1 = self._filter_x(x1)
        V0 = numpy.exp(2 * theta[0])
        L = numpy.exp(theta[1:1 + self.get_n_dimensions()])
        x1_ = x1 / L
        d = dist.dist(x1_)
        sqd = d * d
        sqdd = sqd.sum(-1)
        rv0 = V0 * numpy.exp(-0.5 * sqdd)
        if i == 0:
            return 2 * rv0
        else:
            grad = rv0 * sqd[:, :, i - 1]
            return grad

    def Kgrad_x(self, theta, x1, x2, d):
        """
        The partial derivative of the covariance matrix with
        respect to x, given hyperparameters `theta`.

        **Parameters:**
        See :py:class:`pygp.covar.CovarianceFunction`
        """
        if d not in self.get_dimension_indices():
            return numpy.zeros([x1.shape[0], x2.shape[0]])
        rv = self.K(theta, x1, x2)
        x1, x2 = self._filter_input_dimensions(x1, x2)
        d -= self.get_dimension_indices().min()
        L2 = numpy.exp(2 * theta[1:1 + self.get_n_dimensions()])
        nsdist = dist.dist(x1, x2)[:, :, d] / L2[d]
        return rv * nsdist

    def Kgrad_xdiag(self, theta, x1, d):
        """"""
        RV = numpy.zeros([x1.shape[0]])
        return RV

    def get_ard_dimension_indices(self):
        return numpy.array(self.get_dimension_indices() + 1, dtype='int')


class SqexpCFARDInv(CovarianceFunction):
    """
    Standart Squared Exponential Covariance function.

    **Parameters:**
    
    - dimension : int
        The dimension of this SE. For instance a 2D SE has
        hyperparameters like::
        
          covar_hyper = [Amplitude,1stD Length-Scale, 2ndD Length-Scale]

    - dimension_indices : [int]
        Optional: The indices of the get_n_dimensions() in the input.
        For instance the get_n_dimensions() of inputs are in 2nd and
        4th dimension dimension_indices would have to be [1,3].

    """

    def __init__(self, n_dimensions=-1, dimension_indices=None):
        super(SqexpCFARDInv, self).__init__(n_dimensions, dimension_indices)
        self.n_hyperparameters = self.get_n_dimensions() + 1

    def get_hyperparameter_names(self):
        """
        return the names of hyperparameters to
        make identification easier
        """
        names = []
        names.append('SECF Amplitude')
        for dim in self.get_dimension_indices():
            names.append(('SECF ARD {0:%s}' % len(str(self.get_dimension_indices().max()))).format(dim))

        return names

    def get_number_of_parameters(self):
        """
        Return the number of hyperparameters this CF holds.
        """
        return self.get_n_dimensions() + 1

    def K(self, theta, x1, x2=None):
        r"""
        Get Covariance matrix K with given hyperparameters
        and inputs X=x1 and X\`*`=x2.

        **Parameters:**
        See :py:class:`pygp.covar.CovarianceFunction`
        """
        x1, x2 = self._filter_input_dimensions(x1, x2)
        V0 = numpy.exp(-2 * theta[0])
        L = numpy.exp(theta[1:1 + self.get_n_dimensions()])
        Linv = L
        sqd = dist.sq_dist(x1 * Linv, x2 * Linv)
        rv = V0 * numpy.exp(-0.5 * sqd)
        return rv

    def Kdiag(self, theta, x1):
        """
        Get diagonal of the (squared) covariance matrix.

        **Parameters:**
        See :py:class:`pygp.covar.CovarianceFunction`
        """
        x1 = self._filter_x(x1)
        V0 = numpy.exp(-2 * theta[0])
        return V0 * numpy.exp(0) * numpy.ones([x1.shape[0]])

    def Kgrad_theta(self, theta, x1, i):
        """
        The derivatives of the covariance matrix for
        each hyperparameter, respectively.

        **Parameters:**
        See :py:class:`pygp.covar.CovarianceFunction`
        """
        x1 = self._filter_x(x1)
        V0 = numpy.exp(-2 * theta[0])
        L = numpy.exp(theta[1:1 + self.get_n_dimensions()])
        Linv = L
        x1_ = x1 * Linv
        d = dist.dist(x1_, x1_)
        sqd = d * d
        sqdd = sqd.sum(axis=2)
        rv0 = V0 * numpy.exp(-0.5 * sqdd)
        if i == 0:
            return -2 * rv0
        else:
            return rv0 * -sqd[:, :, i - 1]

    def Kgrad_x(self, theta, x1, x2, d):
        """
        The partial derivative of the covariance matrix with
        respect to x, given hyperparameters `theta`.

        **Parameters:**
        See :py:class:`pygp.covar.CovarianceFunction`
        """
        if d not in self.get_dimension_indices() and self.get_n_dimensions() > 0:
            return numpy.zeros([x1.shape[0], x2.shape[0]])
        rv = self.K(theta, x1, x2)
        x1, x2 = self._filter_input_dimensions(x1, x2)
        d -= self.get_dimension_indices().min()
        L2 = numpy.exp(2 * theta[1:1 + self.get_n_dimensions()])
        nsdist = dist.dist(x1, x2)[:, :, d] * L2[d]
        return rv * nsdist

    def Kgrad_xdiag(self, theta, x1, d):
        """"""
        RV = numpy.zeros([x1.shape[0]])
        return RV

    def get_reparametrized_theta(self, theta):
        theta = theta.copy()
        theta[0] = -theta[0]
        rep = numpy.exp(2 * theta)
        return rep

    def get_de_reparametrized_theta(self, theta):
        rep = 0.5 * numpy.log(theta)
        rep[0] = -rep[0]
        return rep

    def get_ard_dimension_indices(self):
        return numpy.array(self.dimension_indices + 1, dtype='int')


class SqexpCFARDPsiStat(SqexpCFARDInv, BayesianStatisticsCF):

    def update_stats(self, theta, mean, variance, inducing_variables):
        super(SqexpCFARDPsiStat, self).update_stats(theta, mean, variance, inducing_variables)
        self.reparametrize()
        self.sigma = self.theta[0]
        self.alpha = self.theta[1:1 + self.get_n_dimensions()]
        self.dist_mu_Z = self.mean[:, None] - self.inducing_variables
        self.dist_mu_Z_sq = self.dist_mu_Z ** 2
        alpha_variance = self.alpha * self.variance
        self.norm_full = alpha_variance + 1
        self.norm_half = alpha_variance + 0.5
        self.dist_Z_Z = self.inducing_variables[:, None] - self.inducing_variables
        self.dist_Z_Z_sq = self.dist_Z_Z ** 2
        self.Z_hat = (self.inducing_variables[:, None] + self.inducing_variables) / 2.0
        self.dist_mu_Z_hat = self.mean[:, None, None] - self.Z_hat
        self.dist_mu_Z_hat_sq = self.dist_mu_Z_hat ** 2
        self.psi1 = self._psi_1()
        self.psi2_n_expanded = self.sigma ** 2 * numpy.exp(self._psi_2_exponent().sum(-1))
        self.psi2 = self.psi2_n_expanded.sum(0)
        return

    def reparametrize(self):
        self.theta = self.get_reparametrized_theta(self.theta)
        self.variance = numpy.exp(2 * self.variance)

    def psi(self):
        try:
            assert self.theta.shape[0] == self.get_number_of_parameters()
        except NameError:
            raise BayesianStatisticsCF.CacheMissingError('Cache missing, perhaps a missing self.update_stats!')
        except AssertionError:
            raise CovarianceFunction.HyperparameterError('Wrong number of parameters!')

        psi_0 = self.N * self.sigma
        psi_1 = self.psi1
        psi_2 = self.psi2
        return [
         psi_0, psi_1, psi_2]

    def psigrad_theta(self):
        psi_0 = numpy.zeros(self.get_number_of_parameters())
        psi_0[0] = self.N * -2 * self.sigma
        psi_1 = numpy.tile(self.psi1[:, :, None], self.get_number_of_parameters())
        psi_1[:, :, 0] *= -2
        psi_1_inner = self.dist_mu_Z_sq / (self.norm_full ** 2)[:, None]
        psi_1_inner += (self.variance / self.norm_full)[:, None]
        psi_1[:, :, 1:] *= -self.alpha * psi_1_inner
        psi_2 = numpy.zeros((self.M, self.M, self.get_number_of_parameters()))
        psi_2[:, :, 0] = self.psi2 * -4
        psi_2_inner = 0.5 * self.dist_mu_Z_hat_sq / (self.norm_half ** 2)[:, None, None]
        psi_2_inner += (0.5 * self.dist_Z_Z_sq)[None]
        psi_2_inner += (self.variance / self.norm_half)[:, None, None]
        psi_2_inner *= -1.0 * self.alpha
        psi_2[:, :, 1:] = (psi_2_inner * self.psi2_n_expanded[:, :, :, None]).sum(0)
        return (
         psi_0[:, None], psi_1[:, :, :, None], psi_2[:, :, :, None])

    def psigrad_inducing_variables(self):
        psi_0 = 0
        psi_1_inner = self.alpha * self.dist_mu_Z / self.norm_full[:, None]
        psi_1_outer = self.psi1[:, :, None] * psi_1_inner
        psi_1 = numpy.eye(self.M, self.M)[None, :, :, None] * psi_1_outer[:, :, None]
        psi_1 = psi_1
        psi_2_inner = -0.5 * self.alpha * (self.dist_Z_Z[None] - self.dist_mu_Z_hat / self.norm_half[:, None, None])
        psi_2_inner = numpy.eye(self.M)[None, :, None, :, None] * psi_2_inner[:, :, :, None]
        psi_2_inner *= self.psi2_n_expanded[:, :, :, None, None]
        psi_2_inner = psi_2_inner + psi_2_inner.swapaxes(1, 2)
        psi_2 = psi_2_inner.sum(0)
        psi_2 = psi_2.swapaxes(0, 1)
        return (
         psi_0, psi_1, psi_2)

    def psigrad_mean(self):
        psi_0 = 0
        psi_1_inner = -self.alpha * self.dist_mu_Z / self.norm_full[:, None]
        psi_1 = self.psi1[:, :, None] * psi_1_inner
        psi_1 = psi_1[:, :, None, :]
        psi_2_inner = -self.alpha * self.dist_mu_Z_hat / self.norm_half[:, None, None]
        psi_2 = psi_2_inner * self.psi2_n_expanded[:, :, :, None]
        psi_2 = psi_2.swapaxes(0, 2)
        return (
         psi_0, psi_1, psi_2)

    def psigrad_variance(self):
        psi_0 = 0
        psi_1_inner = -(self.alpha ** 2 * self.dist_mu_Z_sq) / self.norm_full[:, None]
        psi_1_inner += self.alpha
        psi_1 = self.psi1[:, :, None] * -(psi_1_inner / self.norm_full[:, None]) * self.variance[:, None]
        psi_1 = psi_1[:, :, None]
        psi_2_inner = self.alpha * self.dist_mu_Z_hat_sq / self.norm_half[:, None, None] - 1
        psi_2 = self.psi2_n_expanded[:, :, :, None] * 0.5 * self.alpha * (psi_2_inner / self.norm_half[:, None, None])
        psi_2 = psi_2.swapaxes(0, 2) * 2 * self.variance[(None, None)]
        return [
         psi_0, psi_1, psi_2]

    def _psi_1(self):
        summand = -0.5 * (self.alpha * self.dist_mu_Z_sq / self.norm_full[:, None] + numpy.log(self.norm_full[:, None]))
        return self.sigma * numpy.exp(summand.sum(-1))

    def _psi_2_exponent(self):
        summand = -0.5 * (self.alpha * ((0.5 * self.dist_Z_Z_sq)[None] + self.dist_mu_Z_hat_sq / self.norm_half[:, None, None]) + numpy.log(2 * self.norm_half[:, None, None]))
        return summand