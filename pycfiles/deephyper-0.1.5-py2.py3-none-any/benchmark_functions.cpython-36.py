# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/benchmark/benchmark_functions.py
# Compiled at: 2019-06-18 16:53:11
# Size of source mod 2**32: 13153 bytes
"""
Created by Dipendra Jha (dipendra@u.northwestern.edu) on 8/9/18
"""
from __future__ import division
import numpy as np
from numpy import abs, cos, exp, mean, pi, prod, sin, sqrt, sum
try:
    from opt.testfuncs.powellsincos import Powellsincos
except ImportError:
    Powellsincos = None

try:
    from opt.testfuncs.randomquad import randomquad
    from opt.testfuncs.logsumexp import logsumexp
except ImportError:
    randomquad = logsumexp = None

__version__ = '2015-03-06 mar  denis-bz-py t-online de'

def ackley(x, a=20, b=0.2, c=2 * pi):
    x = np.asarray_chkfinite(x)
    n = len(x)
    s1 = sum(x ** 2)
    s2 = sum(cos(c * x))
    return -a * exp(-b * sqrt(s1 / n)) - exp(s2 / n) + a + exp(1)


def dixonprice(x):
    x = np.asarray_chkfinite(x)
    n = len(x)
    j = np.arange(2, n + 1)
    x2 = 2 * x ** 2
    return sum(j * (x2[1:] - x[:-1]) ** 2) + (x[0] - 1) ** 2


def griewank(x, fr=4000):
    x = np.asarray_chkfinite(x)
    n = len(x)
    j = np.arange(1.0, n + 1)
    s = sum(x ** 2)
    p = prod(cos(x / sqrt(j)))
    return s / fr - p + 1


def levy(x):
    x = np.asarray_chkfinite(x)
    n = len(x)
    z = 1 + (x - 1) / 4
    return sin(pi * z[0]) ** 2 + sum((z[:-1] - 1) ** 2 * (1 + 10 * sin(pi * z[:-1] + 1) ** 2)) + (z[(-1)] - 1) ** 2 * (1 + sin(2 * pi * z[(-1)]) ** 2)


michalewicz_m = 0.5

def michalewicz(x):
    x = np.asarray_chkfinite(x)
    n = len(x)
    j = np.arange(1.0, n + 1)
    return -sum(sin(x) * sin(j * x ** 2 / pi) ** (2 * michalewicz_m))


def perm(x, b=0.5):
    x = np.asarray_chkfinite(x)
    n = len(x)
    j = np.arange(1.0, n + 1)
    xbyj = np.fabs(x) / j
    return mean([mean((j ** k + b) * (xbyj ** k - 1)) ** 2 for k in j / n])


def powell(x):
    x = np.asarray_chkfinite(x)
    n = len(x)
    n4 = (n + 3) // 4 * 4
    if n < n4:
        x = np.append(x, np.zeros(n4 - n))
    x = x.reshape((4, -1))
    f = np.empty_like(x)
    f[0] = x[0] + 10 * x[1]
    f[1] = sqrt(5) * (x[2] - x[3])
    f[2] = (x[1] - 2 * x[2]) ** 2
    f[3] = sqrt(10) * (x[0] - x[3]) ** 2
    return sum(f ** 2)


def powersum(x, b=[
 8, 18, 44, 114]):
    x = np.asarray_chkfinite(x)
    n = len(x)
    s = 0
    for k in range(1, n + 1):
        bk = b[min(k - 1, len(b) - 1)]
        s += (sum(x ** k) - bk) ** 2

    return s


def rastrigin(x):
    x = np.asarray_chkfinite(x)
    n = len(x)
    return 10 * n + sum(x ** 2 - 10 * cos(2 * pi * x))


def roscenbrock(x):
    """ http://en.wikipedia.org/wiki/Rosenbrock_function """
    x = np.asarray_chkfinite(x)
    x0 = x[:-1]
    x1 = x[1:]
    return sum((1 - x0) ** 2) + 100 * sum((x1 - x0 ** 2) ** 2)


def schwefel(x):
    x = np.asarray_chkfinite(x)
    n = len(x)
    return 418.9829 * n - sum(x * sin(sqrt(abs(x))))


def sphere(x):
    x = np.asarray_chkfinite(x)
    return sum(x ** 2)


def sum2(x):
    x = np.asarray_chkfinite(x)
    n = len(x)
    j = np.arange(1.0, n + 1)
    return sum(j * x ** 2)


def trid(x):
    x = np.asarray_chkfinite(x)
    return sum((x - 1) ** 2) - sum(x[:-1] * x[1:])


def zakharov(x):
    x = np.asarray_chkfinite(x)
    n = len(x)
    j = np.arange(1.0, n + 1)
    s2 = sum(j * x) / 2
    return sum(x ** 2) + s2 ** 2 + s2 ** 4


def ellipse(x):
    x = np.asarray_chkfinite(x)
    return mean((1 - x) ** 2) + 100 * mean(np.diff(x) ** 2)


def nesterov(x):
    """ Nesterov's nonsmooth Chebyshev-Rosenbrock function, Overton 2011 variant 2 """
    x = np.asarray_chkfinite(x)
    x0 = x[:-1]
    x1 = x[1:]
    return abs(1 - x[0]) / 4 + sum(abs(x1 - 2 * abs(x0) + 1))


def saddle(x):
    x = np.asarray_chkfinite(x) - 1
    return np.mean(np.diff(x ** 2)) + 0.5 * np.mean(x ** 4)


allfuncs = [
 ackley,
 dixonprice,
 ellipse,
 griewank,
 levy,
 michalewicz,
 nesterov,
 perm,
 powell,
 powersum,
 rastrigin,
 roscenbrock,
 schwefel,
 sphere,
 saddle,
 sum2,
 trid,
 zakharov]
if Powellsincos is not None:
    _powellsincos = {}

    def powellsincos(x):
        x = np.asarray_chkfinite(x)
        n = len(x)
        if n not in _powellsincos:
            _powellsincos[n] = Powellsincos(dim=n)
        return _powellsincos[n](x)


    allfuncs.append(powellsincos)
if randomquad is not None:
    allfuncs.append(randomquad)
    allfuncs.append(logsumexp)
allfuncs.sort(key=(lambda f: f.__name__))