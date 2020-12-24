# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\xl_tensorflow\layers\layer.py
# Compiled at: 2020-03-20 09:15:57
# Size of source mod 2**32: 6655 bytes
import tensorflow as tf, functools
from tensorflow.keras import layers, Input, Model, backend
from tensorflow.python.keras.utils import tf_utils

def get_swish(**kwargs):

    def swish(x):
        """Swish activation function: x * sigmoid(x).
        Reference: [Searching for Activation Functions](https://arxiv.org/abs/1710.05941)
        """
        return tf.nn.swish(x)

    return swish


def get_relu6():

    def swish(x):
        """Swish activation function: x * sigmoid(x).
        Reference: [Searching for Activation Functions](https://arxiv.org/abs/1710.05941)
        """
        return tf.nn.relu6(x)

    return swish


CONV_KERNEL_INITIALIZER = {'class_name':'VarianceScaling', 
 'config':{'scale':2.0, 
  'mode':'fan_out', 
  'distribution':'normal'}}
DENSE_KERNEL_INITIALIZER = {'class_name':'VarianceScaling', 
 'config':{'scale':0.3333333333333333, 
  'mode':'fan_out', 
  'distribution':'uniform'}}

class GlobalAveragePooling2DKeepDim(layers.GlobalAveragePooling2D):
    __doc__ = 'Global average pooling operation for spatial data, this class keep dim for output\n\n    Arguments:\n        data_format: A string,\n          one of `channels_last` (default) or `channels_first`.\n          The ordering of the dimensions in the inputs.\n          `channels_last` corresponds to inputs with shape\n          `(batch, height, width, channels)` while `channels_first`\n          corresponds to inputs with shape\n          `(batch, channels, height, width)`.\n          It defaults to the `image_data_format` value found in your\n          Keras config file at `~/.keras/keras.json`.\n          If you never set it, then it will be "channels_last".\n\n    Input shape:\n      - If `data_format=\'channels_last\'`:\n        4D tensor with shape `(batch_size, rows, cols, channels)`.\n      - If `data_format=\'channels_first\'`:\n        4D tensor with shape `(batch_size, channels, rows, cols)`.\n\n    Output shape:\n      4D tensor with shape `(batch_size,1,1, channels)`.\n    '

    def __init__(self, **kwargs):
        (super(GlobalAveragePooling2DKeepDim, self).__init__)(**kwargs)

    def call(self, inputs):
        if self.data_format == 'channels_last':
            return backend.mean(inputs, axis=[1, 2], keepdims=True)
        return backend.mean(inputs, axis=[2, 3], keepdims=True)

    def get_config(self):
        config = super(GlobalAveragePooling2DKeepDim, self).get_config()
        return config


class SEConvEfnet2D(layers.Layer):
    __doc__ = '\n    This  Squeeze and Excitation layer for efficientnet\n    Args:\n        input_channels: 输入通道数\n        se_ratio: squeeze ratio\n    '

    def __init__(self, input_channels, se_ratio, name='SEConvEfnet2D', **kwargs):
        (super(SEConvEfnet2D, self).__init__)(name=name, **kwargs)
        num_reduced_filters = max(1, int(input_channels * se_ratio))
        self.se_ratio = se_ratio
        self.global_pooling = GlobalAveragePooling2DKeepDim()
        self.conv_kernel_initializer = {'class_name':'VarianceScaling', 
         'config':{'scale':2.0, 
          'mode':'fan_out', 
          'distribution':'normal'}}
        self._se_reduce = layers.Conv2D(num_reduced_filters, 1, strides=[1, 1], kernel_initializer=(self.conv_kernel_initializer),
          activation=None,
          padding='same',
          use_bias=True)
        self.activation = layers.ReLU()
        self._se_expand = layers.Conv2D(input_channels, 1, strides=[1, 1], kernel_initializer=(self.conv_kernel_initializer),
          activation='hard_sigmoid',
          padding='same',
          use_bias=True)
        self._multiply = layers.Multiply()

    def call(self, inputs, **kwargs):
        se_tensor = self.global_pooling(inputs)
        se_tensor = self._se_expand(self.activation(self._se_reduce(se_tensor)))
        x = self._multiply([se_tensor, inputs])
        return x

    def get_config(self):
        config = super(SEConvEfnet2D, self).get_config()
        config.update({'se_ratio': self.se_ratio})
        return config


class Swish(layers.Layer):

    def __init__(self, **kwargs):
        (super(Swish, self).__init__)(**kwargs)

    def call(self, inputs, **kwargs):
        return tf.multiply(backend.sigmoid(inputs), inputs)

    def get_config(self):
        base_config = super(Swish, self).get_config()
        return base_config

    @tf_utils.shape_type_conversion
    def compute_output_shape(self, input_shape):
        return input_shape


class HSwish(layers.Layer):

    def __init__(self, **kwargs):
        (super(HSwish, self).__init__)(**kwargs)

    def call(self, inputs, **kwargs):
        return tf.multiply(backend.sigmoid(inputs), tf.nn.relu6(inputs + 3) / 6)

    def get_config(self):
        base_config = super(HSwish, self).get_config()
        return base_config

    @tf_utils.shape_type_conversion
    def compute_output_shape(self, input_shape):
        return input_shape


def main():
    inputs = Input(shape=(224, 224, 3))
    x = layers.Conv2D(32, 3)(inputs)
    x = SEConvEfnet2D(32, 0.25)(x)
    x = Swish()(x)
    model = Model(inputs, x)
    print(model.summary())
    model.save('../1.h5')


if __name__ == '__main__':
    main()