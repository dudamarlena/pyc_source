# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gleipnir/distributions.py
# Compiled at: 2019-07-03 18:58:20
# Size of source mod 2**32: 2134 bytes
from abc import ABC, abstractmethod

class ContinuousDistBase(ABC):
    __doc__ = 'Base abstract class for custom continuous distribution objects.\n    '

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def pdf(self, value):
        """Return the probability distribution function (pdf) at value.
        """
        pass

    @abstractmethod
    def logpdf(self, value):
        """Return the log of  the probability distribution function (pdf) at value.
        """
        pass

    @abstractmethod
    def cdf(self, value):
        """Return the cumulative distribution function (cdf) at value (integrated
        from the lower boundary of the distribution's support).
        """
        pass

    @abstractmethod
    def ppf(self, value):
        """Return the percent point function (ppf) (i.e., inverse of cdf) at value.
        Value is from [0:1].
        """
        pass

    @abstractmethod
    def rvs(self, shape):
        """Return a random variate sample (rvs) from the distribution with size
        given by shape.
        """
        pass


class DiscreteDistBase(ABC):
    __doc__ = 'Base abstract class for custom discrete distribution objects.\n    '

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def pmf(self, value):
        """Return the probability distribution function (pdf) at value.
        """
        pass

    @abstractmethod
    def logpmf(self, value):
        """Return the log of  the probability distribution function (pdf) at value.
        """
        pass

    @abstractmethod
    def cdf(self, value):
        """Return the cumulative distribution function (cdf) at value (integrated
        from the lower boundary of the distribution's support).
        """
        pass

    @abstractmethod
    def ppf(self, value):
        """Return the percent point function (ppf) (i.e., inverse of cdf) at value.
        Value is from [0:1].
        """
        pass

    @abstractmethod
    def rvs(self, shape):
        """Return a random variate sample (rvs) from the distribution with size
        given by shape.
        """
        pass