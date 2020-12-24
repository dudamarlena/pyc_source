# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/pygp/covar/delta.py
# Compiled at: 2013-04-10 06:45:39
"""
Classes for delta covariance function
======================================
Linear covariance functions

DeltaCFISO

"""
import scipy as SP
from pygp.covar.covar_base import CovarianceFunction
from pygp.covar import dist

class DeltaCFISO(CovarianceFunction):
    """
    Linear delta covaraince function
    """

    def __init__(self, *args, **kw_args):
        super(DeltaCFISO, self).__init__(*args, **kw_args)
        self.n_hyperparameters = 1

    def K(self, theta, x1, x2=None):
        x1, x2 = self._filter_input_dimensions(x1, x2)
        A = SP.exp(2 * theta[0])
        D = dist.dist(x1, x2)
        K = (D == 0).sum(axis=2)
        RV = A * K
        return RV

    def Kdiag(self, theta, x1):
        x1 = self._filter_x(x1)
        RV = SP.exp(2 * theta[0]) * x1.shape[1]
        return RV

    def Kgrad_theta(self, theta, x1, i):
        assert i == 0, 'LinearCF: Kgrad_theta: only one hyperparameter for linear covariance'
        RV = self.K(theta, x1)
        RV *= 2
        return RV

    def Kgrad_x(self, theta, x1, x2, d):
        RV = SP.zeros([x1.shape[0], x2.shape[0]])
        return RV

    def Kgrad_xdiag(self, theta, x1, d):
        """derivative w.r.t diagonal of self covariance matrix"""
        RV = SP.zeros([x1.shape[0]])
        return RV

    def get_hyperparameter_names(self):
        names = []
        names.append('DeltaCFISO Amplitude')
        return names


class DeltaCF(CovarianceFunction):
    """
    Linear delta covaraince function
    """

    def __init__(self, *args, **kw_args):
        super(DeltaCF, self).__init__(*args, **kw_args)
        self.n_hyperparameters = self.get_n_dimensions()

    def K(self, theta, x1, x2=None):
        x1, x2 = self._filter_input_dimensions(x1, x2)
        A = SP.exp(2 * theta)
        D = 1.0 * (dist.dist(x1, x2) == 0)
        K = SP.dot(D, A)
        return K

    def Kgrad_theta(self, theta, x1, i):
        A = 2 * SP.exp(2 * theta)
        D = 1.0 * (dist.dist(x1, x1) == 0)
        K = D[:, :, i] * A[i]
        return K

    def Kdiag(self, theta, x1):
        """self covariance"""
        if x1.shape[0] == self._K.shape[0]:
            return self._K.diagonal()
        else:
            return SP.zeros([x1.shape[0]])

    def Kgrad_x(self, theta, x1, x2, d):
        RV = SP.zeros([x1.shape[0], x2.shape[0]])
        return RV

    def Kgrad_xdiag(self, theta, x1, d):
        """derivative w.r.t diagonal of self covariance matrix"""
        RV = SP.zeros([x1.shape[0]])
        return RV

    def get_hyperparameter_names(self):
        names = []
        names.append('DeltaCFISO Amplitude')
        return names


def tri_flat(array):
    R = array.shape[0]
    mask = SP.asarray(SP.invert(SP.tri(R, R, dtype=bool)), dtype=float)
    x, y = mask.nonzero()
    return array[(x, y)]


class CovarCF(CovarianceFunction):
    """
    Covariance CF, with explicit parameters for covaraition between groups of different type
    """

    def __init__(self, n_groups=2, **kw_args):
        super(CovarCF, self).__init__(**kw_args)
        self.n_groups = n_groups
        self.n_hyperparameters = int(0.5 * n_groups * (n_groups - 1) + n_groups)

    def K(self, theta, x1, x2=None):
        x1, x2 = self._filter_input_dimensions(x1, x2)
        K = SP.zeros([x1.shape[0], x2.shape[0]])
        ic = 0
        for i in xrange(self.n_groups):
            for j in xrange(i + 1):
                A = theta[ic]
                x1_ = x1 == i
                x2_ = x2 == j
                K0_ = SP.outer(x1_, x2_) | SP.outer(x2_, x1_)
                K += A * K0_
                ic += 1

        return K

    def Kgrad_theta(self, theta, x1, d):
        K = SP.zeros([x1.shape[0], x1.shape[0]])
        ic = 0
        for i in xrange(self.n_groups):
            for j in xrange(i + 1):
                if ic == d:
                    A = 1.0
                    x1_ = x1 == i
                    x2_ = x1 == j
                    K0_ = SP.outer(x1_, x2_) | SP.outer(x2_, x1_)
                    K = A * K0_
                    return K
                ic += 1

        return K

    def get_hyperparameter_names(self):
        names = []
        names.append('DeltaCFISO Amplitude')
        return names