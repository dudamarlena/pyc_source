# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/shu/research/deepy/deepy/trainers/cores/adam.py
# Compiled at: 2016-04-20 00:05:45
import theano, theano.tensor as T, numpy as np

def adam_core(params, gradients, learning_rate=0.002, beta1=0.1, beta2=0.001, epsilon=1e-08, gamma=0.99999999):
    updates = []
    free_parameters = []
    i = theano.shared(np.float32(1), name='adam_i')
    free_parameters.append(i)
    i_t = i + 1.0
    fix1 = 1.0 - (1.0 - beta1) ** i_t
    fix2 = 1.0 - (1.0 - beta2) ** i_t
    beta1_t = 1 - (1 - beta1) * gamma ** (i_t - 1)
    learning_rate_t = learning_rate * (T.sqrt(fix2) / fix1)
    for param_i, g in zip(params, gradients):
        m = theano.shared(np.zeros(param_i.get_value().shape, dtype=theano.config.floatX), name='adam_m_%s' % param_i.name)
        v = theano.shared(np.zeros(param_i.get_value().shape, dtype=theano.config.floatX), name='adam_v_%s' % param_i.name)
        free_parameters.extend([m, v])
        m_t = beta1_t * g + (1.0 - beta1_t) * m
        v_t = beta2 * g ** 2 + (1.0 - beta2) * v
        g_t = m_t / (T.sqrt(v_t) + epsilon)
        param_i_t = param_i - learning_rate_t * g_t
        updates.append((m, m_t))
        updates.append((v, v_t))
        updates.append((param_i, param_i_t))

    updates.append((i, i_t))
    return (updates, free_parameters)