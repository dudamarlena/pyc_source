# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\poda\transfer_learning\inception_utils.py
# Compiled at: 2019-09-26 09:27:13
# Size of source mod 2**32: 3040 bytes
__doc__ = 'Contains common code shared by all inception models.\nUsage of arg scope:\n  with slim.arg_scope(inception_arg_scope()):\n    logits, end_points = inception.inception_v3(images, num_classes,\n                                                is_training=is_training)\n'
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