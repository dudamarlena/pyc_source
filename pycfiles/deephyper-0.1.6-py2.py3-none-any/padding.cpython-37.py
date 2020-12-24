# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/model/space/layers/padding.py
# Compiled at: 2019-09-05 10:20:47
# Size of source mod 2**32: 1683 bytes
import tensorflow as tf
from tensorflow import keras

class Padding(keras.layers.Layer):
    __doc__ = "Multi-dimensions padding layer.\n\n    This operation pads a tensor according to the paddings you specify. paddings is an integer tensor with shape [n-1, 2], where n is the rank of tensor. For each dimension D of input, paddings[D, 0] indicates how many values to add before the contents of tensor in that dimension, and paddings[D, 1] indicates how many values to add after the contents of tensor in that dimension. The first dimension corresponding to the batch size cannot be padded.\n\n    Args:\n        padding (list(list(int))): e.g. [[1, 1]]\n        mode (str): 'CONSTANT', 'REFLECT' or 'SYMMETRIC'\n    "

    def __init__(self, padding, mode='CONSTANT', constant_values=0, **kwargs):
        (super(Padding, self).__init__)(**kwargs)
        self.padding = [[0, 0]] + padding
        self.mode = mode
        self.constant_values = constant_values

    def call(self, x, mask=None):
        padding = tf.constant(self.padding)
        return tf.pad(tensor=x,
          paddings=padding,
          mode=(self.mode),
          constant_values=(self.constant_values))

    def compute_output_shape(self, input_shape):
        return tf.TensorShape([input_shape[i] + sum(self.padding[i]) if input_shape[i] is not None else None for i in range(len(input_shape))])

    def get_config(self):
        config = {'padding':self.padding[1:], 
         'mode':self.mode, 
         'constant_values':self.constant_values}
        base_config = super(Padding, self).get_config()
        return dict(list(base_config.items()) + list(config.items()))