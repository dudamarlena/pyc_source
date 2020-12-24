# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/svpino/dev/tensorflow-object-detection-sagemaker/todl/tensorflow-object-detection/research/object_detection/models/faster_rcnn_nas_feature_extractor.py
# Compiled at: 2020-04-05 19:50:57
# Size of source mod 2**32: 12933 bytes
"""NASNet Faster R-CNN implementation.

Learning Transferable Architectures for Scalable Image Recognition
Barret Zoph, Vijay Vasudevan, Jonathon Shlens, Quoc V. Le
https://arxiv.org/abs/1707.07012
"""
import tensorflow as tf
import tensorflow.contrib as contrib_framework
import tensorflow.contrib as contrib_slim
from object_detection.meta_architectures import faster_rcnn_meta_arch
from object_detection.utils import variables_helper
import nets.nasnet as nasnet
from nets.nasnet import nasnet_utils
arg_scope = contrib_framework.arg_scope
slim = contrib_slim

def nasnet_large_arg_scope_for_detection(is_batch_norm_training=False):
    """Defines the default arg scope for the NASNet-A Large for object detection.

  This provides a small edit to switch batch norm training on and off.

  Args:
    is_batch_norm_training: Boolean indicating whether to train with batch norm.

  Returns:
    An `arg_scope` to use for the NASNet Large Model.
  """
    imagenet_scope = nasnet.nasnet_large_arg_scope()
    with arg_scope(imagenet_scope):
        with arg_scope([slim.batch_norm], is_training=is_batch_norm_training) as (sc):
            return sc


def _build_nasnet_base(hidden_previous, hidden, normal_cell, reduction_cell, hparams, true_cell_num, start_cell_num):
    """Constructs a NASNet image model."""
    reduction_indices = nasnet_utils.calc_reduction_layers(hparams.num_cells, hparams.num_reduction_layers)
    cell_outputs = [
     None, hidden_previous, hidden]
    net = hidden
    filter_scaling = 2.0
    for cell_num in range(start_cell_num, hparams.num_cells):
        stride = 1
        if hparams.skip_reduction_layer_input:
            prev_layer = cell_outputs[(-2)]
        if cell_num in reduction_indices:
            filter_scaling *= hparams.filter_scaling_rate
            net = reduction_cell(net,
              scope=('reduction_cell_{}'.format(reduction_indices.index(cell_num))),
              filter_scaling=filter_scaling,
              stride=2,
              prev_layer=(cell_outputs[(-2)]),
              cell_num=true_cell_num)
            true_cell_num += 1
            cell_outputs.append(net)
        if not hparams.skip_reduction_layer_input:
            prev_layer = cell_outputs[(-2)]
        net = normal_cell(net,
          scope=('cell_{}'.format(cell_num)),
          filter_scaling=filter_scaling,
          stride=stride,
          prev_layer=prev_layer,
          cell_num=true_cell_num)
        true_cell_num += 1
        cell_outputs.append(net)

    with tf.variable_scope('final_layer'):
        net = tf.nn.relu(net)
    return net


