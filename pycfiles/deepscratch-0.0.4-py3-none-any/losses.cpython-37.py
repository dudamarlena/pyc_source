# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tuguldur/Documents/ml from scratch/build/lib/deepscratch/losses.py
# Compiled at: 2019-06-14 03:37:54
# Size of source mod 2**32: 320 bytes
import numpy as np

class Loss:

    def __init__(self, value=None, grad=None):
        self.value = value
        self.grad = grad


def mse_loss(y_true, y_pred):
    loss = np.mean(0.5 * np.power(y_true - y_pred, 2))
    grad = -(y_true - y_pred)
    return Loss(loss, grad)