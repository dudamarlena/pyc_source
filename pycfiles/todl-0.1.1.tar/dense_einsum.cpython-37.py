# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/svpino/dev/tensorflow-object-detection-sagemaker/todl/tensorflow-object-detection/official/nlp/modeling/layers/dense_einsum.py
# Compiled at: 2020-04-05 19:50:57
# Size of source mod 2**32: 7079 bytes
"""Keras-based einsum layer."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import tensorflow as tf
_CHR_IDX = [
 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm']

@tf.keras.utils.register_keras_serializable(package='Text')
class DenseEinsum(tf.keras.layers.Layer):
    __doc__ = 'A densely connected layer that uses tf.einsum as the backing computation.\n\n  This layer can perform einsum calculations of arbitrary dimensionality.\n\n  Arguments:\n    output_shape: Positive integer or tuple, dimensionality of the output space.\n    num_summed_dimensions: The number of dimensions to sum over. Standard 2D\n      matmul should use 1, 3D matmul should use 2, and so forth.\n    activation: Activation function to use. If you don\'t specify anything, no\n      activation is applied\n      (ie. "linear" activation: `a(x) = x`).\n    use_bias: Boolean, whether the layer uses a bias vector.\n    kernel_initializer: Initializer for the `kernel` weights matrix.\n    bias_initializer: Initializer for the bias vector.\n    kernel_regularizer: Regularizer function applied to the `kernel` weights\n      matrix.\n    bias_regularizer: Regularizer function applied to the bias vector.\n    activity_regularizer: Regularizer function applied to the output of the\n      layer (its "activation")..\n    kernel_constraint: Constraint function applied to the `kernel` weights\n      matrix.\n    bias_constraint: Constraint function applied to the bias vector.\n  Input shape:\n    N-D tensor with shape: `(batch_size, ..., input_dim)`. The most common\n      situation would be a 2D input with shape `(batch_size, input_dim)`.\n  Output shape:\n    N-D tensor with shape: `(batch_size, ..., units)`. For instance, for a 2D\n      input with shape `(batch_size, input_dim)`, the output would have shape\n      `(batch_size, units)`.\n  '

    def __init__(self, output_shape, num_summed_dimensions=1, activation=None, use_bias=True, kernel_initializer='glorot_uniform', bias_initializer='zeros', kernel_regularizer=None, bias_regularizer=None, activity_regularizer=None, kernel_constraint=None, bias_constraint=None, **kwargs):
        (super(DenseEinsum, self).__init__)(**kwargs)
        self._output_shape = output_shape if isinstance(output_shape, (list, tuple)) else (output_shape,)
        self._activation = tf.keras.activations.get(activation)
        self._use_bias = use_bias
        self._kernel_initializer = tf.keras.initializers.get(kernel_initializer)
        self._bias_initializer = tf.keras.initializers.get(bias_initializer)
        self._kernel_regularizer = tf.keras.regularizers.get(kernel_regularizer)
        self._bias_regularizer = tf.keras.regularizers.get(bias_regularizer)
        self._kernel_constraint = tf.keras.constraints.get(kernel_constraint)
        self._bias_constraint = tf.keras.constraints.get(bias_constraint)
        self._num_summed_dimensions = num_summed_dimensions
        self._einsum_string = None

    def _build_einsum_string(self, free_input_dims, bound_dims, output_dims):
        input_str = ''
        kernel_str = ''
        output_str = ''
        letter_offset = 0
        for i in range(free_input_dims):
            char = _CHR_IDX[(i + letter_offset)]
            input_str += char
            output_str += char

        letter_offset += free_input_dims
        for i in range(bound_dims):
            char = _CHR_IDX[(i + letter_offset)]
            input_str += char
            kernel_str += char

        letter_offset += bound_dims
        for i in range(output_dims):
            char = _CHR_IDX[(i + letter_offset)]
            kernel_str += char
            output_str += char

        return input_str + ',' + kernel_str + '->' + output_str

    def build(self, input_shape):
        input_shape = tf.TensorShape(input_shape)
        input_rank = input_shape.rank
        free_input_dims = input_rank - self._num_summed_dimensions
        output_dims = len(self._output_shape)
        self._einsum_string = self._build_einsum_string(free_input_dims, self._num_summed_dimensions, output_dims)
        self._kernel_shape = input_shape[free_input_dims:].concatenate(self._output_shape)
        self._kernel = self.add_weight('kernel',
          shape=(self._kernel_shape),
          initializer=(self._kernel_initializer),
          regularizer=(self._kernel_regularizer),
          constraint=(self._kernel_constraint),
          dtype=(self.dtype),
          trainable=True)
        if self._use_bias:
            self._bias = self.add_weight('bias',
              shape=(self._output_shape),
              initializer=(self._bias_initializer),
              regularizer=(self._bias_regularizer),
              constraint=(self._bias_constraint),
              dtype=(self.dtype),
              trainable=True)
        else:
            self._bias = None
        super(DenseEinsum, self).build(input_shape)

    def get_config(self):
        config = {'output_shape':self._output_shape, 
         'activation':tf.keras.activations.serialize(self._activation), 
         'use_bias':self._use_bias, 
         'kernel_initializer':tf.keras.initializers.serialize(self._kernel_initializer), 
         'bias_initializer':tf.keras.initializers.serialize(self._bias_initializer), 
         'kernel_regularizer':tf.keras.regularizers.serialize(self._kernel_regularizer), 
         'bias_regularizer':tf.keras.regularizers.serialize(self._bias_regularizer), 
         'activity_regularizer':tf.keras.regularizers.serialize(self._activity_regularizer), 
         'kernel_constraint':tf.keras.constraints.serialize(self._kernel_constraint), 
         'bias_constraint':tf.keras.constraints.serialize(self._bias_constraint)}
        base_config = super(DenseEinsum, self).get_config()
        return dict(list(base_config.items()) + list(config.items()))

    def call(self, inputs):
        ret = tf.einsum(self._einsum_string, inputs, self._kernel)
        if self._use_bias:
            ret += self._bias
        if self._activation is not None:
            ret = self._activation(ret)
        return ret