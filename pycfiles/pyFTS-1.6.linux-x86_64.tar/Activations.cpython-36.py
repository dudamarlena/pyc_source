# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyFTS/fcm/Activations.py
# Compiled at: 2019-04-26 12:54:52
# Size of source mod 2**32: 264 bytes
import numpy as np

def step(x):
    if x <= 0:
        return 0
    else:
        return 1


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def softmax(x):
    mvs = sum([np.exp(k) for k in x.flatten()])
    return np.array([np.exp(k) / mvs for k in x.flatten()])