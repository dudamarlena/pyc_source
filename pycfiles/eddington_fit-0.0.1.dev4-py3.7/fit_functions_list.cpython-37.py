# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/eddington_fit/fit_functions_list.py
# Compiled at: 2020-04-24 11:38:34
# Size of source mod 2**32: 2304 bytes
import numpy as np
from eddington_core import fit_function

@fit_function(n=2,
  syntax='a[0] + a[1] * x',
  x_derivative=(lambda a, x: np.full(shape=(x.shape), fill_value=(a[1]))),
  a_derivative=(lambda a, x: np.stack((np.ones(shape=(x.shape)), x))))
def linear(a, x):
    return a[0] + a[1] * x


@fit_function(n=1,
  syntax='a[0]',
  x_derivative=(lambda a, x: np.zeros(shape=(x.shape))),
  a_derivative=(lambda a, x: np.ones(shape=(x.shape))))
def constant(a, x):
    return np.full(fill_value=(a[0]), shape=(x.shape))


@fit_function(n=3,
  syntax='a[0] + a[1] * x + a[2] * x ^ 2',
  x_derivative=(lambda a, x: a[1] + 2 * a[2] * x),
  a_derivative=(lambda a, x: np.stack([np.ones(shape=(x.shape)), x, x ** 2])))
def parabolic(a, x):
    return a[0] + a[1] * x + a[2] * x ** 2


@fit_function(n=3,
  syntax='a[0] / (x + a[1]) + a[2]',
  x_derivative=(lambda a, x: -a[0] / (x + a[1]) ** 2),
  a_derivative=(lambda a, x: np.stack([
 1 / (x + a[1]), -a[0] / (x + a[1]) ** 2, np.ones(shape=(x.shape))])))
def hyperbolic(a, x):
    return a[0] / (x + a[1]) + a[2]


@fit_function(n=3,
  syntax='a[0] * exp(a[1] * x) + a[2]',
  x_derivative=(lambda a, x: a[0] * a[1] * np.exp(a[1] * x)),
  a_derivative=(lambda a, x: np.stack([
 np.exp(a[1] * x), a[0] * x * np.exp(a[1] * x), np.ones(x.shape)])))
def exponential(a, x):
    return a[0] * np.exp(a[1] * x) + a[2]


@fit_function(n=4,
  syntax='a[0] * cos(a[1] * x + a[2]) + a[3]',
  x_derivative=(lambda a, x: -a[0] * a[1] * np.sin(a[1] * x + a[2])),
  a_derivative=(lambda a, x: np.stack([
 np.cos(a[1] * x + a[2]),
 -a[0] * x * np.sin(a[1] * x + a[2]),
 -a[0] * np.sin(a[1] * x + a[2]),
 np.ones(shape=(x.shape))])))
def cos(a, x):
    return a[0] * np.cos(a[1] * x + a[2]) + a[3]


@fit_function(n=4,
  syntax='a[0] * sin(a[1] * x + a[2]) + a[3]',
  x_derivative=(lambda a, x: a[0] * a[1] * np.cos(a[1] * x + a[2])),
  a_derivative=(lambda a, x: np.stack([
 np.sin(a[1] * x + a[2]),
 a[0] * x * np.cos(a[1] * x + a[2]),
 a[0] * np.cos(a[1] * x + a[2]),
 np.ones(shape=(x.shape))])))
def sin(a, x):
    return a[0] * np.sin(a[1] * x + a[2]) + a[3]