# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cjld/new_jittor/jittor/python/jittor/init.py
# Compiled at: 2020-03-20 04:44:53
# Size of source mod 2**32: 1956 bytes
import jittor as jt, numpy as np, math

def constant(shape, dtype, value=0.0):
    return jt.array(np.ones(shape) * value).unary(dtype)


def constant_(var, value=0.0):
    var.assign(constant(tuple(var.shape), var.dtype, value))


def uniform(shape, dtype, low, high):
    return jt.array(np.random.uniform(low, high, shape)).unary(dtype)


def uniform_(var, low, high):
    var.assign(uniform(tuple(var.shape), var.dtype, low, high))


def gauss(shape, dtype, mean=0.0, std=1.0):
    return jt.array(np.random.normal(mean, std, shape)).unary(dtype)


def gauss_(var, mean=0.0, std=1.0):
    var.assign(gauss(tuple(var.shape), var.dtype, mean, std))


def invariant_uniform(shape, dtype, mode='fan_in'):
    assert len(shape) > 1
    if not mode == 'fan_in':
        assert mode == 'fan_out'
    matsize = 1
    for i in shape[2:]:
        matsize *= i

    fan = shape[1] * matsize if mode == 'fan_in' else shape[0] * matsize
    bound = math.sqrt(1.0 / fan)
    return uniform(shape, dtype, -bound, bound)


def invariant_uniform_(var, mode='fan_in'):
    var.assign(invariant_uniform(tuple(var.shape), var.dtype, mode))


def relu_invariant_gauss(shape, dtype, mode='fan_in'):
    assert len(shape) > 1
    if not mode == 'fan_in':
        assert mode == 'fan_out'
    matsize = 1
    for i in shape[2:]:
        matsize *= i

    fan = shape[1] * matsize if mode == 'fan_in' else shape[0] * matsize
    std = math.sqrt(2.0 / fan)
    return gauss(shape, dtype, 0, std)


def relu_invariant_gauss_(var, mode='fan_in'):
    var.assign(relu_invariant_gauss(tuple(var.shape), var.dtype, mode))