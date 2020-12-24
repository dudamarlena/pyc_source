# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extenteten/attention.py
# Compiled at: 2017-05-19 10:13:18
# Size of source mod 2**32: 1540 bytes
import tensorflow as tf
from . import collections, summary
from .util import static_shape, func_scope
from .layer import linear
from .variable import variable
from .random import sample_crop
from .softmax import softmax
__all__ = [
 'attention_please']

@func_scope()
def attention_please(xs, context_vector_size, sequence_length=None, name=None):
    attention = _calculate_attention(xs, context_vector_size, sequence_length)
    summary.tensor(attention)
    summary.image(tf.expand_dims(sample_crop(attention, tf.shape(attention)[1]), 0))
    collections.add_attention(attention)
    return _give_attention(xs, attention)


@func_scope()
def _calculate_attention(xs: ('batch', 'sequence', 'embedding'), context_vector_size, sequence_length=None):
    context_vector = variable([context_vector_size, 1], name='context_vector')
    summary.tensor(context_vector)
    attention_logits = tf.reshape(tf.matmul(tf.tanh(linear(tf.reshape(xs, [
     tf.shape(xs)[0] * tf.shape(xs)[1],
     static_shape(xs)[2]]), context_vector_size)), context_vector), tf.shape(xs)[:2])
    return softmax(attention_logits, sequence_length)


@func_scope()
def _give_attention(xs, attention):
    return tf.squeeze(tf.matmul(tf.transpose(xs, [0, 2, 1]), tf.expand_dims(attention, 2)), [
     2])