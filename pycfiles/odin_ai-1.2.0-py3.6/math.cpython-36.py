# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/odin/networks/math.py
# Compiled at: 2019-08-26 04:21:03
# Size of source mod 2**32: 1494 bytes
from __future__ import absolute_import, division, print_function
import inspect, tensorflow as tf
from tensorflow.python.keras.layers import Layer
from tensorflow_probability.python.distributions import Distribution
__all__ = [
 'Reduce']

class Reduce(Layer):
    __doc__ = ' ReduceMean '

    def __init__(self, op, axis=None, keepdims=None):
        op = callable(op) or str(op).lower()
        if op == 'mean':
            op = tf.reduce_mean
        else:
            if op == 'sum':
                op = tf.reduce_sum
            else:
                if op == 'prod':
                    op = tf.reduce_prod
                else:
                    if op == 'max':
                        op = tf.reduce_max
                    else:
                        if op == 'min':
                            op = tf.reduce_min
                        else:
                            if op == 'logsumexp':
                                op = tf.reduce_logsumexp
                            else:
                                if op == 'any':
                                    op = tf.reduce_any
                                else:
                                    if op == 'all':
                                        op = tf.reduce_all
                                    else:
                                        args = inspect.getfullargspec(op)
                                    assert 'axis' in args and 'keepdims' in args, "reduce function must has 2 arguments: 'axis' and 'keepdims'"
                                    super(Reduce, self).__init__(name=(op.__name__))
                                    self.op = op
                                    self.axis = axis
                                    self.keepdims = keepdims

    def get_config(self):
        config = super(Reduce, self).get_config()
        config['op'] = self.op
        config['axis'] = self.axis
        config['keepdims'] = self.keepdims
        return config

    def call(self, x):
        if isinstance(x, (tuple, list)):
            return [self.op(i, axis=(self.axis), keepdims=(self.keepdims)) for i in x]
        else:
            return self.op(x, axis=(self.axis), keepdims=(self.keepdims))