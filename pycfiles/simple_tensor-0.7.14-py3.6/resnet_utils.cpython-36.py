# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/simple_tensor/networks/resnet_utils.py
# Compiled at: 2019-09-29 10:59:29
# Size of source mod 2**32: 4560 bytes
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from collections import namedtuple
import tensorflow as tf, tensorflow.contrib.slim as slim

class Block(namedtuple('Block', ['scope', 'unit_fn', 'args'])):
    __doc__ = 'A named tuple describing a ResNet block.\n\n    Its parts are:\n        scope: The scope of the `Block`.\n        unit_fn: The ResNet unit function which takes as input a `Tensor` and returns another `Tensor` with the output of the ResNet unit.\n        args: A list of length equal to the number of units in the `Block`. The list contains one (depth, depth_bottleneck, stride) tuple for each unit in the block to serve as argument to unit_fn.\n    '


def subsample(inputs, factor, scope=None):
    if factor == 1:
        return inputs
    else:
        return slim.max_pool2d(inputs, [1, 1], stride=factor, scope=scope)


def conv2d_same(inputs, num_outputs, kernel_size, stride, rate=1, scope=None):
    if stride == 1:
        return slim.conv2d(inputs, num_outputs, kernel_size, stride=1, rate=rate, padding='SAME', scope=scope)
    else:
        kernel_size_effective = kernel_size + (kernel_size - 1) * (rate - 1)
        pad_total = kernel_size_effective - 1
        pad_beg = pad_total // 2
        pad_end = pad_total - pad_beg
        inputs = tf.pad(inputs, [[0, 0], [pad_beg, pad_end], [pad_beg, pad_end], [0, 0]])
        return slim.conv2d(inputs, num_outputs, kernel_size, stride=stride, rate=rate, padding='VALID', scope=scope)


@slim.add_arg_scope
def stack_blocks_dense(net, blocks, output_stride=None, store_non_strided_activations=False, outputs_collections=None):
    current_stride = 1
    rate = 1
    for block in blocks:
        with tf.variable_scope(block.scope, 'block', [net]) as (sc):
            block_stride = 1
            for i, unit in enumerate(block.args):
                if store_non_strided_activations:
                    if i == len(block.args) - 1:
                        block_stride = unit.get('stride', 1)
                        unit = dict(unit, stride=1)
                with tf.variable_scope(('unit_%d' % (i + 1)), values=[net]):
                    if output_stride is not None and current_stride == output_stride:
                        net = (block.unit_fn)(net, rate=rate, **dict(unit, stride=1))
                        rate *= unit.get('stride', 1)
                    else:
                        net = (block.unit_fn)(net, rate=1, **unit)
                        current_stride *= unit.get('stride', 1)
                    if output_stride is not None:
                        if current_stride > output_stride:
                            raise ValueError('The target output_stride cannot be reached.')

            net = slim.utils.collect_named_outputs(outputs_collections, sc.name, net)
            if output_stride is not None:
                if current_stride == output_stride:
                    rate *= block_stride
            net = subsample(net, block_stride)
            current_stride *= block_stride
            if output_stride is not None:
                if current_stride > output_stride:
                    raise ValueError('The target output_stride cannot be reached.')

    if output_stride is not None:
        if current_stride != output_stride:
            raise ValueError('The target output_stride cannot be reached.')
    return net


def resnet_arg_scope(weight_decay=0.0001, batch_norm_decay=0.9, batch_norm_epsilon=2e-05, batch_norm_scale=True, activation_fn=tf.nn.leaky_relu, use_batch_norm=True, batch_norm_updates_collections=tf.GraphKeys.UPDATE_OPS):
    batch_norm_params = {'decay':batch_norm_decay, 
     'epsilon':batch_norm_epsilon, 
     'scale':batch_norm_scale, 
     'updates_collections':batch_norm_updates_collections, 
     'fused':None, 
     'param_regularizers':{'gamma': slim.l2_regularizer(weight_decay)}}
    with slim.arg_scope([
     slim.conv2d],
      weights_regularizer=(slim.l2_regularizer(weight_decay)),
      weights_initializer=tf.contrib.layers.xavier_initializer(uniform=False),
      activation_fn=activation_fn,
      normalizer_fn=(slim.batch_norm if use_batch_norm else None),
      normalizer_params=batch_norm_params):
        with (slim.arg_scope)([slim.batch_norm], **batch_norm_params):
            with slim.arg_scope([slim.max_pool2d], padding='SAME') as (arg_sc):
                return arg_sc