# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extenteten/mask.py
# Compiled at: 2017-01-06 05:01:09
# Size of source mod 2**32: 847 bytes
import tensorflow as tf
from .util import static_rank, func_scope, dimension_indices
__all__ = [
 'max_mask', 'mean_mask', 'range_mask']

@func_scope()
def max_mask(x, reduction_indices=None, dtype=None):
    assert static_rank(x) >= 2
    max = tf.reduce_max(x, (reduction_indices or dimension_indices(x, 1)),
      keep_dims=True)
    return tf.cast(tf.equal(x, max), dtype or x.dtype)


@func_scope()
def mean_mask(x, reduction_indices=None, dtype=None):
    assert static_rank(x) >= 2
    mean = tf.reduce_mean(x, (reduction_indices or dimension_indices(x, 1)),
      keep_dims=True)
    return tf.cast(x >= mean, dtype or x.dtype)


@func_scope()
def range_mask(x, first, last, dtype=None):
    return tf.cast((first <= x) & (x <= last), dtype or x.dtype)