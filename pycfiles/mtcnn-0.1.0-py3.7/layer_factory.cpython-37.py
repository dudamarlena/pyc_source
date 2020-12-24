# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mtcnn/layer_factory.py
# Compiled at: 2019-11-14 12:16:36
# Size of source mod 2**32: 9674 bytes
import tensorflow as tf
from distutils.version import LooseVersion
__author__ = 'Iván de Paz Centeno'

class LayerFactory(object):
    __doc__ = '\n    Allows to create stack layers for a given network.\n    '
    AVAILABLE_PADDINGS = ('SAME', 'VALID')

    def __init__(self, network):
        self._LayerFactory__network = network

    @staticmethod
    def __validate_padding(padding):
        if padding not in LayerFactory.AVAILABLE_PADDINGS:
            raise Exception('Padding {} not valid'.format(padding))

    @staticmethod
    def __validate_grouping(channels_input: int, channels_output: int, group: int):
        if channels_input % group != 0:
            raise Exception('The number of channels in the input does not match the group')
        if channels_output % group != 0:
            raise Exception('The number of channels in the output does not match the group')

    @staticmethod
    def vectorize_input(input_layer):
        input_shape = input_layer.get_shape()
        if input_shape.ndims == 4:
            dim = 1
            for x in input_shape[1:].as_list():
                dim *= int(x)

            vectorized_input = tf.reshape(input_layer, [-1, dim])
        else:
            vectorized_input, dim = input_layer, input_shape[(-1)]
        return (vectorized_input, dim)

    def __make_var(self, name: str, shape: list):
        """
        Creates a tensorflow variable with the given name and shape.
        :param name: name to set for the variable.
        :param shape: list defining the shape of the variable.
        :return: created TF variable.
        """
        return tf.compat.v1.get_variable(name, shape, trainable=(self._LayerFactory__network.is_trainable()), use_resource=False)

    def new_feed(self, name: str, layer_shape: tuple):
        """
        Creates a feed layer. This is usually the first layer in the network.
        :param name: name of the layer
        :return:
        """
        feed_data = tf.compat.v1.placeholder(tf.float32, layer_shape, 'input')
        self._LayerFactory__network.add_layer(name, layer_output=feed_data)

    def new_conv(self, name: str, kernel_size: tuple, channels_output: int, stride_size: tuple, padding: str='SAME', group: int=1, biased: bool=True, relu: bool=True, input_layer_name: str=None):
        """
        Creates a convolution layer for the network.
        :param name: name for the layer
        :param kernel_size: tuple containing the size of the kernel (Width, Height)
        :param channels_output: ¿? Perhaps number of channels in the output? it is used as the bias size.
        :param stride_size: tuple containing the size of the stride (Width, Height)
        :param padding: Type of padding. Available values are: ('SAME', 'VALID')
        :param group: groups for the kernel operation. More info required.
        :param biased: boolean flag to set if biased or not.
        :param relu: boolean flag to set if ReLu should be applied at the end of the layer or not.
        :param input_layer_name: name of the input layer for this layer. If None, it will take the last added layer of
        the network.
        """
        self._LayerFactory__validate_padding(padding)
        input_layer = self._LayerFactory__network.get_layer(input_layer_name)
        channels_input = int(input_layer.get_shape()[(-1)])
        self._LayerFactory__validate_grouping(channels_input, channels_output, group)
        convolve = lambda input_val, kernel: tf.nn.conv2d(input=input_val, filters=kernel,
          strides=[
         1, stride_size[1], stride_size[0], 1],
          padding=padding)
        with tf.compat.v1.variable_scope(name) as (scope):
            kernel = self._LayerFactory__make_var('weights', shape=[kernel_size[1], kernel_size[0], channels_input // group, channels_output])
            output = convolve(input_layer, kernel)
            if biased:
                biases = self._LayerFactory__make_var('biases', [channels_output])
                output = tf.nn.bias_add(output, biases)
            if relu:
                output = tf.nn.relu(output, name=(scope.name))
        self._LayerFactory__network.add_layer(name, layer_output=output)

    def new_prelu(self, name: str, input_layer_name: str=None):
        """
        Creates a new prelu layer with the given name and input.
        :param name: name for this layer.
        :param input_layer_name: name of the layer that serves as input for this one.
        """
        input_layer = self._LayerFactory__network.get_layer(input_layer_name)
        with tf.compat.v1.variable_scope(name):
            channels_input = int(input_layer.get_shape()[(-1)])
            alpha = self._LayerFactory__make_var('alpha', shape=[channels_input])
            output = tf.nn.relu(input_layer) + tf.multiply(alpha, -tf.nn.relu(-input_layer))
        self._LayerFactory__network.add_layer(name, layer_output=output)

    def new_max_pool(self, name: str, kernel_size: tuple, stride_size: tuple, padding='SAME', input_layer_name: str=None):
        """
        Creates a new max pooling layer.
        :param name: name for the layer.
        :param kernel_size: tuple containing the size of the kernel (Width, Height)
        :param stride_size: tuple containing the size of the stride (Width, Height)
        :param padding: Type of padding. Available values are: ('SAME', 'VALID')
        :param input_layer_name: name of the input layer for this layer. If None, it will take the last added layer of
        the network.
        """
        self._LayerFactory__validate_padding(padding)
        input_layer = self._LayerFactory__network.get_layer(input_layer_name)
        output = tf.nn.max_pool2d(input=input_layer, ksize=[
         1, kernel_size[1], kernel_size[0], 1],
          strides=[
         1, stride_size[1], stride_size[0], 1],
          padding=padding,
          name=name)
        self._LayerFactory__network.add_layer(name, layer_output=output)

    def new_fully_connected(self, name: str, output_count: int, relu=True, input_layer_name: str=None):
        """
        Creates a new fully connected layer.

        :param name: name for the layer.
        :param output_count: number of outputs of the fully connected layer.
        :param relu: boolean flag to set if ReLu should be applied at the end of this layer.
        :param input_layer_name: name of the input layer for this layer. If None, it will take the last added layer of
        the network.
        """
        with tf.compat.v1.variable_scope(name):
            input_layer = self._LayerFactory__network.get_layer(input_layer_name)
            vectorized_input, dimension = self.vectorize_input(input_layer)
            weights = self._LayerFactory__make_var('weights', shape=[dimension, output_count])
            biases = self._LayerFactory__make_var('biases', shape=[output_count])
            operation = tf.compat.v1.nn.relu_layer if relu else tf.compat.v1.nn.xw_plus_b
            fc = operation(vectorized_input, weights, biases, name=name)
        self._LayerFactory__network.add_layer(name, layer_output=fc)

    def new_softmax(self, name, axis, input_layer_name: str=None):
        """
        Creates a new softmax layer
        :param name: name to set for the layer
        :param axis:
        :param input_layer_name: name of the input layer for this layer. If None, it will take the last added layer of
        the network.
        """
        input_layer = self._LayerFactory__network.get_layer(input_layer_name)
        if LooseVersion(tf.__version__) < LooseVersion('1.5.0'):
            max_axis = tf.reduce_max(input_tensor=input_layer, axis=axis, keepdims=True)
            target_exp = tf.exp(input_layer - max_axis)
            normalize = tf.reduce_sum(input_tensor=target_exp, axis=axis, keepdims=True)
        else:
            max_axis = tf.reduce_max(input_tensor=input_layer, axis=axis, keepdims=True)
            target_exp = tf.exp(input_layer - max_axis)
            normalize = tf.reduce_sum(input_tensor=target_exp, axis=axis, keepdims=True)
        softmax = tf.math.divide(target_exp, normalize, name)
        self._LayerFactory__network.add_layer(name, layer_output=softmax)