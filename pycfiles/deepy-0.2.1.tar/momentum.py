# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/shu/research/deepy/deepy/trainers/cores/momentum.py
# Compiled at: 2016-04-20 00:05:45
import theano, numpy as np

def momentum_core(params, gradients, momentum=0.9, learning_rate=0.01):
    """
    Momentum SGD optimization core.
    """
    free_parameters = []
    updates = []
    for param, grad in zip(params, gradients):
        delta = learning_rate * grad
        velocity = theano.shared(np.zeros_like(param.get_value()), name=param.name + '_vel')
        updates.append((velocity, momentum * velocity - delta))
        updates.append((param, param + velocity))
        free_parameters.append(velocity)

    return (
     updates, free_parameters)