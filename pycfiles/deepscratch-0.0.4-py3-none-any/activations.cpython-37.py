# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tuguldur/Documents/ml from scratch/build/lib/deepscratch/activations.py
# Compiled at: 2019-06-14 03:32:21
# Size of source mod 2**32: 270 bytes
import numpy as np

def relu(x, deriv=False):
    if not deriv:
        return np.where(x >= 0, x, 0)
    return np.where(x >= 0, x, 0)


def sigmoid(x, deriv=False):
    sigm = 1.0 / (1.0 + np.exp(-x))
    if not deriv:
        return sigm
    return sigm * (1.0 - sigm)