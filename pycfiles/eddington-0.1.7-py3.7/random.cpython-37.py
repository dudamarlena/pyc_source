# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/eddington/input/random.py
# Compiled at: 2020-04-04 13:10:47
# Size of source mod 2**32: 1281 bytes
from eddington.consts import DEFAULT_XMIN, DEFAULT_XMAX, DEFAULT_MEASUREMENTS, DEFAULT_XSIGMA, DEFAULT_YSIGMA, DEFAULT_MIN_COEFF, DEFAULT_MAX_COEFF
import numpy as np
from collections import OrderedDict

def random_data(func, actual_a=None, xmin=DEFAULT_XMIN, xmax=DEFAULT_XMAX, measurements=DEFAULT_MEASUREMENTS, xsigma=DEFAULT_XSIGMA, ysigma=DEFAULT_YSIGMA, min_coeff=DEFAULT_MIN_COEFF, max_coeff=DEFAULT_MAX_COEFF):
    a = get_actual_a(func=func,
      actual_a=actual_a,
      min_coeff=min_coeff,
      max_coeff=max_coeff)
    x = np.random.uniform(xmin, xmax, size=measurements)
    xerr = np.random.exponential(scale=xsigma, size=measurements)
    yerr = np.random.exponential(scale=ysigma, size=measurements)
    y = func(a, x + np.random.normal(scale=xerr)) + np.random.normal(scale=yerr)
    return OrderedDict([('x', x), ('xerr', xerr), ('y', y), ('yerr', yerr)])


def get_actual_a(func, actual_a, min_coeff, max_coeff):
    if actual_a is not None:
        return actual_a
    return random_parameters((func.n), min_coeff=min_coeff, max_coeff=max_coeff)


def random_parameters(n, min_coeff=DEFAULT_MIN_COEFF, max_coeff=DEFAULT_MAX_COEFF):
    return np.random.uniform(min_coeff, max_coeff, size=n)