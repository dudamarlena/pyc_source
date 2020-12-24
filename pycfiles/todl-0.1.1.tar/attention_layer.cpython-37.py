# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/svpino/dev/tensorflow-object-detection-sagemaker/todl/tensorflow-object-detection/official/nlp/transformer/attention_layer.py
# Compiled at: 2020-04-05 19:50:57
# Size of source mod 2**32: 6524 bytes
"""Implementation of multiheaded attention and self-attention layers."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import tensorflow as tf
from official.nlp.modeling import layers

class Attention(tf.keras.layers.Layer):
    __doc__ = 'Multi-headed attention layer.'

    def __init__(self, hidden_size, num_heads, attention_dropout):
        if hidden_size % num_heads:
            raise ValueError('Hidden size ({}) must be divisible by the number of heads ({}).'.format(hidden_size, num_heads))
        super(Attention, self).__init__()
        self.hidden_size = hidden_size
        self.num_heads = num_heads
        self.attention_dropout = attention_dropout

    def build(self, input_shape):
        size_per_head = self.hidden_size // self.num_heads
        self.query_dense_layer = layers.DenseEinsum(output_shape=(
         self.num_heads, size_per_head),
          kernel_initializer='glorot_uniform',
          use_bias=False,
          name='query')
        self.key_dense_layer = layers.DenseEinsum(output_shape=(
         self.num_heads, size_per_head),
          kernel_initializer='glorot_uniform',
          use_bias=False,
          name='key')
        self.value_dense_layer = layers.DenseEinsum(output_shape=(
         self.num_heads, size_per_head),
          kernel_initializer='glorot_uniform',
          use_bias=False,
          name='value')
        self.output_dense_layer = layers.DenseEinsum(output_shape=(self.hidden_size),
          num_summed_dimensions=2,
          kernel_initializer='glorot_uniform',
          use_bias=False,
          name='output_transform')
        super(Attention, self).build(input_shape)

    def get_config(self):
        return {'hidden_size':self.hidden_size, 
         'num_heads':self.num_heads, 
         'attention_dropout':self.attention_dropout}

    def call(self, query_input, source_input, bias, training, cache=None, decode_loop_step=None):
        """Apply attention mechanism to query_input and source_input.

    Args:
      query_input: A tensor with shape [batch_size, length_query, hidden_size].
      source_input: A tensor with shape [batch_size, length_source,
        hidden_size].
      bias: A tensor with shape [batch_size, 1, length_query, length_source],
        the attention bias that will be added to the result of the dot product.
      training: A bool, whether in training mode or not.
      cache: (Used during prediction) A dictionary with tensors containing
        results of previous attentions. The dictionary must have the items:
            {"k": tensor with shape [batch_size, i, heads, dim_per_head],
             "v": tensor with shape [batch_size, i, heads, dim_per_head]}
        where i is the current decoded length for non-padded decode, or max
        sequence length for padded decode.
      decode_loop_step: An integer, step number of the decoding loop. Used only
        for autoregressive inference on TPU.

    Returns:
      Attention layer output with shape [batch_size, length_query, hidden_size]
    """
        query = self.query_dense_layer(query_input)
        key = self.key_dense_layer(source_input)
        value = self.value_dense_layer(source_input)
        if cache is not None:
            if decode_loop_step is not None:
                cache_k_shape = cache['k'].shape.as_list()
                indices = tf.reshape(tf.one_hot(decode_loop_step, (cache_k_shape[1]), dtype=(key.dtype)), [
                 1, cache_k_shape[1], 1, 1])
                key = cache['k'] + key * indices
                cache_v_shape = cache['v'].shape.as_list()
                indices = tf.reshape(tf.one_hot(decode_loop_step, (cache_v_shape[1]), dtype=(value.dtype)), [
                 1, cache_v_shape[1], 1, 1])
                value = cache['v'] + value * indices
            else:
                key = tf.concat([tf.cast(cache['k'], key.dtype), key], axis=1)
                value = tf.concat([tf.cast(cache['v'], value.dtype), value], axis=1)
            cache['k'] = key
            cache['v'] = value
        depth = self.hidden_size // self.num_heads
        query *= depth ** (-0.5)
        logits = tf.einsum('BTNH,BFNH->BNFT', key, query)
        logits += bias
        weights = tf.nn.softmax(logits, name='attention_weights')
        if training:
            weights = tf.nn.dropout(weights, rate=(self.attention_dropout))
        attention_output = tf.einsum('BNFT,BTNH->BFNH', weights, value)
        attention_output = self.output_dense_layer(attention_output)
        return attention_output


class SelfAttention(Attention):
    __doc__ = 'Multiheaded self-attention layer.'

    def call(self, query_input, bias, training, cache=None, decode_loop_step=None):
        return super(SelfAttention, self).call(query_input, query_input, bias, training, cache, decode_loop_step)