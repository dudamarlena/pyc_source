# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\poda\transfer_learning\InceptionV4_slim.py
# Compiled at: 2019-09-26 09:27:13
# Size of source mod 2**32: 16042 bytes
__doc__ = 'Contains the definition of the Inception V4 architecture.\nAs described in http://arxiv.org/abs/1602.07261.\n  Inception-v4, Inception-ResNet and the Impact of Residual Connections\n    on Learning\n  Christian Szegedy, Sergey Ioffe, Vincent Vanhoucke, Alex Alemi\n'
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import tensorflow as tf
slim = tf.contrib.slim
from poda.layers.activation import *
from poda.layers.dense import *
from poda.layers.regularizer import *

def block_inception_a(inputs, scope=None, reuse=None):
    """Builds Inception-A block for Inception v4 network."""
    with slim.arg_scope([slim.conv2d, slim.avg_pool2d, slim.max_pool2d], stride=1,
      padding='SAME'):
        with tf.variable_scope(scope, 'BlockInceptionA', [inputs], reuse=reuse):
            with tf.variable_scope('Branch_0'):
                branch_0 = slim.conv2d(inputs, 96, [1, 1], scope='Conv2d_0a_1x1')
            with tf.variable_scope('Branch_1'):
                branch_1 = slim.conv2d(inputs, 64, [1, 1], scope='Conv2d_0a_1x1')
                branch_1 = slim.conv2d(branch_1, 96, [3, 3], scope='Conv2d_0b_3x3')
            with tf.variable_scope('Branch_2'):
                branch_2 = slim.conv2d(inputs, 64, [1, 1], scope='Conv2d_0a_1x1')
                branch_2 = slim.conv2d(branch_2, 96, [3, 3], scope='Conv2d_0b_3x3')
                branch_2 = slim.conv2d(branch_2, 96, [3, 3], scope='Conv2d_0c_3x3')
            with tf.variable_scope('Branch_3'):
                branch_3 = slim.avg_pool2d(inputs, [3, 3], scope='AvgPool_0a_3x3')
                branch_3 = slim.conv2d(branch_3, 96, [1, 1], scope='Conv2d_0b_1x1')
            return tf.concat(axis=3, values=[branch_0, branch_1, branch_2, branch_3])


def block_reduction_a(inputs, scope=None, reuse=None):
    """Builds Reduction-A block for Inception v4 network."""
    with slim.arg_scope([slim.conv2d, slim.avg_pool2d, slim.max_pool2d], stride=1,
      padding='SAME'):
        with tf.variable_scope(scope, 'BlockReductionA', [inputs], reuse=reuse):
            with tf.variable_scope('Branch_0'):
                branch_0 = slim.conv2d(inputs, 384, [3, 3], stride=2, padding='VALID', scope='Conv2d_1a_3x3')
            with tf.variable_scope('Branch_1'):
                branch_1 = slim.conv2d(inputs, 192, [1, 1], scope='Conv2d_0a_1x1')
                branch_1 = slim.conv2d(branch_1, 224, [3, 3], scope='Conv2d_0b_3x3')
                branch_1 = slim.conv2d(branch_1, 256, [3, 3], stride=2, padding='VALID',
                  scope='Conv2d_1a_3x3')
            with tf.variable_scope('Branch_2'):
                branch_2 = slim.max_pool2d(inputs, [3, 3], stride=2, padding='VALID', scope='MaxPool_1a_3x3')
            return tf.concat(axis=3, values=[branch_0, branch_1, branch_2])


