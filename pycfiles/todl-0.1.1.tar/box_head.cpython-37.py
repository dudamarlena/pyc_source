# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/svpino/dev/tensorflow-object-detection-sagemaker/todl/tensorflow-object-detection/research/object_detection/predictors/heads/box_head.py
# Compiled at: 2020-04-05 19:50:57
# Size of source mod 2**32: 11157 bytes
"""Box Head.

Contains Box prediction head classes for different meta architectures.
All the box prediction heads have a predict function that receives the
`features` as the first argument and returns `box_encodings`.
"""
import functools, tensorflow as tf
import tensorflow.contrib as contrib_slim
from object_detection.predictors.heads import head
slim = contrib_slim

class MaskRCNNBoxHead(head.Head):
    __doc__ = 'Box prediction head.\n\n  Please refer to Mask RCNN paper:\n  https://arxiv.org/abs/1703.06870\n  '

    def __init__(self, is_training, num_classes, fc_hyperparams_fn, use_dropout, dropout_keep_prob, box_code_size, share_box_across_classes=False):
        """Constructor.

    Args:
      is_training: Indicates whether the BoxPredictor is in training mode.
      num_classes: number of classes.  Note that num_classes *does not*
        include the background category, so if groundtruth labels take values
        in {0, 1, .., K-1}, num_classes=K (and not K+1, even though the
        assigned classification targets can range from {0,... K}).
      fc_hyperparams_fn: A function to generate tf-slim arg_scope with
        hyperparameters for fully connected ops.
      use_dropout: Option to use dropout or not.  Note that a single dropout
        op is applied here prior to both box and class predictions, which stands
        in contrast to the ConvolutionalBoxPredictor below.
      dropout_keep_prob: Keep probability for dropout.
        This is only used if use_dropout is True.
      box_code_size: Size of encoding for each box.
      share_box_across_classes: Whether to share boxes across classes rather
        than use a different box for each class.
    """
        super(MaskRCNNBoxHead, self).__init__()
        self._is_training = is_training
        self._num_classes = num_classes
        self._fc_hyperparams_fn = fc_hyperparams_fn
        self._use_dropout = use_dropout
        self._dropout_keep_prob = dropout_keep_prob
        self._box_code_size = box_code_size
        self._share_box_across_classes = share_box_across_classes

    def predict(self, features, num_predictions_per_location=1):
        """Predicts boxes.

    Args:
      features: A float tensor of shape [batch_size, height, width,
        channels] containing features for a batch of images.
      num_predictions_per_location: Int containing number of predictions per
        location.

    Returns:
      box_encodings: A float tensor of shape
        [batch_size, 1, num_classes, code_size] representing the location of the
        objects.

    Raises:
      ValueError: If num_predictions_per_location is not 1.
    """
        if num_predictions_per_location != 1:
            raise ValueError('Only num_predictions_per_location=1 is supported')
        else:
            spatial_averaged_roi_pooled_features = tf.reduce_mean(features,
              [1, 2], keep_dims=True, name='AvgPool')
            flattened_roi_pooled_features = slim.flatten(spatial_averaged_roi_pooled_features)
            if self._use_dropout:
                flattened_roi_pooled_features = slim.dropout(flattened_roi_pooled_features,
                  keep_prob=(self._dropout_keep_prob),
                  is_training=(self._is_training))
            number_of_boxes = 1
            number_of_boxes = self._share_box_across_classes or self._num_classes
        with slim.arg_scope(self._fc_hyperparams_fn()):
            box_encodings = slim.fully_connected(flattened_roi_pooled_features,
              (number_of_boxes * self._box_code_size),
              activation_fn=None,
              scope='BoxEncodingPredictor')
        box_encodings = tf.reshape(box_encodings, [
         -1, 1, number_of_boxes, self._box_code_size])
        return box_encodings


