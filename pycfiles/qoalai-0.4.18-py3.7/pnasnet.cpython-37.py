# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/qoalai/networks/pnasnet.py
# Compiled at: 2019-12-05 07:10:11
# Size of source mod 2**32: 10667 bytes
"""Contains the definition for the PNASNet classification networks.
Paper: https://arxiv.org/abs/1712.00559
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import copy, tensorflow as tf
import tensorflow.contrib as contrib_framework
import tensorflow.contrib as contrib_slim
import tensorflow.contrib as contrib_training
from qoalai.networks import nasnet
from qoalai.networks import nasnet_utils
arg_scope = contrib_framework.arg_scope
slim = contrib_slim

def large_imagenet_config():
    """Large ImageNet configuration based on PNASNet-5."""
    return contrib_training.HParams(stem_multiplier=3.0,
      dense_dropout_keep_prob=0.5,
      num_cells=12,
      filter_scaling_rate=2.0,
      num_conv_filters=216,
      drop_path_keep_prob=0.6,
      use_aux_head=0,
      num_reduction_layers=2,
      data_format='NHWC',
      skip_reduction_layer_input=1,
      total_training_steps=250000,
      use_bounded_activation=False)


def mobile_imagenet_config():
    """Mobile ImageNet configuration based on PNASNet-5."""
    return contrib_training.HParams(stem_multiplier=1.0,
      dense_dropout_keep_prob=0.5,
      num_cells=9,
      filter_scaling_rate=2.0,
      num_conv_filters=54,
      drop_path_keep_prob=1.0,
      use_aux_head=0,
      num_reduction_layers=2,
      data_format='NHWC',
      skip_reduction_layer_input=1,
      total_training_steps=250000,
      use_bounded_activation=False)


def pnasnet_large_arg_scope(weight_decay=4e-05, batch_norm_decay=0.9997, batch_norm_epsilon=0.001):
    """Default arg scope for the PNASNet Large ImageNet model."""
    return nasnet.nasnet_large_arg_scope(weight_decay, batch_norm_decay, batch_norm_epsilon)


def pnasnet_mobile_arg_scope(weight_decay=4e-05, batch_norm_decay=0.9997, batch_norm_epsilon=0.001):
    """Default arg scope for the PNASNet Mobile ImageNet model."""
    return nasnet.nasnet_mobile_arg_scope(weight_decay, batch_norm_decay, batch_norm_epsilon)


def _build_pnasnet_base(images, normal_cell, num_classes, hparams, is_training, final_endpoint=None):
    """Constructs a PNASNet image model."""
    end_points = {}

    def add_and_check_endpoint(endpoint_name, net):
        end_points[endpoint_name] = net
        return final_endpoint and endpoint_name == final_endpoint

    reduction_indices = nasnet_utils.calc_reduction_layers(hparams.num_cells, hparams.num_reduction_layers)
    stem = lambda : nasnet._imagenet_stem(images, hparams, normal_cell)
    net, cell_outputs = stem()
    if add_and_check_endpoint('Stem', net):
        return (
         net, end_points)
    aux_head_cell_idxes = []
    if len(reduction_indices) >= 2:
        aux_head_cell_idxes.append(reduction_indices[1] - 1)
    filter_scaling = 1.0
    true_cell_num = 2
    activation_fn = tf.nn.relu6 if hparams.use_bounded_activation else tf.nn.relu
    for cell_num in range(hparams.num_cells):
        is_reduction = cell_num in reduction_indices
        stride = 2 if is_reduction else 1
        if is_reduction:
            filter_scaling *= hparams.filter_scaling_rate
        if not hparams.skip_reduction_layer_input:
            if not is_reduction:
                prev_layer = cell_outputs[(-2)]
            net = normal_cell(net,
              scope=('cell_{}'.format(cell_num)),
              filter_scaling=filter_scaling,
              stride=stride,
              prev_layer=prev_layer,
              cell_num=true_cell_num)
            if add_and_check_endpoint('Cell_{}'.format(cell_num), net):
                return (
                 net, end_points)
            true_cell_num += 1
            cell_outputs.append(net)
            if hparams.use_aux_head and cell_num in aux_head_cell_idxes and num_classes and is_training:
                aux_net = activation_fn(net)
                nasnet._build_aux_head(aux_net, end_points, num_classes, hparams, scope=('aux_{}'.format(cell_num)))

    with tf.variable_scope('final_layer'):
        net = activation_fn(net)
        net = nasnet_utils.global_avg_pool(net)
        return add_and_check_endpoint('global_pool', net) or num_classes or (
         net, end_points)
    return (
     net, None)


def build_pnasnet_large(images, num_classes, is_training=True, final_endpoint=None, config=None):
    """Build PNASNet Large model for the ImageNet Dataset."""
    hparams = copy.deepcopy(config) if config else large_imagenet_config()
    nasnet._update_hparams(hparams, is_training)
    if tf.test.is_gpu_available():
        if hparams.data_format == 'NHWC':
            tf.logging.info('A GPU is available on the machine, consider using NCHW data format for increased speed on GPU.')
    if hparams.data_format == 'NCHW':
        images = tf.transpose(images, [0, 3, 1, 2])
    total_num_cells = hparams.num_cells + 2
    normal_cell = PNasNetNormalCell(hparams.num_conv_filters, hparams.drop_path_keep_prob, total_num_cells, hparams.total_training_steps, hparams.use_bounded_activation)
    with arg_scope([
     slim.dropout, nasnet_utils.drop_path, slim.batch_norm],
      is_training=is_training):
        with arg_scope([slim.avg_pool2d, slim.max_pool2d, slim.conv2d,
         slim.batch_norm, slim.separable_conv2d,
         nasnet_utils.factorized_reduction,
         nasnet_utils.global_avg_pool,
         nasnet_utils.get_channel_index,
         nasnet_utils.get_channel_dim],
          data_format=(hparams.data_format)):
            return _build_pnasnet_base(images,
              normal_cell=normal_cell,
              num_classes=num_classes,
              hparams=hparams,
              is_training=is_training,
              final_endpoint=final_endpoint)


build_pnasnet_large.default_image_size = 331

def build_pnasnet_mobile(images, num_classes, is_training=True, final_endpoint=None, config=None):
    """Build PNASNet Mobile model for the ImageNet Dataset."""
    hparams = copy.deepcopy(config) if config else mobile_imagenet_config()
    nasnet._update_hparams(hparams, is_training)
    if tf.test.is_gpu_available():
        if hparams.data_format == 'NHWC':
            tf.logging.info('A GPU is available on the machine, consider using NCHW data format for increased speed on GPU.')
    if hparams.data_format == 'NCHW':
        images = tf.transpose(images, [0, 3, 1, 2])
    total_num_cells = hparams.num_cells + 2
    normal_cell = PNasNetNormalCell(hparams.num_conv_filters, hparams.drop_path_keep_prob, total_num_cells, hparams.total_training_steps, hparams.use_bounded_activation)
    with arg_scope([
     slim.dropout, nasnet_utils.drop_path, slim.batch_norm],
      is_training=is_training):
        with arg_scope([
         slim.avg_pool2d, slim.max_pool2d, slim.conv2d, slim.batch_norm,
         slim.separable_conv2d, nasnet_utils.factorized_reduction,
         nasnet_utils.global_avg_pool, nasnet_utils.get_channel_index,
         nasnet_utils.get_channel_dim],
          data_format=(hparams.data_format)):
            return _build_pnasnet_base(images,
              normal_cell=normal_cell,
              num_classes=num_classes,
              hparams=hparams,
              is_training=is_training,
              final_endpoint=final_endpoint)


build_pnasnet_mobile.default_image_size = 224

class PNasNetNormalCell(nasnet_utils.NasNetABaseCell):
    __doc__ = 'PNASNet Normal Cell.'

    def __init__(self, num_conv_filters, drop_path_keep_prob, total_num_cells, total_training_steps, use_bounded_activation=False):
        operations = [
         'separable_5x5_2', 'max_pool_3x3', 'separable_7x7_2', 'max_pool_3x3',
         'separable_5x5_2', 'separable_3x3_2', 'separable_3x3_2', 'max_pool_3x3',
         'separable_3x3_2', 'none']
        used_hiddenstates = [
         1, 1, 0, 0, 0, 0, 0]
        hiddenstate_indices = [1, 1, 0, 0, 0, 0, 4, 0, 1, 0]
        super(PNasNetNormalCell, self).__init__(num_conv_filters, operations, used_hiddenstates, hiddenstate_indices, drop_path_keep_prob, total_num_cells, total_training_steps, use_bounded_activation)