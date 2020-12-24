# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/simple_tensor/transfer_learning/inception_utils.py
# Compiled at: 2019-02-17 22:31:48
# Size of source mod 2**32: 2967 bytes
"""Contains common code shared by all inception models.
Usage of arg scope:
  with slim.arg_scope(inception_arg_scope()):
    logits, end_points = inception.inception_v3(images, num_classes,
                                                is_training=is_training)
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import tensorflow as tf
slim = tf.contrib.slim

def inception_arg_scope(weight_decay=4e-05, use_batch_norm=True, batch_norm_decay=0.9997, batch_norm_epsilon=0.001, activation_fn=tf.nn.relu, batch_norm_updates_collections=tf.GraphKeys.UPDATE_OPS):
    """Defines the default arg scope for inception models.
  Args:
    weight_decay: The weight decay to use for regularizing the model.
    use_batch_norm: "If `True`, batch_norm is applied after each convolution.
    batch_norm_decay: Decay for batch norm moving average.
    batch_norm_epsilon: Small float added to variance to avoid dividing by zero
      in batch norm.
    activation_fn: Activation function for conv2d.
    batch_norm_updates_collections: Collection for the update ops for
      batch norm.
  Returns:
    An `arg_scope` to use for the inception models.
  """
    batch_norm_params = {'decay':batch_norm_decay, 
     'epsilon':batch_norm_epsilon, 
     'updates_collections':batch_norm_updates_collections, 
     'fused':None}
    if use_batch_norm:
        normalizer_fn = slim.batch_norm
        normalizer_params = batch_norm_params
    else:
        normalizer_fn = None
        normalizer_params = {}
    with slim.arg_scope([slim.conv2d, slim.fully_connected], weights_regularizer=(slim.l2_regularizer(weight_decay))):
        with slim.arg_scope([
         slim.conv2d],
          weights_initializer=(slim.variance_scaling_initializer()),
          activation_fn=activation_fn,
          normalizer_fn=normalizer_fn,
          normalizer_params=normalizer_params) as (sc):
            return sc