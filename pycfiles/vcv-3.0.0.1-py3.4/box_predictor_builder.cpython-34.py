# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/object_detection/builders/box_predictor_builder.py
# Compiled at: 2018-06-15 01:39:54
# Size of source mod 2**32: 4989 bytes
"""Function to build box predictor from configuration."""
from object_detection.core import box_predictor
from object_detection.protos import box_predictor_pb2

def build(argscope_fn, box_predictor_config, is_training, num_classes):
    """Builds box predictor based on the configuration.

  Builds box predictor based on the configuration. See box_predictor.proto for
  configurable options. Also, see box_predictor.py for more details.

  Args:
    argscope_fn: A function that takes the following inputs:
        * hyperparams_pb2.Hyperparams proto
        * a boolean indicating if the model is in training mode.
      and returns a tf slim argscope for Conv and FC hyperparameters.
    box_predictor_config: box_predictor_pb2.BoxPredictor proto containing
      configuration.
    is_training: Whether the models is in training mode.
    num_classes: Number of classes to predict.

  Returns:
    box_predictor: box_predictor.BoxPredictor object.

  Raises:
    ValueError: On unknown box predictor.
  """
    if not isinstance(box_predictor_config, box_predictor_pb2.BoxPredictor):
        raise ValueError('box_predictor_config not of type box_predictor_pb2.BoxPredictor.')
    box_predictor_oneof = box_predictor_config.WhichOneof('box_predictor_oneof')
    if box_predictor_oneof == 'convolutional_box_predictor':
        conv_box_predictor = box_predictor_config.convolutional_box_predictor
        conv_hyperparams = argscope_fn(conv_box_predictor.conv_hyperparams, is_training)
        box_predictor_object = box_predictor.ConvolutionalBoxPredictor(is_training=is_training, num_classes=num_classes, conv_hyperparams=conv_hyperparams, min_depth=conv_box_predictor.min_depth, max_depth=conv_box_predictor.max_depth, num_layers_before_predictor=conv_box_predictor.num_layers_before_predictor, use_dropout=conv_box_predictor.use_dropout, dropout_keep_prob=conv_box_predictor.dropout_keep_probability, kernel_size=conv_box_predictor.kernel_size, box_code_size=conv_box_predictor.box_code_size, apply_sigmoid_to_scores=conv_box_predictor.apply_sigmoid_to_scores)
        return box_predictor_object
    if box_predictor_oneof == 'mask_rcnn_box_predictor':
        mask_rcnn_box_predictor = box_predictor_config.mask_rcnn_box_predictor
        fc_hyperparams = argscope_fn(mask_rcnn_box_predictor.fc_hyperparams, is_training)
        conv_hyperparams = None
        if mask_rcnn_box_predictor.HasField('conv_hyperparams'):
            conv_hyperparams = argscope_fn(mask_rcnn_box_predictor.conv_hyperparams, is_training)
        box_predictor_object = box_predictor.MaskRCNNBoxPredictor(is_training=is_training, num_classes=num_classes, fc_hyperparams=fc_hyperparams, use_dropout=mask_rcnn_box_predictor.use_dropout, dropout_keep_prob=mask_rcnn_box_predictor.dropout_keep_probability, box_code_size=mask_rcnn_box_predictor.box_code_size, conv_hyperparams=conv_hyperparams, predict_instance_masks=mask_rcnn_box_predictor.predict_instance_masks, mask_prediction_conv_depth=mask_rcnn_box_predictor.mask_prediction_conv_depth, predict_keypoints=mask_rcnn_box_predictor.predict_keypoints)
        return box_predictor_object
    if box_predictor_oneof == 'rfcn_box_predictor':
        rfcn_box_predictor = box_predictor_config.rfcn_box_predictor
        conv_hyperparams = argscope_fn(rfcn_box_predictor.conv_hyperparams, is_training)
        box_predictor_object = box_predictor.RfcnBoxPredictor(is_training=is_training, num_classes=num_classes, conv_hyperparams=conv_hyperparams, crop_size=[
         rfcn_box_predictor.crop_height,
         rfcn_box_predictor.crop_width], num_spatial_bins=[
         rfcn_box_predictor.num_spatial_bins_height,
         rfcn_box_predictor.num_spatial_bins_width], depth=rfcn_box_predictor.depth, box_code_size=rfcn_box_predictor.box_code_size)
        return box_predictor_object
    raise ValueError('Unknown box predictor: {}'.format(box_predictor_oneof))