def block_inception_b(inputs, scope=None, reuse=None):
    """Builds Inception-B block for Inception v4 network."""
    with slim.arg_scope([slim.conv2d, slim.avg_pool2d, slim.max_pool2d], stride=1,
      padding='SAME'):
        with tf.variable_scope(scope, 'BlockInceptionB', [inputs], reuse=reuse):
            with tf.variable_scope('Branch_0'):
                branch_0 = slim.conv2d(inputs, 384, [1, 1], scope='Conv2d_0a_1x1')
            with tf.variable_scope('Branch_1'):
                branch_1 = slim.conv2d(inputs, 192, [1, 1], scope='Conv2d_0a_1x1')
                branch_1 = slim.conv2d(branch_1, 224, [1, 7], scope='Conv2d_0b_1x7')
                branch_1 = slim.conv2d(branch_1, 256, [7, 1], scope='Conv2d_0c_7x1')
            with tf.variable_scope('Branch_2'):
                branch_2 = slim.conv2d(inputs, 192, [1, 1], scope='Conv2d_0a_1x1')
                branch_2 = slim.conv2d(branch_2, 192, [7, 1], scope='Conv2d_0b_7x1')
                branch_2 = slim.conv2d(branch_2, 224, [1, 7], scope='Conv2d_0c_1x7')
                branch_2 = slim.conv2d(branch_2, 224, [7, 1], scope='Conv2d_0d_7x1')
                branch_2 = slim.conv2d(branch_2, 256, [1, 7], scope='Conv2d_0e_1x7')
            with tf.variable_scope('Branch_3'):
                branch_3 = slim.avg_pool2d(inputs, [3, 3], scope='AvgPool_0a_3x3')
                branch_3 = slim.conv2d(branch_3, 128, [1, 1], scope='Conv2d_0b_1x1')
            return tf.concat(axis=3, values=[branch_0, branch_1, branch_2, branch_3])


def block_reduction_b(inputs, scope=None, reuse=None):
    """Builds Reduction-B block for Inception v4 network."""
    with slim.arg_scope([slim.conv2d, slim.avg_pool2d, slim.max_pool2d], stride=1,
      padding='SAME'):
        with tf.variable_scope(scope, 'BlockReductionB', [inputs], reuse=reuse):
            with tf.variable_scope('Branch_0'):
                branch_0 = slim.conv2d(inputs, 192, [1, 1], scope='Conv2d_0a_1x1')
                branch_0 = slim.conv2d(branch_0, 192, [3, 3], stride=2, padding='VALID',
                  scope='Conv2d_1a_3x3')
            with tf.variable_scope('Branch_1'):
                branch_1 = slim.conv2d(inputs, 256, [1, 1], scope='Conv2d_0a_1x1')
                branch_1 = slim.conv2d(branch_1, 256, [1, 7], scope='Conv2d_0b_1x7')
                branch_1 = slim.conv2d(branch_1, 320, [7, 1], scope='Conv2d_0c_7x1')
                branch_1 = slim.conv2d(branch_1, 320, [3, 3], stride=2, padding='VALID',
                  scope='Conv2d_1a_3x3')
            with tf.variable_scope('Branch_2'):
                branch_2 = slim.max_pool2d(inputs, [3, 3], stride=2, padding='VALID', scope='MaxPool_1a_3x3')
            return tf.concat(axis=3, values=[branch_0, branch_1, branch_2])


def block_inception_c(inputs, scope=None, reuse=None):
    """Builds Inception-C block for Inception v4 network."""
    with slim.arg_scope([slim.conv2d, slim.avg_pool2d, slim.max_pool2d], stride=1,
      padding='SAME'):
        with tf.variable_scope(scope, 'BlockInceptionC', [inputs], reuse=reuse):
            with tf.variable_scope('Branch_0'):
                branch_0 = slim.conv2d(inputs, 256, [1, 1], scope='Conv2d_0a_1x1')
            with tf.variable_scope('Branch_1'):
                branch_1 = slim.conv2d(inputs, 384, [1, 1], scope='Conv2d_0a_1x1')
                branch_1 = tf.concat(axis=3, values=[
                 slim.conv2d(branch_1, 256, [1, 3], scope='Conv2d_0b_1x3'),
                 slim.conv2d(branch_1, 256, [3, 1], scope='Conv2d_0c_3x1')])
            with tf.variable_scope('Branch_2'):
                branch_2 = slim.conv2d(inputs, 384, [1, 1], scope='Conv2d_0a_1x1')
                branch_2 = slim.conv2d(branch_2, 448, [3, 1], scope='Conv2d_0b_3x1')
                branch_2 = slim.conv2d(branch_2, 512, [1, 3], scope='Conv2d_0c_1x3')
                branch_2 = tf.concat(axis=3, values=[
                 slim.conv2d(branch_2, 256, [1, 3], scope='Conv2d_0d_1x3'),
                 slim.conv2d(branch_2, 256, [3, 1], scope='Conv2d_0e_3x1')])
            with tf.variable_scope('Branch_3'):
                branch_3 = slim.avg_pool2d(inputs, [3, 3], scope='AvgPool_0a_3x3')
                branch_3 = slim.conv2d(branch_3, 256, [1, 1], scope='Conv2d_0b_1x1')
            return tf.concat(axis=3, values=[branch_0, branch_1, branch_2, branch_3])


