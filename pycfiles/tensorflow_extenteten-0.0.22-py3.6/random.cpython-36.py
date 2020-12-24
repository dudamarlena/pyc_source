# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extenteten/random.py
# Compiled at: 2017-05-19 10:24:15
# Size of source mod 2**32: 289 bytes
import tensorflow as tf
from .assertion import is_natural_num
from .util import func_scope, static_shape
__all__ = [
 'sample_crop']

@func_scope()
def sample_crop(xs, n):
    return tf.random_crop(xs, tf.concat([[tf.minimum(n, tf.shape(xs)[0])], tf.shape(xs)[1:]], 0))