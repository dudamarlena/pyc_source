# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/pygp/likelihood/likelihood_base.py
# Compiled at: 2013-04-10 06:45:39
import scipy as SP
from pygp.linalg import *
import pdb, copy

class ALik(object):
    """abstract class for arbitrary likelihood model"""
    pass


class GaussGroupLikISO(ALik):
    """Gaussian isotropic noise with a specific noise parameter per group
    """

    def __init__(self, n_groups=2, column=0):
        self.n_hyperparameters = n_groups
        self.column = column

    def get_number_of_parameters(self):
        return self.n_hyperparameters

    def K(self, theta, x1):
        return SP.diag(self.Kdiag(theta, x1))

    def Kdiag(self, theta, x1):
        sigma = SP.exp(2 * theta)
        Knoise = SP.zeros([x1.shape[0]])
        for i in xrange(len(theta)):
            Knoise += sigma[i] * (1.0 * (x1[:, self.column] == i))

        return Knoise

    def Kgrad_theta(self, theta, x1, i):
        """
        The derivative of the covariance matrix with
        respect to i-th hyperparameter.

        **Parameters:**
        See :py:class:`pygp.covar.CovarianceFunction`
        """
        sigma = SP.exp(2 * theta[i])
        Knoise = SP.diag(2 * sigma * (1.0 * (x1[:, self.column] == i)))
        return Knoise


class GaussLikISO(ALik):
    """Gaussian isotropic likelihood model
    This may serve as a blueprint for other more general likelihood models
    _get_Knoise serves as an effective component of the covariance funciton and may be adapted as needed.
    """

    def __init__(self):
        self.n_hyperparameters = 1

    def get_number_of_parameters(self):
        return self.n_hyperparameters

    def K(self, theta, x1):
        sigma = SP.exp(2 * theta[0])
        Knoise = sigma * SP.eye(x1.shape[0])
        return Knoise

    def Kdiag(self, theta, x1):
        sigma = SP.exp(2 * theta)
        return sigma * SP.ones(x1.shape[0])

    def Kgrad_theta(self, theta, x1, i):
        """
        The derivative of the covariance matrix with
        respect to i-th hyperparameter.

        **Parameters:**
        See :py:class:`pygp.covar.CovarianceFunction`
        """
        K = self.K(theta, x1)
        assert i == 0, 'unknown hyperparameter'
        return 2 * K


class GaussLikARD(ALik):
    """Gaussian likelihood model with one noise level per dimension
    Note: currently this is only supported in gplvm module
    """

    def __init__(self, n_dimensions=1):
        self.n_dimensions = n_dimensions
        self.n_hyperparameters = n_dimensions

    def get_number_of_parameters(self):
        return self.n_hyperparameters

    def K(self, theta, x1):
        sigma = SP.exp(2 * theta[0])
        Knoise = sigma * SP.eye(x1.shape[0])
        return Knoise

    def Kdiag(self, theta, x1):
        sigma = SP.exp(2 * theta)
        RV = SP.tile(sigma[SP.newaxis, :], [x1.shape[0], 1])
        return RV

    def Kgrad_theta(self, theta, x1, i):
        """
        The derivative of the covariance matrix with
        respect to i-th hyperparameter.

        **Parameters:**
        See :py:class:`pygp.covar.CovarianceFunction`
        """
        K = self.Kdiag(theta, x1)[:, i]
        return 2 * K


def n2mode(x):
    """convert from natural parameter to mode and back"""
    return SP.array([x[0] / x[1], 1 / x[1]])


def sigmoid(x):
    """sigmoid function int_-inf^+inf Normal(x,1)"""
    return (1 + SP.special.erf(x / SP.sqrt(2.0))) / 2.0


def gos(x):
    """Gaussian over sigmoid"""
    return SP.sqrt(2.0 / SP.pi) * SP.exp(-0.5 * x ** 2) / (1 + SP.special.erf(x / SP.sqrt(2.0)))


class ProbitLik(ALik):
    """Probit likelihood for GP classification"""

    def get_number_of_parameters(self):
        return 0

    def K(self, theta, x1):
        zi = x1 * theta[0] / SP.sqrt(theta[1] * (1 + theta[1]))
        K = theta[0] / theta[1] + x1 * gos(zi) / SP.sqrt(theta[1] * (1 + theta[1]))
        return SP.diag(K)

    def Kdiag(self, theta, x1):
        zi = x1 * theta[0] / SP.sqrt(theta[1] * (1 + theta[1]))
        K = theta[0] / theta[1] + x1 * gos(zi) / SP.sqrt(theta[1] * (1 + theta[1]))
        return SP.squeeze(K)

    def Kgrad_theta(self, theta, x1, i):
        """
        The derivative of the covariance matrix with
        respect to i-th hyperparameter.

        **Parameters:**
        See :py:class:`pygp.covar.CovarianceFunction`
        """
        zi = x1 * theta[0] / SP.sqrt(theta[1] * (1 + theta[1]))
        Kgrad = (1 - gos(zi) * (zi + gos(zi)) / (1 + theta[1])) / theta[1]
        return Kgrad