class FasterRCNNNASFeatureExtractor(faster_rcnn_meta_arch.FasterRCNNFeatureExtractor):
    __doc__ = 'Faster R-CNN with NASNet-A feature extractor implementation.'

    def __init__(self, is_training, first_stage_features_stride, batch_norm_trainable=False, reuse_weights=None, weight_decay=0.0):
        """Constructor.

    Args:
      is_training: See base class.
      first_stage_features_stride: See base class.
      batch_norm_trainable: See base class.
      reuse_weights: See base class.
      weight_decay: See base class.

    Raises:
      ValueError: If `first_stage_features_stride` is not 16.
    """
        if first_stage_features_stride != 16:
            raise ValueError('`first_stage_features_stride` must be 16.')
        super(FasterRCNNNASFeatureExtractor, self).__init__(is_training, first_stage_features_stride, batch_norm_trainable, reuse_weights, weight_decay)

    def preprocess(self, resized_inputs):
        """Faster R-CNN with NAS preprocessing.

    Maps pixel values to the range [-1, 1].

    Args:
      resized_inputs: A [batch, height_in, width_in, channels] float32 tensor
        representing a batch of images with values between 0 and 255.0.

    Returns:
      preprocessed_inputs: A [batch, height_out, width_out, channels] float32
        tensor representing a batch of images.

    """
        return 0.00784313725490196 * resized_inputs - 1.0

    def _extract_proposal_features(self, preprocessed_inputs, scope):
        """Extracts first stage RPN features.

    Extracts features using the first half of the NASNet network.
    We construct the network in `align_feature_maps=True` mode, which means
    that all VALID paddings in the network are changed to SAME padding so that
    the feature maps are aligned.

    Args:
      preprocessed_inputs: A [batch, height, width, channels] float32 tensor
        representing a batch of images.
      scope: A scope name.

    Returns:
      rpn_feature_map: A tensor with shape [batch, height, width, depth]
      end_points: A dictionary mapping feature extractor tensor names to tensors

    Raises:
      ValueError: If the created network is missing the required activation.
    """
        del scope
        if len(preprocessed_inputs.get_shape().as_list()) != 4:
            raise ValueError('`preprocessed_inputs` must be 4 dimensional, got a tensor of shape %s' % preprocessed_inputs.get_shape())
        with slim.arg_scope(nasnet_large_arg_scope_for_detection(is_batch_norm_training=(self._train_batch_norm))):
            with arg_scope([slim.conv2d,
             slim.batch_norm,
             slim.separable_conv2d],
              reuse=(self._reuse_weights)):
                _, end_points = nasnet.build_nasnet_large(preprocessed_inputs,
                  num_classes=None, is_training=(self._is_training),
                  final_endpoint='Cell_11')
        rpn_feature_map = tf.concat([end_points['Cell_10'],
         end_points['Cell_11']], 3)
        batch = preprocessed_inputs.get_shape().as_list()[0]
        shape_without_batch = rpn_feature_map.get_shape().as_list()[1:]
        rpn_feature_map_shape = [batch] + shape_without_batch
        rpn_feature_map.set_shape(rpn_feature_map_shape)
        return (
         rpn_feature_map, end_points)

    def _extract_box_classifier_features(self, proposal_feature_maps, scope):
        """Extracts second stage box classifier features.

    This function reconstructs the "second half" of the NASNet-A
    network after the part defined in `_extract_proposal_features`.

    Args:
      proposal_feature_maps: A 4-D float tensor with shape
        [batch_size * self.max_num_proposals, crop_height, crop_width, depth]
        representing the feature map cropped to each proposal.
      scope: A scope name.

    Returns:
      proposal_classifier_features: A 4-D float tensor with shape
        [batch_size * self.max_num_proposals, height, width, depth]
        representing box classifier features for each proposal.
    """
        del scope
        hidden_previous, hidden = tf.split(proposal_feature_maps, 2, axis=3)
        hparams = nasnet.large_imagenet_config()
        if not self._is_training:
            hparams.set_hparam('drop_path_keep_prob', 1.0)
        total_num_cells = hparams.num_cells + 2
        total_num_cells += 2
        normal_cell = nasnet_utils.NasNetANormalCell(hparams.num_conv_filters, hparams.drop_path_keep_prob, total_num_cells, hparams.total_training_steps)
        reduction_cell = nasnet_utils.NasNetAReductionCell(hparams.num_conv_filters, hparams.drop_path_keep_prob, total_num_cells, hparams.total_training_steps)
        with arg_scope([slim.dropout, nasnet_utils.drop_path], is_training=(self._is_training)):
            with arg_scope([slim.batch_norm], is_training=(self._train_batch_norm)):
                with arg_scope([slim.avg_pool2d,
                 slim.max_pool2d,
                 slim.conv2d,
                 slim.batch_norm,
                 slim.separable_conv2d,
                 nasnet_utils.factorized_reduction,
                 nasnet_utils.global_avg_pool,
                 nasnet_utils.get_channel_index,
                 nasnet_utils.get_channel_dim],
                  data_format=(hparams.data_format)):
                    start_cell_num = 12
                    true_cell_num = 15
                    with slim.arg_scope(nasnet.nasnet_large_arg_scope()):
                        net = _build_nasnet_base(hidden_previous, hidden,
                          normal_cell=normal_cell,
                          reduction_cell=reduction_cell,
                          hparams=hparams,
                          true_cell_num=true_cell_num,
                          start_cell_num=start_cell_num)
        proposal_classifier_features = net
        return proposal_classifier_features

    def restore_from_classification_checkpoint_fn(self, first_stage_feature_extractor_scope, second_stage_feature_extractor_scope):
        """Returns a map of variables to load from a foreign checkpoint.

    Note that this overrides the default implementation in
    faster_rcnn_meta_arch.FasterRCNNFeatureExtractor which does not work for
    NASNet-A checkpoints.

    Args:
      first_stage_feature_extractor_scope: A scope name for the first stage
        feature extractor.
      second_stage_feature_extractor_scope: A scope name for the second stage
        feature extractor.

    Returns:
      A dict mapping variable names (to load from a checkpoint) to variables in
      the model graph.
    """
        variables_to_restore = {}
        for variable in variables_helper.get_global_variables_safely():
            if variable.op.name.startswith(first_stage_feature_extractor_scope):
                var_name = variable.op.name.replace(first_stage_feature_extractor_scope + '/', '')
                var_name += '/ExponentialMovingAverage'
                variables_to_restore[var_name] = variable
            if variable.op.name.startswith(second_stage_feature_extractor_scope):
                var_name = variable.op.name.replace(second_stage_feature_extractor_scope + '/', '')
                var_name += '/ExponentialMovingAverage'
                variables_to_restore[var_name] = variable

        return variables_to_restore