class ConvolutionalBoxHead(head.Head):
    __doc__ = 'Convolutional box prediction head.'

    def __init__(self, is_training, box_code_size, kernel_size, use_depthwise=False, box_encodings_clip_range=None):
        """Constructor.

    Args:
      is_training: Indicates whether the BoxPredictor is in training mode.
      box_code_size: Size of encoding for each box.
      kernel_size: Size of final convolution kernel.  If the
        spatial resolution of the feature map is smaller than the kernel size,
        then the kernel size is automatically set to be
        min(feature_width, feature_height).
      use_depthwise: Whether to use depthwise convolutions for prediction
        steps. Default is False.
      box_encodings_clip_range: Min and max values for clipping box_encodings.

    Raises:
      ValueError: if min_depth > max_depth.
      ValueError: if use_depthwise is True and kernel_size is 1.
    """
        if use_depthwise:
            if kernel_size == 1:
                raise ValueError('Should not use 1x1 kernel when using depthwise conv')
        super(ConvolutionalBoxHead, self).__init__()
        self._is_training = is_training
        self._box_code_size = box_code_size
        self._kernel_size = kernel_size
        self._use_depthwise = use_depthwise
        self._box_encodings_clip_range = box_encodings_clip_range

    def predict(self, features, num_predictions_per_location):
        """Predicts boxes.

    Args:
      features: A float tensor of shape [batch_size, height, width, channels]
        containing image features.
      num_predictions_per_location: Number of box predictions to be made per
        spatial location. Int specifying number of boxes per location.

    Returns:
      box_encodings: A float tensors of shape
        [batch_size, num_anchors, q, code_size] representing the location of
        the objects, where q is 1 or the number of classes.
    """
        net = features
        if self._use_depthwise:
            box_encodings = slim.separable_conv2d(net,
              None, [self._kernel_size, self._kernel_size], padding='SAME',
              depth_multiplier=1,
              stride=1,
              rate=1,
              scope='BoxEncodingPredictor_depthwise')
            box_encodings = slim.conv2d(box_encodings,
              (num_predictions_per_location * self._box_code_size),
              [1, 1], activation_fn=None,
              normalizer_fn=None,
              normalizer_params=None,
              scope='BoxEncodingPredictor')
        else:
            box_encodings = slim.conv2d(net,
              (num_predictions_per_location * self._box_code_size), [
             self._kernel_size, self._kernel_size],
              activation_fn=None,
              normalizer_fn=None,
              normalizer_params=None,
              scope='BoxEncodingPredictor')
        batch_size = features.get_shape().as_list()[0]
        if batch_size is None:
            batch_size = tf.shape(features)[0]
        if self._box_encodings_clip_range is not None:
            box_encodings = tf.clip_by_value(box_encodings, self._box_encodings_clip_range.min, self._box_encodings_clip_range.max)
        box_encodings = tf.reshape(box_encodings, [
         batch_size, -1, 1, self._box_code_size])
        return box_encodings


class WeightSharedConvolutionalBoxHead(head.Head):
    __doc__ = 'Weight shared convolutional box prediction head.\n\n  This head allows sharing the same set of parameters (weights) when called more\n  then once on different feature maps.\n  '

    def __init__(self, box_code_size, kernel_size=3, use_depthwise=False, box_encodings_clip_range=None, return_flat_predictions=True):
        """Constructor.

    Args:
      box_code_size: Size of encoding for each box.
      kernel_size: Size of final convolution kernel.
      use_depthwise: Whether to use depthwise convolutions for prediction steps.
        Default is False.
      box_encodings_clip_range: Min and max values for clipping box_encodings.
      return_flat_predictions: If true, returns flattened prediction tensor
        of shape [batch, height * width * num_predictions_per_location,
        box_coder]. Otherwise returns the prediction tensor before reshaping,
        whose shape is [batch, height, width, num_predictions_per_location *
        num_class_slots].

    Raises:
      ValueError: if use_depthwise is True and kernel_size is 1.
    """
        if use_depthwise:
            if kernel_size == 1:
                raise ValueError('Should not use 1x1 kernel when using depthwise conv')
        super(WeightSharedConvolutionalBoxHead, self).__init__()
        self._box_code_size = box_code_size
        self._kernel_size = kernel_size
        self._use_depthwise = use_depthwise
        self._box_encodings_clip_range = box_encodings_clip_range
        self._return_flat_predictions = return_flat_predictions

    def predict(self, features, num_predictions_per_location):
        """Predicts boxes.

    Args:
      features: A float tensor of shape [batch_size, height, width, channels]
        containing image features.
      num_predictions_per_location: Number of box predictions to be made per
        spatial location.

    Returns:
      box_encodings: A float tensor of shape
        [batch_size, num_anchors, code_size] representing the location of
        the objects, or a float tensor of shape [batch, height, width,
        num_predictions_per_location * box_code_size] representing grid box
        location predictions if self._return_flat_predictions is False.
    """
        box_encodings_net = features
        if self._use_depthwise:
            conv_op = functools.partial((slim.separable_conv2d), depth_multiplier=1)
        else:
            conv_op = slim.conv2d
        box_encodings = conv_op(box_encodings_net,
          (num_predictions_per_location * self._box_code_size),
          [
         self._kernel_size, self._kernel_size],
          activation_fn=None,
          stride=1,
          padding='SAME',
          normalizer_fn=None,
          scope='BoxPredictor')
        batch_size = features.get_shape().as_list()[0]
        if batch_size is None:
            batch_size = tf.shape(features)[0]
        if self._box_encodings_clip_range is not None:
            box_encodings = tf.clip_by_value(box_encodings, self._box_encodings_clip_range.min, self._box_encodings_clip_range.max)
        if self._return_flat_predictions:
            box_encodings = tf.reshape(box_encodings, [
             batch_size, -1, self._box_code_size])
        return box_encodings