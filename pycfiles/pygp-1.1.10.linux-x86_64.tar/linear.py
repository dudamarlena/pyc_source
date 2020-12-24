# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/pygp/covar/linear.py
# Compiled at: 2013-04-10 06:45:39
"""
Classes for linear covariance function
======================================
Linear covariance functions

LinearCFISO
LinearCFARD

"""
import numpy
from pygp.covar.covar_base import BayesianStatisticsCF, CovarianceFunction

class LinearCFISO(CovarianceFunction):
    """
    isotropic linear covariance function with a single hyperparameter
    """

    def __init__(self, *args, **kw_args):
        super(LinearCFISO, self).__init__(*args, **kw_args)
        self.n_hyperparameters = 1

    def K(self, theta, x1, x2=None):
        x1, x2 = self._filter_input_dimensions(x1, x2)
        A = numpy.exp(2 * theta[0])
        RV = A * numpy.dot(x1, x2.T)
        return RV

    def Kdiag(self, theta, x1):
        x1 = self._filter_x(x1)
        RV = numpy.dot(x1, x1.T).sum(axis=1)
        RV *= 2
        return RV

    def Kgrad_theta(self, theta, x1, i):
        assert i == 0, 'LinearCF: Kgrad_theta: only one hyperparameter for linear covariance'
        RV = self.K(theta, x1)
        RV *= 2
        return RV

    def Kgrad_x(self, theta, x1, x2, d):
        x1, x2 = self._filter_input_dimensions(x1, x2)
        RV = numpy.zeros([x1.shape[0], x2.shape[0]])
        if d not in self.get_dimension_indices():
            return RV
        d -= self.get_dimension_indices().min()
        A = numpy.exp(2 * theta[0])
        RV[:, :] = A * x2[:, d]
        return RV

    def Kgrad_xdiag(self, theta, x1, d):
        """derivative w.r.t diagonal of self covariance matrix"""
        x1 = self._filter_x(x1)
        RV = numpy.zeros([x1.shape[0]])
        if d not in self.get_dimension_indices():
            return RV
        d -= self.get_dimension_indices().min()
        A = numpy.exp(2 * theta[0])
        RV[:] = 2 * A * x1[:, d]
        return RV

    def get_hyperparameter_names(self):
        names = []
        names.append('LinearCFISO Amplitude')
        return names


class LinearCF(CovarianceFunction):

    def __init__(self, n_dimensions=1, dimension_indices=None):
        super(LinearCF, self).__init__(n_dimensions, dimension_indices)
        self.n_hyperparameters = self.get_n_dimensions()

    def get_reparametrized_theta(self, theta):
        return numpy.exp(2 * theta)

    def get_ard_dimension_indices(self):
        return numpy.array(self.dimension_indices, dtype='int')

    def get_de_reparametrized_theta(self, theta):
        return 0.5 * numpy.log(theta)

    def get_hyperparameter_names(self):
        return [ 'Linear ARD %i' % i for i in self.get_dimension_indices() ]

    def K(self, logtheta, x1, x2=None):
        x1, x2 = self._filter_input_dimensions(x1, x2)
        if self.get_n_dimensions() > 0:
            M = numpy.diag(numpy.exp(2 * logtheta[:self.get_n_dimensions()]))
            RV = numpy.dot(numpy.dot(x1, M), x2.T)
        else:
            RV = numpy.zeros([x1.shape[0], x2.shape[0]])
        return RV

    def Kgrad_theta(self, logtheta, x1, i):
        iid = self.get_dimension_indices()[i]
        Li = numpy.exp(2 * logtheta[i])
        RV = 2 * Li * numpy.dot(x1[:, iid:iid + 1], x1[:, iid:iid + 1].T)
        return RV

    def Kgrad_x(self, logtheta, x1, x2, d):
        RV = numpy.zeros([x1.shape[0], x2.shape[0]])
        if d not in self.get_dimension_indices():
            return RV
        i = numpy.nonzero(self.get_dimension_indices() == d)[0][0]
        A = numpy.exp(2 * logtheta[i])
        RV[:, :] = A * x2[:, d]
        return RV

    def Kgrad_xdiag(self, logtheta, x1, d):
        """derivative w.r.t diagonal of self covariance matrix"""
        RV = numpy.zeros([x1.shape[0]])
        if d not in self.get_dimension_indices():
            return RV
        i = numpy.nonzero(self.get_dimension_indices() == d)[0][0]
        A = numpy.exp(2 * logtheta[i])
        RV = numpy.zeros([x1.shape[0]])
        RV[:] = 2 * A * x1[:, d]
        return RV