def inception_v4_base(inputs, final_endpoint='Mixed_7d', scope=None):
    """Creates the Inception V4 network up to the given final endpoint.
  Args:
    inputs: a 4-D tensor of size [batch_size, height, width, 3].
    final_endpoint: specifies the endpoint to construct the network up to.
      It can be one of [ 'Conv2d_1a_3x3', 'Conv2d_2a_3x3', 'Conv2d_2b_3x3',
      'Mixed_3a', 'Mixed_4a', 'Mixed_5a', 'Mixed_5b', 'Mixed_5c', 'Mixed_5d',
      'Mixed_5e', 'Mixed_6a', 'Mixed_6b', 'Mixed_6c', 'Mixed_6d', 'Mixed_6e',
      'Mixed_6f', 'Mixed_6g', 'Mixed_6h', 'Mixed_7a', 'Mixed_7b', 'Mixed_7c',
      'Mixed_7d']
    scope: Optional variable_scope.
  Returns:
    logits: the logits outputs of the model.
    end_points: the set of end_points from the inception model.
  Raises:
    ValueError: if final_endpoint is not set to one of the predefined values,
  """
    end_points = {}

    def add_and_check_final(name, net):
        end_points[name] = net
        return name == final_endpoint

    with tf.variable_scope(scope, 'InceptionV4', [inputs]):
        with slim.arg_scope([slim.conv2d, slim.max_pool2d, slim.avg_pool2d], stride=1,
          padding='SAME'):
            net = slim.conv2d(inputs, 32, [3, 3], stride=2, padding='VALID',
              scope='Conv2d_1a_3x3')
            if add_and_check_final('Conv2d_1a_3x3', net):
                return (
                 net, end_points)
            net = slim.conv2d(net, 32, [3, 3], padding='VALID', scope='Conv2d_2a_3x3')
            if add_and_check_final('Conv2d_2a_3x3', net):
                return (
                 net, end_points)
            net = slim.conv2d(net, 64, [3, 3], scope='Conv2d_2b_3x3')
            if add_and_check_final('Conv2d_2b_3x3', net):
                return (
                 net, end_points)
            with tf.variable_scope('Mixed_3a'):
                with tf.variable_scope('Branch_0'):
                    branch_0 = slim.max_pool2d(net, [3, 3], stride=2, padding='VALID', scope='MaxPool_0a_3x3')
                with tf.variable_scope('Branch_1'):
                    branch_1 = slim.conv2d(net, 96, [3, 3], stride=2, padding='VALID', scope='Conv2d_0a_3x3')
                net = tf.concat(axis=3, values=[branch_0, branch_1])
                if add_and_check_final('Mixed_3a', net):
                    return (
                     net, end_points)
            with tf.variable_scope('Mixed_4a'):
                with tf.variable_scope('Branch_0'):
                    branch_0 = slim.conv2d(net, 64, [1, 1], scope='Conv2d_0a_1x1')
                    branch_0 = slim.conv2d(branch_0, 96, [3, 3], padding='VALID', scope='Conv2d_1a_3x3')
                with tf.variable_scope('Branch_1'):
                    branch_1 = slim.conv2d(net, 64, [1, 1], scope='Conv2d_0a_1x1')
                    branch_1 = slim.conv2d(branch_1, 64, [1, 7], scope='Conv2d_0b_1x7')
                    branch_1 = slim.conv2d(branch_1, 64, [7, 1], scope='Conv2d_0c_7x1')
                    branch_1 = slim.conv2d(branch_1, 96, [3, 3], padding='VALID', scope='Conv2d_1a_3x3')
                net = tf.concat(axis=3, values=[branch_0, branch_1])
                if add_and_check_final('Mixed_4a', net):
                    return (
                     net, end_points)
            with tf.variable_scope('Mixed_5a'):
                with tf.variable_scope('Branch_0'):
                    branch_0 = slim.conv2d(net, 192, [3, 3], stride=2, padding='VALID', scope='Conv2d_1a_3x3')
                with tf.variable_scope('Branch_1'):
                    branch_1 = slim.max_pool2d(net, [3, 3], stride=2, padding='VALID', scope='MaxPool_1a_3x3')
                net = tf.concat(axis=3, values=[branch_0, branch_1])
                if add_and_check_final('Mixed_5a', net):
                    return (
                     net, end_points)
            for idx in range(4):
                block_scope = 'Mixed_5' + chr(ord('b') + idx)
                net = block_inception_a(net, block_scope)
                if add_and_check_final(block_scope, net):
                    return (
                     net, end_points)

            net = block_reduction_a(net, 'Mixed_6a')
            if add_and_check_final('Mixed_6a', net):
                return (
                 net, end_points)
            for idx in range(7):
                block_scope = 'Mixed_6' + chr(ord('b') + idx)
                net = block_inception_b(net, block_scope)
                if add_and_check_final(block_scope, net):
                    return (
                     net, end_points)

            net = block_reduction_b(net, 'Mixed_7a')
            if add_and_check_final('Mixed_7a', net):
                return (
                 net, end_points)
            for idx in range(3):
                block_scope = 'Mixed_7' + chr(ord('b') + idx)
                net = block_inception_c(net, block_scope)
                if add_and_check_final(block_scope, net):
                    return (
                     net, end_points)

    raise ValueError('Unknown final endpoint %s' % final_endpoint)


