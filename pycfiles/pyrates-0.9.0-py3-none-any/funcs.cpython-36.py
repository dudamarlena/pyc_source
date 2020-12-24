# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: E:\01_Work\15_PhD\11_Python_neural_mass_models\PyRates\pyrates\backend\funcs.py
# Compiled at: 2020-01-06 14:08:25
# Size of source mod 2**32: 2546 bytes
"""Contains functions that may be used as backend operations

"""
import numpy as np
from scipy.interpolate import interp1d
__author__ = 'Richard Gast'
__status__ = 'development'

def pr_sigmoid(x, scaling=1.0, steepness=1.0, offset=0.0):
    return scaling / (1.0 + np.exp(steepness * (offset - x)))


def pr_softmax(x, axis=0):
    x_exp = np.exp(x)
    return x_exp / np.sum(x_exp, axis=axis)


def pr_identity(x):
    return x


def pr_interp_1d_linear(x, y, x_new):
    return np.interp(x_new, x, y)


def pr_interp_nd_linear(x, y, x_new, y_idx, t):
    return np.asarray([np.interp(t - x_new_tmp, x, y[i, :]) for i, x_new_tmp in zip(y_idx, x_new)])


def pr_interp_1d(x, y, x_new):
    return interp1d(x, y, kind=3, axis=(-1))(x_new)


def pr_interp_nd(x, y, x_new, y_idx, t):
    try:
        f = interp1d(x, y, kind=3, axis=(-1), fill_value='extrapolate', copy=False)
    except ValueError:
        try:
            x, idx = np.unique(x, return_index=True)
            f = interp1d(x, (y[:, idx]), kind=3, axis=(-1), copy=False, fill_value='extrapolate')
        except ValueError:
            f = interp1d(x, (y[:, idx]), kind='linear', axis=(-1), copy=False, fill_value='extrapolate')

    return np.asarray([f(x_new_tmp)[i] for i, x_new_tmp in zip(y_idx, t - x_new)])


def pr_interp(f, x_new):
    return f(x_new)