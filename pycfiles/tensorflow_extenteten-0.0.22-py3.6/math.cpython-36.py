# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extenteten/math.py
# Compiled at: 2017-01-06 05:01:09
# Size of source mod 2**32: 455 bytes
import tensorflow as tf
from .util import func_scope, static_rank, dtype_epsilon
__all__ = [
 'scalar_to_vec', 'vec_to_mat', 'softmax_inverse']

@func_scope()
def scalar_to_vec(scalar):
    assert static_rank(scalar) == 1
    return tf.expand_dims(scalar, [1])


@func_scope()
def vec_to_mat(vec):
    assert static_rank(vec) == 2
    return tf.expand_dims(vec, [2])


@func_scope()
def softmax_inverse(x):
    return tf.log(x + dtype_epsilon(x.dtype))