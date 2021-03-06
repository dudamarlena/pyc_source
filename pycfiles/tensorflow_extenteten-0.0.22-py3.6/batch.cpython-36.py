# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extenteten/batch.py
# Compiled at: 2017-05-19 06:10:34
# Size of source mod 2**32: 1255 bytes
import tensorflow as tf
from .util import func_scope, static_rank, dimension_indices
from .math import vec_to_mat
__all__ = [
 'dynamic_partition',
 'mat_vec_mul',
 'max',
 'min',
 'sum']

@func_scope()
def dynamic_partition(data, partitions, num_partitions, name=None):
    return tf.map_fn(lambda args: (tf.dynamic_partition)(args, *(num_partitions,), **{'name': name}), [
     data, partitions])


@func_scope()
def mat_vec_mul(matrix, vector):
    if not static_rank(matrix) == 3:
        raise AssertionError
    elif not static_rank(vector) == 2:
        raise AssertionError
    return tf.squeeze(tf.matmul(matrix, vec_to_mat(vector)), [2])


@func_scope()
def max(x, keep_dims=False, name=None):
    return tf.reduce_max(x, (dimension_indices(x, 1)),
      keep_dims=keep_dims,
      name=name)


@func_scope()
def min(x, keep_dims=False, name=None):
    return tf.reduce_min(x, (dimension_indices(x, 1)),
      keep_dims=keep_dims,
      name=name)


@func_scope()
def sum(x, keep_dims=False, name=None):
    return tf.reduce_sum(x, (dimension_indices(x, 1)),
      keep_dims=keep_dims,
      name=name)