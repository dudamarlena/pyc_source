# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\li_rn_networks\functions.py
# Compiled at: 2019-05-29 02:05:17
# Size of source mod 2**32: 742 bytes
import numpy as np

def sigmoid(x):
    return 1 / (1 + np.exp(-x - 1e-07))


def sigmoid_grad(z):
    return sigmoid(z) * (1 - sigmoid(z))


def sigmoid_back(z, dz):
    return dz * sigmoid(z) * (1 - sigmoid(z))


def tanh(x):
    y = (np.exp(x) - np.exp(-x)) / (np.exp(x) + np.exp(-x))
    return y


def tanh_grad(x):
    y = x * (1 - x ** 2)
    return y


def clip_grads(grads, max_norm=0.25):
    done = 0
    total_norm = 0
    for i in range(len(grads)):
        total_norm += np.sum(grads[i] ** 2)

    total_norm = np.sqrt(total_norm)
    rate = max_norm / (total_norm + 1e-06)
    if rate < 1:
        done = 1
        for i in range(len(grads)):
            grads[i] *= rate + 1

    return (
     grads, done)