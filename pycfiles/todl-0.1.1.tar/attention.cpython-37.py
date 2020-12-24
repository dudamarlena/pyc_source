# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/svpino/dev/tensorflow-object-detection-sagemaker/todl/tensorflow-object-detection/official/nlp/modeling/layers/attention.py
# Compiled at: 2020-04-05 19:50:57
# Size of source mod 2**32: 10924 bytes
"""Keras-based attention layer."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import math, tensorflow as tf
from official.nlp.modeling.layers import dense_einsum
from official.nlp.modeling.layers import masked_softmax

@tf.keras.utils.register_keras_serializable(package='Text')
class MultiHeadAttention(tf.keras.layers.Layer):
    __doc__ = 'MultiHeadAttention layer.\n\n  This is an implementation of multi-headed attention based on "Attention\n  is all you Need". If `from_tensor` and `to_tensor` are the same, then\n  this is self-attention. Each timestep in `from_tensor` attends to the\n  corresponding sequence in `to_tensor`, and returns a fixed-width vector.\n\n  This function first projects `from_tensor` into a "query" tensor and\n  `to_tensor` into "key" and "value" tensors. These are (effectively) a list\n  of tensors of length `num_attention_heads`, where each tensor is of shape\n  [batch_size, seq_length, size_per_head].\n\n  Then, the query and key tensors are dot-producted and scaled. These are\n  softmaxed to obtain attention probabilities. The value tensors are then\n  interpolated by these probabilities, then concatenated back to a single\n  tensor and returned.\n\n  Arguments:\n    num_heads: Number of attention heads.\n    head_size: Size of each attention head.\n    dropout: Dropout probability.\n    kernel_initializer: Initializer for dense layer kernels.\n    bias_initializer: Initializer for dense layer biases.\n    kernel_regularizer: Regularizer for dense layer kernels.\n    bias_regularizer: Regularizer for dense layer biases.\n    activity_regularizer: Regularizer for dense layer activity.\n    kernel_constraint: Constraint for dense layer kernels.\n    bias_constraint: Constraint for dense layer kernels.\n  '

    def __init__(self, num_heads, head_size, dropout_rate=0.0, kernel_initializer='glorot_uniform', bias_initializer='zeros', kernel_regularizer=None, bias_regularizer=None, activity_regularizer=None, kernel_constraint=None, bias_constraint=None, **kwargs):
        (super(MultiHeadAttention, self).__init__)(**kwargs)
        self._num_heads = num_heads
        self._head_size = head_size
        self._dropout_rate = dropout_rate
        self._kernel_initializer = tf.keras.initializers.get(kernel_initializer)
        self._bias_initializer = tf.keras.initializers.get(bias_initializer)
        self._kernel_regularizer = tf.keras.regularizers.get(kernel_regularizer)
        self._bias_regularizer = tf.keras.regularizers.get(bias_regularizer)
        self._kernel_constraint = tf.keras.constraints.get(kernel_constraint)
        self._bias_constraint = tf.keras.constraints.get(bias_constraint)
        self._query_dense = dense_einsum.DenseEinsum(output_shape=(
         self._num_heads, self._head_size),
          kernel_initializer=(self._kernel_initializer),
          bias_initializer=(self._bias_initializer),
          kernel_regularizer=(self._kernel_regularizer),
          bias_regularizer=(self._bias_regularizer),
          activity_regularizer=(self._activity_regularizer),
          kernel_constraint=(self._kernel_constraint),
          bias_constraint=(self._bias_constraint),
          name='query')
        self._key_dense = dense_einsum.DenseEinsum(output_shape=(
         self._num_heads, self._head_size),
          kernel_initializer=(self._kernel_initializer),
          bias_initializer=(self._bias_initializer),
          kernel_regularizer=(self._kernel_regularizer),
          bias_regularizer=(self._bias_regularizer),
          activity_regularizer=(self._activity_regularizer),
          kernel_constraint=(self._kernel_constraint),
          bias_constraint=(self._bias_constraint),
          name='key')
        self._value_dense = dense_einsum.DenseEinsum(output_shape=(
         self._num_heads, self._head_size),
          kernel_initializer=(self._kernel_initializer),
          bias_initializer=(self._bias_initializer),
          kernel_regularizer=(self._kernel_regularizer),
          bias_regularizer=(self._bias_regularizer),
          activity_regularizer=(self._activity_regularizer),
          kernel_constraint=(self._kernel_constraint),
          bias_constraint=(self._bias_constraint),
          name='value')
        self._masked_softmax = masked_softmax.MaskedSoftmax(mask_expansion_axes=[1])
        self._dropout = tf.keras.layers.Dropout(rate=(self._dropout_rate))

    def get_config(self):
        config = {'num_heads':self._num_heads, 
         'head_size':self._head_size, 
         'dropout_rate':self._dropout_rate, 
         'kernel_initializer':tf.keras.initializers.serialize(self._kernel_initializer), 
         'bias_initializer':tf.keras.initializers.serialize(self._bias_initializer), 
         'kernel_regularizer':tf.keras.regularizers.serialize(self._kernel_regularizer), 
         'bias_regularizer':tf.keras.regularizers.serialize(self._bias_regularizer), 
         'activity_regularizer':tf.keras.regularizers.serialize(self._activity_regularizer), 
         'kernel_constraint':tf.keras.constraints.serialize(self._kernel_constraint), 
         'bias_constraint':tf.keras.constraints.serialize(self._bias_constraint)}
        base_config = super(MultiHeadAttention, self).get_config()
        return dict(list(base_config.items()) + list(config.items()))

    def call(self, inputs):
        from_tensor = inputs[0]
        to_tensor = inputs[1]
        attention_mask = inputs[2] if len(inputs) == 3 else None
        query_tensor = self._query_dense(from_tensor)
        key_tensor = self._key_dense(to_tensor)
        value_tensor = self._value_dense(to_tensor)
        attention_scores = tf.einsum('BTNH,BFNH->BNFT', key_tensor, query_tensor)
        attention_scores = tf.multiply(attention_scores, 1.0 / math.sqrt(float(self._head_size)))
        attention_probs = self._masked_softmax([attention_scores, attention_mask])
        attention_probs = self._dropout(attention_probs)
        return tf.einsum('BNFT,BTNH->BFNH', attention_probs, value_tensor)


@tf.keras.utils.register_keras_serializable(package='Text')
class CachedAttention(MultiHeadAttention):
    __doc__ = 'Attention layer with cache used for auto-agressive decoding.\n\n  Arguments:\n    num_heads: Number of attention heads.\n    head_size: Size of each attention head.\n    **kwargs: Other keyword arguments inherit from `Attention` class.\n  '

    def __init__(self, num_heads, head_size, **kwargs):
        (super(CachedAttention, self).__init__)(num_heads, head_size, **kwargs)

    def _update_cache(self, key_tensor, value_tensor, cache, decode_loop_step):
        """Updates cache states and gets full-length key/value tensors."""
        if decode_loop_step is not None:
            key_seq_dim = cache['key'].shape.as_list()[1]
            indices = tf.reshape(tf.one_hot(decode_loop_step, key_seq_dim, dtype=(key_tensor.dtype)), [
             1, key_seq_dim, 1, 1])
            key_tensor = cache['key'] + key_tensor * indices
            value_seq_dim = cache['value'].shape.as_list()[1]
            indices = tf.reshape(tf.one_hot(decode_loop_step, value_seq_dim, dtype=(value_tensor.dtype)), [
             1, value_seq_dim, 1, 1])
            value_tensor = cache['value'] + value_tensor * indices
        else:
            key_tensor = tf.concat([
             tf.cast(cache['key'], key_tensor.dtype), key_tensor],
              axis=1)
            value_tensor = tf.concat([
             tf.cast(cache['value'], value_tensor.dtype), value_tensor],
              axis=1)
        cache['key'] = key_tensor
        cache['value'] = value_tensor
        return (
         key_tensor, value_tensor)

    def call(self, inputs, decode_loop_step=None):
        from_tensor = inputs[0]
        to_tensor = inputs[1]
        attention_mask = inputs[2] if len(inputs) >= 3 else None
        cache = inputs[3] if len(inputs) >= 4 else None
        query_tensor = self._query_dense(from_tensor)
        key_tensor = self._key_dense(to_tensor)
        value_tensor = self._value_dense(to_tensor)
        if cache:
            key_tensor, value_tensor = self._update_cache(key_tensor, value_tensor, cache, decode_loop_step)
        attention_scores = tf.einsum('BTNH,BFNH->BNFT', key_tensor, query_tensor)
        attention_scores = tf.multiply(attention_scores, 1.0 / math.sqrt(float(self._head_size)))
        attention_probs = self._masked_softmax([attention_scores, attention_mask])
        attention_probs = self._dropout(attention_probs)
        return (
         tf.einsum('BNFT,BTNH->BFNH', attention_probs, value_tensor), cache)