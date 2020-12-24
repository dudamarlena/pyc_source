# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\odddML\custom_layers.py
# Compiled at: 2019-12-19 16:13:08
# Size of source mod 2**32: 3070 bytes
from tensorflow.keras import backend
from tensorflow.keras import layers
from tensorflow.keras import regularizers
from tensorflow.keras.layers import Conv2D, Multiply, Activation
from tensorflow.keras.initializers import glorot_uniform
import tensorflow as tf, numpy as np, cv2, os

class GatedConv2D(Conv2D):
    __doc__ = 'Gated Convolutional Class'

    def __init__(self, **kwargs):
        (super(GatedConv2D, self).__init__)(**kwargs)

    def call(self, inputs):
        output = super(GatedConv2D, self).call(inputs)
        linear = Activation('linear')(inputs)
        sigmoid = Activation('sigmoid')(output)
        return Multiply()([linear, sigmoid])

    def get_config(self):
        config = super(GatedConv2D, self).get_config()
        return config


class FullGatedConv2D(Conv2D):
    __doc__ = 'Gated Convolutional Class'

    def __init__(self, filters, **kwargs):
        (super(FullGatedConv2D, self).__init__)(filters=filters * 2, **kwargs)
        self.nb_filters = filters

    def call(self, inputs):
        output = super(FullGatedConv2D, self).call(inputs)
        linear = Activation('linear')(output[:, :, :, :self.nb_filters])
        sigmoid = Activation('sigmoid')(output[:, :, :, self.nb_filters:])
        return Multiply()([linear, sigmoid])

    def compute_output_shape(self, input_shape):
        output_shape = super(FullGatedConv2D, self).compute_output_shape(input_shape)
        return tuple(output_shape[:3]) + (self.nb_filters,)

    def get_config(self):
        config = super(FullGatedConv2D, self).get_config()
        config['nb_filters'] = self.nb_filters
        del config['filters']
        return config


if __name__ == '__main__':
    pass