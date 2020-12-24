# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/joao/postdoc1/JeffreysPrior/build/lib/loguniform/LogUniform.py
# Compiled at: 2018-05-24 10:17:35
# Size of source mod 2**32: 8515 bytes
import numpy as np
from abc import ABC, abstractmethod

class dist(ABC):
    __doc__ = ' \n    A simple distribution class.\n    Requires the implementation of properties `a` and `b`, representing the \n    bounds of the distribution, and methods `pdf`, `cdf` for the probability \n    and cumulative density functions and `ppf` for the inverse of `cdf`.\n    '

    @property
    @abstractmethod
    def a(self):
        pass

    @property
    @abstractmethod
    def b(self):
        pass

    def _support_mask(self, x):
        return (self.a <= x) & (x <= self.b)

    def _separate_support_mask(self, x):
        return (
         self.a <= x, x <= self.b)

    @abstractmethod
    def pdf(self, x):
        """ Probability density function evaluated at x. """
        pass

    @abstractmethod
    def cdf(self, x):
        """ Cumulative density function evaluated at x. """
        pass

    @abstractmethod
    def ppf(self, x):
        """ Percent point function (inverse of `cdf`) evaluated at q. """
        pass

    def sf(self, x):
        """ Survival function (1 - `cdf`) evaluated at x. """
        return 1 - self.cdf(x)

    def rvs(self, size=1):
        """
        Random samples from the distribution.

        Parameters
        ----------
        size : int or tuple of ints, optional
            Number of random samples to draw (default is 1).

        Returns
        -------
        rvs : ndarray or scalar
        """
        u = np.random.uniform(size=size)
        s = self.ppf(u)
        if size == 1:
            return np.asscalar(s)
        else:
            return s

    def interval(self, alpha):
        """
        Confidence interval with equal areas around the median.

        Parameters
        ----------
        alpha : array_like of float
            Probability that an rv will be drawn from the returned range.
            Each value should be in the range [0, 1].

        Returns
        -------
        a, b : ndarray of float
            end-points of range that contains 100 * alpha % of the
            distribution support.
        """
        alpha = np.asarray(alpha)
        if np.any((alpha > 1) | (alpha < 0)):
            raise ValueError('alpha must be between 0 and 1 inclusive')
        q1 = (1.0 - alpha) / 2
        q2 = (1.0 + alpha) / 2
        a = self.ppf(q1)
        b = self.ppf(q2)
        return (a, b)


class LogUniform(dist):
    __doc__ = ' \n    A log-uniform distribution, sometimes called "reciprocal" or, in some\n    contexts, used as a "Jeffreys prior".\n\n    Parameters\n    ----------\n    a, b : float\n           Lower and upper bounds of the distribution.\n    \n    Methods\n    -------\n    pdf    : probability density function\n    logpdf : logarithm of the probability density function\n    cdf    : cumulative density function\n    ppf    : percent point function (inverse of cdf)\n\n    Properties\n    ----------\n    mean, mode, var, std, skewness, kurtosis\n\n    '
    a = None
    b = None

    def __init__(self, a, b):
        if not (a > 0 and b > 0):
            raise AssertionError('parameters `a` and `b` must both be positive')
        elif not b > a:
            raise AssertionError('upper limit `b` cannot be less than or equal to lower limit `a`')
        self.a, self.b = a, b
        self.q = np.log(self.b) - np.log(self.a)

    def pdf(self, x):
        x = np.asarray(x)
        m = self._support_mask(x)
        with np.errstate(divide='ignore'):
            return np.where(m, 1 / (x * self.q), 0.0)

    def logpdf(self, x):
        x = np.asarray(x)
        m = self._support_mask(x)
        with np.errstate(divide='ignore'):
            return np.where(m, -np.log(x * np.log(self.q)), -np.inf)

    def cdf(self, x):
        x = np.asarray(x)
        m1, m2 = self._separate_support_mask(x)
        return np.where(m2, np.where(m1, np.log(x / self.a) / self.q, 0.0), 1.0)

    def ppf(self, p):
        return np.exp(np.log(self.a) + p * self.q)

    @property
    def mean(self):
        return (self.b - self.a) / self.q

    @property
    def mode(self):
        return self.a

    @property
    def var(self):
        a, b, q = self.a, self.b, self.q
        return (b - a) * (b * (q - 2) + a * (q + 2)) / (2 * q ** 2)

    @property
    def std(self):
        return np.sqrt(self.var)

    @property
    def skewness(self):
        a, b, q = self.a, self.b, self.q
        f1 = np.sqrt(2) * (12 * q * (a - b) ** 2 + q ** 2 * (b ** 2 * (2 * q - 9) + 2 * a * b * q + a ** 2 * (2 * q + 9)))
        f2 = 3 * q * np.sqrt(b - a) * (b * (q - 2) + a * (q + 2)) ** 1.5
        return f1 / f2

    @property
    def kurtosis(self):
        a, b, q = self.a, self.b, self.q
        f1 = 36 * q * (b - a) ** 2 * (a + b) - 36 * (b - a) ** 3 - 16 * q ** 2 * (b ** 3 - a ** 3) + 3 * q ** 3 * (b ** 2 + a ** 2) * (a + b)
        f2 = 3 * (b - a) * (b * (q - 2) + a * (q + 2)) ** 2
        return f1 / f2 - 3