def build_top_layer_model(base_layer, num_depthwise_layer=None, dropout_keep_prob=None, regularizers=None, num_classes=1000):
    previous_layer = base_layer
    if num_depthwise_layer != None:
        num_depthwise_layer = num_depthwise_layer
        for i in range(num_depthwise_layer):
            depth_wise_net = depthwise_convolution_2d(input_tensor=previous_layer, number_filters=1, kernel_sizes=(3,
                                                                                                                   3),
              stride_sizes=(2, 2),
              paddings='same',
              activations='relu',
              names=(str(i)))
            previous_layer = depth_wise_net

    else:
        depth_wise_net = previous_layer
    flatten_layer = dropout(input_tensor=flatten_layer, names='output', dropout_rates=dropout_keep_prob)
    flatten_layer = flatten(input_tensor=depth_wise_net)
    full_var_list = tf.compat.v1.get_collection(tf.compat.v1.GraphKeys.GLOBAL_VARIABLES)
    non_logit = dense(input_tensor=flatten_layer, hidden_units=num_classes, activations=None)
    if num_classes > 2:
        output = softmax(input_tensor=non_logit, names='output')
    else:
        output = sigmoid(input_tensor=non_logit, names='output')
    return (non_logit, output, full_var_list)


def inception_v4(inputs, num_classes=1000, final_endpoint='Mixed_7d', is_training=True, dropout_keep_prob=0.2, reuse=None, scope='InceptionV4', create_aux_logits=True, num_depthwise_layer=None, regularizers=None):
    """Creates the Inception V4 model.
  Args:
    inputs: a 4-D tensor of size [batch_size, height, width, 3].
    num_classes: number of predicted classes. If 0 or None, the logits layer
      is omitted and the input features to the logits layer (before dropout)
      are returned instead.
    is_training: whether is training or not.
    dropout_keep_prob: float, the fraction to keep before final layer.
    reuse: whether or not the network and its variables should be reused. To be
      able to reuse 'scope' must be given.
    scope: Optional variable_scope.
    create_aux_logits: Whether to include the auxiliary logits.
  Returns:
    net: a Tensor with the logits (pre-softmax activations) if num_classes
      is a non-zero integer, or the non-dropped input to the logits layer
      if num_classes is 0 or None.
    end_points: the set of end_points from the inception model.
  """
    end_points = {}
    with tf.variable_scope(scope, 'InceptionV4', [inputs], reuse=reuse) as (scope):
        with slim.arg_scope([slim.batch_norm, slim.dropout], is_training=is_training):
            net, end_points = inception_v4_base(inputs, final_endpoint=final_endpoint, scope=scope)
    base_var_list = tf.compat.v1.get_collection(tf.compat.v1.GraphKeys.GLOBAL_VARIABLES)
    non_logit, output, full_var_list = build_top_layer_model(net, num_depthwise_layer=num_depthwise_layer, regularizers=regularizers)
    return (
     non_logit, output, base_var_list, full_var_list)