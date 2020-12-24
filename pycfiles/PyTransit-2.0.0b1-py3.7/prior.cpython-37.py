# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/pytransit/param/prior.py
# Compiled at: 2020-01-13 18:32:58
# Size of source mod 2**32: 3301 bytes
import math as m
from numpy import inf, zeros, pi, log, where, exp
from numpy.random import normal, uniform
import scipy.stats as gm

class Prior:

    def __init__(self):
        raise NotImplementedError

    def logpdf(self, v):
        raise NotImplementedError

    def rvs(self, size):
        raise NotImplementedError


class DefaultPrior(Prior):

    def logpdf(self, v: float):
        return 0

    def rvs(self, size):
        return zeros(size)


class NormalPrior(Prior):

    def __init__(self, mean: float, std: float):
        self.mean = float(mean)
        self.std = float(std)
        self._f1 = 1 / m.sqrt(2 * pi * std ** 2)
        self._lf1 = m.log(self._f1)
        self._f2 = 1 / (2 * std ** 2)

    def logpdf(self, x):
        return self._lf1 - self._f2 * (x - self.mean) ** 2

    def rvs(self, size=1):
        return normal(self.mean, self.std, size)

    def __str__(self):
        return f"N(μ = {self.mean}, σ = {self.std})"

    def __repr__(self):
        return f"NormalPrior({self.mean}, {self.std})"


class UniformPrior(Prior):

    def __init__(self, a: float, b: float):
        self.a, self.b = a, b
        self.lnc = m.log(b - a)

    def logpdf(self, v):
        return where((self.a < v) & (v < self.b), self.lnc, -inf)

    def rvs(self, size=1):
        return uniform(self.a, self.b, size)

    def __str__(self):
        return f"U(a = {self.a}, b = {self.b})"

    def __repr__(self):
        return f"UniformPrior({self.a}, {self.b})"


class JeffreysPrior(Prior):

    def __init__(self, x0: float, x1: float):
        self.x0 = x0
        self.x1 = x1
        self._f = log(x1 / x0)

    def pdf(self, x):
        return where((x > self.x0) & (x < self.x1), 1.0 / (x * self._f), -inf)

    def logpdf(self, x):
        return where((x > self.x0) & (x < self.x1), -log(x * self._f), -inf)

    def rvs(self, size=1):
        return exp(uniform(log(self.x0), log(self.x1), size))


class LogLogisticPrior(Prior):

    def __init__(self, a, b):
        self.a, self.b = a, b

    def logpdf(self, v):
        if not 0.001 < v < 1.0:
            return -inf
        a, b = self.a, self.b
        return m.log(b / a * (v / a) ** (b - 1.0) / (1.0 + (v / a) ** b) ** 2)

    def rvs(self, size=1):
        return uniform(0.001, 1.0, size)


class GammaPrior(Prior):

    def __init__(self, a):
        self.a = a
        self.A = -m.lgamma(a)

    def logpdf(self, x):
        return self.A + (self.a - 1.0) * log(x) - x

    def rvs(self, size):
        return gm(self.a).rvs(size)