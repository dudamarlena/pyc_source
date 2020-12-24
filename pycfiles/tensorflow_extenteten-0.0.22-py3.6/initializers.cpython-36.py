# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extenteten/initializers.py
# Compiled at: 2017-01-06 05:01:09
# Size of source mod 2**32: 439 bytes
import numpy as np, tensorflow as tf
__all__ = [
 'identity_initializer']

def identity_initializer(dtype=tf.float32):

    def initializer(shape, dtype=dtype):
        if len(shape) == 1:
            return tf.zeros(shape, dtype)
        if len(shape) == 2:
            if shape[0] == shape[1]:
                return tf.constant(np.eye(shape[0]), dtype)
        raise ValueError('Invalid shape for identity_initializer.')

    return initializer