class ModifiedLogUniform(dist):
    __doc__ = ' \n    A modified log-uniform distribution, sometimes called a "modified Jeffreys prior".\n    The support of the distribution includes zero.\n\n    Parameters\n    ----------\n    knee : float\n           Point where the distribution changes from uniform to log-uniform.\n    b    : float\n           Upper bound of the distribution.\n    \n    Methods\n    -------\n    pdf    : probability density function\n    logpdf : logarithm of the probability density function\n    cdf    : cumulative density function\n    ppf    : percent point function (inverse of cdf)\n\n    Properties\n    ----------\n    mean, mode, var, std, skewness, kurtosis\n\n    '
    a = 0
    b = 100
    knee = 1

    def __init__(self, knee, b):
        if not b > 0:
            raise AssertionError('upper limit `b` must be positive')
        else:
            assert knee > 0, '`knee` must be positive'
            assert b > knee, 'upper limit `b` must be larger than `knee`'
        self.b = b
        self.knee = knee
        self.q = np.log((self.b + self.knee) / self.knee)

    def pdf(self, x):
        x = np.asarray(x)
        m = self._support_mask(x)
        with np.errstate(divide='ignore'):
            return np.where(m, 1 / ((x + self.knee) * self.q), 0.0)

    def logpdf(self, x):
        x = np.asarray(x)
        m = self._support_mask(x)
        with np.errstate(divide='ignore'):
            return np.where(m, -np.log(x + self.knee) - np.log(self.q), -np.inf)

    def cdf(self, x):
        r = self.b / self.knee
        return np.log(x / self.knee + 1) / np.log(r + 1)

    def ppf(self, p, *args):
        return self.knee * (-1 + np.exp(np.log(self.b / self.knee + 1) * p))

    @property
    def mean(self):
        b, knee, q = self.b, self.knee, self.q
        return (b + knee * np.log(knee) - knee * np.log(knee + b)) / q

    @property
    def mode(self):
        return self.a

    @property
    def var(self):
        b, knee, q = self.b, self.knee, self.q
        mu = self.mean
        return (b ** 2 - 2 * b * knee - 2 * knee ** 2 * np.log(knee) + 2 * knee ** 2 * np.log(knee + b) + (4 * knee * np.log(knee + b) - 4 * knee * np.log(knee) - 4 * b) * mu + (2 * np.log(knee + b) - 2 * np.log(knee)) * mu ** 2) / (2 * q)

    @property
    def std(self):
        return np.sqrt(self.var)

    @property
    def skewness(self):
        b, knee, q = (self.b, self.knee, self.q)
        mu = self.mean
        var = self.var
        return -(-2 * b ** 3 + 3 * b ** 2 * knee - 6 * b * knee ** 2 - 6 * knee ** 3 * np.log(knee) + 6 * knee ** 3 * np.log(knee + b) + (18 * knee ** 2 * np.log(knee + b) - 18 * knee ** 2 * np.log(knee) - 18 * b * knee + 9 * b ** 2) * mu + (18 * knee * np.log(knee + b) - 18 * knee * np.log(knee) - 18 * b) * mu ** 2 + (6 * np.log(knee + b) - 6 * np.log(knee)) * mu ** 3) / (6 * q * var ** (3 / 2))

    @property
    def kurtosis(self):
        b, knee, q = (self.b, self.knee, self.q)
        mu = self.mean
        var = self.var
        return -(-3 * b ** 4 + 4 * b ** 3 * knee - 6 * b ** 2 * knee ** 2 + 12 * b * knee ** 3 + 12 * knee ** 4 * np.log(knee) - 12 * knee ** 4 * np.log(knee + b) + (-48 * knee ** 3 * np.log(knee + b) + 48 * knee ** 3 * np.log(knee) + 48 * b * knee ** 2 - 24 * b ** 2 * knee + 16 * b ** 3) * mu + (-72 * knee ** 2 * np.log(knee + b) + 72 * knee ** 2 * np.log(knee) + 72 * b * knee - 36 * b ** 2) * mu ** 2 + (-48 * knee * np.log(knee + b) + 48 * knee * np.log(knee) + 48 * b) * mu ** 3 + (12 * np.log(knee) - 12 * np.log(knee + b)) * mu ** 4 + 36 * q * var ** 2) / (12 * q * var ** 2)