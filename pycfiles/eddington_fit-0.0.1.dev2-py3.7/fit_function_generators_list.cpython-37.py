# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/eddington_fit/fit_function_generators_list.py
# Compiled at: 2020-04-20 10:00:06
# Size of source mod 2**32: 2294 bytes
import numpy as np
from eddington_core import InvalidGeneratorInitialization, fit_function, fit_function_generator
from eddington_fit.fit_functions_list import linear, parabolic, hyperbolic

@fit_function_generator(parameters='n', syntax='a[0] + a[1] * x + ... + a[n] * x ^ n')
def polynom(n):
    n = int(n)
    if n <= 0:
        raise InvalidGeneratorInitialization(f"n must be positive, got {n}")
    if n == 1:
        return linear
    if n == 2:
        return parabolic
    arange = np.arange(1, n + 1)

    @fit_function(n=(n + 1),
      name=f"polynom_{n}",
      x_derivative=(lambda a, x: polynom(n - 1)(arange * a[1:], x)),
      a_derivative=(lambda a, x: np.stack([x ** i for i in range(n + 1)])),
      save=False)
    def func(a, x):
        return sum([a[i] * x ** i for i in range(n + 1)])

    return func


@fit_function_generator(parameters='n', syntax='a[0] * (x + a[1]) ^ n + a[2]')
def straight_power(n):
    n = int(n)
    if n <= 0:
        raise InvalidGeneratorInitialization(f"n must be positive, got {n}")
    if n == 1:
        raise InvalidGeneratorInitialization('n cannot be 1. use "linear" fit instead.')

    @fit_function(n=3,
      name=f"straight_power_{n}",
      x_derivative=(lambda a, x: n * a[0] * (x + a[1]) ** (n - 1)),
      a_derivative=(lambda a, x: np.stack([
     (x + a[1]) ** n, n * a[0] * (x + a[1]) ** (n - 1), np.ones(shape=(x.shape))])),
      save=False)
    def func(a, x):
        return a[0] * (x + a[1]) ** n + a[2]

    return func


@fit_function_generator(parameters='n', syntax='a[0] / (x + a[1]) ^ n + a[2]')
def inverse_power(n):
    n = int(n)
    if n <= 0:
        raise InvalidGeneratorInitialization(f"n must be positive, got {n}")
    if n == 1:
        return hyperbolic

    @fit_function(n=3,
      name=f"inverse_power_{n}",
      x_derivative=(lambda a, x: -n * a[0] / (x + a[1]) ** (n + 1)),
      a_derivative=(lambda a, x: np.stack([
     1 / (x + a[1]) ** n,
     -n * a[0] / (x + a[1]) ** (n + 1),
     np.ones(shape=(x.shape))])),
      save=False)
    def func(a, x):
        return a[0] / (x + a[1]) ** n + a[2]

    return func