class LinearCFARD(CovarianceFunction):
    """identical to LinearCF, however alternative paramerterisation of the ard parameters"""

    def __init__(self, n_dimensions=-1, dimension_indices=None):
        super(LinearCFARD, self).__init__(n_dimensions=n_dimensions, dimension_indices=dimension_indices)
        self.n_hyperparameters = self.get_n_dimensions()

    def get_hyperparameter_names(self):
        names = []
        names.append('Amplitude')
        return names

    def K(self, theta, x1, x2=None):
        if x2 is None:
            x2 = x1
        RV = numpy.dot(numpy.dot(x1[:, self.get_dimension_indices()], self._A(theta)), x2[:, self.get_dimension_indices()].T)
        return RV

    def Kgrad_theta(self, theta, x1, i):
        iid = self.get_dimension_indices()[i]
        Li = 1.0 / theta[i]
        RV = -1 * Li ** 2 * numpy.dot(x1[:, iid:iid + 1], x1[:, iid:iid + 1].T)
        return RV

    def Kgrad_x(self, theta, x1, x2, d):
        RV = numpy.zeros([x1.shape[0], x2.shape[0]])
        if d not in self.get_dimension_indices():
            return RV
        i = numpy.nonzero(self.get_dimension_indices() == d)[0][0]
        RV[:, :] = self._A(theta, i) * x2[:, d]
        return RV

    def Kgrad_xdiag(self, theta, x1, d):
        """derivative w.r.t diagonal of self covariance matrix"""
        RV = numpy.zeros([x1.shape[0]])
        if d not in self.get_dimension_indices():
            return RV
        i = numpy.nonzero(self.get_dimension_indices() == d)[0][0]
        RV = numpy.zeros([x1.shape[0]])
        RV[:] = 2 * self._A(theta, i) * x1[:, d]
        return RV

    def _A(self, theta, i=None):
        if i is None:
            return numpy.diagflat(1.0 / theta[0:self.get_n_dimensions()])
        else:
            return 1.0 / theta[i]


class LinearCFPsiStat(LinearCF, BayesianStatisticsCF):

    def __init__(self, *args, **kwargs):
        super(LinearCFPsiStat, self).__init__(*args, **kwargs)

    def update_stats(self, theta, mean, variance, inducing_variables):
        super(LinearCFPsiStat, self).update_stats(theta, mean, variance, inducing_variables)
        self.reparametrize()
        self.thetamean = self.theta * self.mean
        self.thetaindv = self.inducing_variables * self.theta
        self.K_inner = numpy.dot(self.mean.T, self.mean) + numpy.diag(numpy.sum(self.variance, 0))
        self.thetaindvK = numpy.dot(self.thetaindv, self.K_inner)
        self.psi1 = numpy.dot(self.mean, self.thetaindv.T)

    def reparametrize(self):
        self.theta = numpy.exp(2 * self.theta)
        self.variance = numpy.exp(2 * self.variance)

    def psi(self):
        try:
            assert self.theta.shape[0] == self.get_number_of_parameters()
        except AttributeError:
            raise type(self).CacheMissingError('Cache Missing: Perhaps a missing self.update_stats!')
        except AssertionError:
            raise type(self).HyperparameterError('Wrong number of parameters!')

        psi_0 = numpy.sum(self.theta * (self.mean ** 2 + self.variance))
        psi_1 = numpy.dot(self.mean, self.thetaindv.T)
        psi_2 = numpy.dot(self.thetaindv, numpy.dot(self.K_inner, self.thetaindv.T))
        return (psi_0, psi_1, psi_2)

    def psigrad_theta(self):
        """
        returns the gradients w.r.t. _...
        """
        psi_0grad_theta = 2 * numpy.sum(self.theta * (self.mean ** 2 + self.variance), 0)
        psi_1grad_theta = 2 * self.thetamean[:, None, :] * self.inducing_variables
        prod = self.thetaindvK[:, None] * self.thetaindv
        psi_2grad_theta = 2.0 * (prod.swapaxes(0, 1) + prod)
        return (psi_0grad_theta[:, None], psi_1grad_theta[:, :, :, None], psi_2grad_theta[:, :, :, None])

    def psigrad_mean(self):
        """
        returns the gradients w.r.t. _...
        """
        psi_0grad_mean = 2 * self.thetamean
        psi_1grad_mean = self.thetaindv[None, :, None]
        prod = self.psi1.T[:, None, :, None] * self.thetaindv[None, :, None]
        psi_2grad_mean = prod + prod.swapaxes(0, 1)
        return (psi_0grad_mean, psi_1grad_mean, psi_2grad_mean)

    def psigrad_variance(self):
        """
        returns the gradients w.r.t. _...
        """
        psi_0grad_variance = 2 * self.theta * self.variance
        psi_1grad_variance = 0
        psi_2grad_variance = 2 * self.variance * (self.thetaindv[:, None] * self.thetaindv)[:, :, None, :]
        return (psi_0grad_variance, psi_1grad_variance, psi_2grad_variance)

    def psigrad_inducing_variables(self):
        psi_1grad_inducing_variables = numpy.eye(self.M)[None, :, :, None] * self.thetamean[:, None, None, :]
        prod = numpy.eye(self.M)[:, None, :, None] * (self.thetaindvK * self.theta)[None, :, None]
        psi_2grad_inducing_variables = prod.swapaxes(0, 1) + prod
        return [0,
         psi_1grad_inducing_variables,
         psi_2grad_inducing_variables]