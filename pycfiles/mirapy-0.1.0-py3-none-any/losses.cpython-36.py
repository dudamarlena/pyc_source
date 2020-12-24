# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/swapsha96/mtp/MiraPy/build/lib/mirapy/fitting/losses.py
# Compiled at: 2019-05-03 11:14:15
# Size of source mod 2**32: 265 bytes
import autograd.numpy as np
from autograd.scipy.stats import norm

def negative_log_likelihood(y_true, y_pred):
    ll = norm.logpdf(y_true, y_pred)
    return -np.sum(ll)


def mean_squared_error(y_true, y_pred):
    return np.sum((y_true - y_pred) ** 2) / len(y_true)