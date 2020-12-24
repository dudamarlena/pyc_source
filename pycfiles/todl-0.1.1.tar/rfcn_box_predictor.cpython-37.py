# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/svpino/dev/tensorflow-object-detection-sagemaker/todl/tensorflow-object-detection/research/object_detection/predictors/rfcn_box_predictor.py
# Compiled at: 2020-04-05 19:50:57
# Size of source mod 2**32: 7107 bytes
"""RFCN Box Predictor."""
import tensorflow as tf
from object_detection.core import box_predictor
from object_detection.utils import ops
slim = tf.contrib.slim
BOX_ENCODINGS = box_predictor.BOX_ENCODINGS
CLASS_PREDICTIONS_WITH_BACKGROUND = box_predictor.CLASS_PREDICTIONS_WITH_BACKGROUND
MASK_PREDICTIONS = box_predictor.MASK_PREDICTIONS

class RfcnBoxPredictor(box_predictor.BoxPredictor):
    __doc__ = 'RFCN Box Predictor.\n\n  Applies a position sensitive ROI pooling on position sensitive feature maps to\n  predict classes and refined locations. See https://arxiv.org/abs/1605.06409\n  for details.\n\n  This is used for the second stage of the RFCN meta architecture. Notice that\n  locations are *not* shared across classes, thus for each anchor, a separate\n  prediction is made for each class.\n  '

    def __init__(self, is_training, num_classes, conv_hyperparams_fn, num_spatial_bins, depth, crop_size, box_code_size):
        super(RfcnBoxPredictor, self).__init__(is_training, num_classes)
        self._conv_hyperparams_fn = conv_hyperparams_fn
        self._num_spatial_bins = num_spatial_bins
        self._depth = depth
        self._crop_size = crop_size
        self._box_code_size = box_code_size

    @property
    def num_classes(self):
        return self._num_classes

    def _predict(self, image_features, num_predictions_per_location, proposal_boxes):
        """Computes encoded object locations and corresponding confidences.

    Args:
      image_features: A list of float tensors of shape [batch_size, height_i,
      width_i, channels_i] containing features for a batch of images.
      num_predictions_per_location: A list of integers representing the number
        of box predictions to be made per spatial location for each feature map.
        Currently, this must be set to [1], or an error will be raised.
      proposal_boxes: A float tensor of shape [batch_size, num_proposals,
        box_code_size].

    Returns:
      box_encodings: A list of float tensors of shape
        [batch_size, num_anchors_i, q, code_size] representing the location of
        the objects, where q is 1 or the number of classes. Each entry in the
        list corresponds to a feature map in the input `image_features` list.
      class_predictions_with_background: A list of float tensors of shape
        [batch_size, num_anchors_i, num_classes + 1] representing the class
        predictions for the proposals. Each entry in the list corresponds to a
        feature map in the input `image_features` list.

    Raises:
      ValueError: if num_predictions_per_location is not 1 or if
        len(image_features) is not 1.
    """
        if len(num_predictions_per_location) != 1 or num_predictions_per_location[0] != 1:
            raise ValueError('Currently RfcnBoxPredictor only supports predicting a single box per class per location.')
        if len(image_features) != 1:
            raise ValueError('length of `image_features` must be 1. Found {}'.format(len(image_features)))
        image_feature = image_features[0]
        num_predictions_per_location = num_predictions_per_location[0]
        batch_size = tf.shape(proposal_boxes)[0]
        num_boxes = tf.shape(proposal_boxes)[1]
        net = image_feature
        with slim.arg_scope(self._conv_hyperparams_fn()):
            net = slim.conv2d(net, (self._depth), [1, 1], scope='reduce_depth')
            location_feature_map_depth = self._num_spatial_bins[0] * self._num_spatial_bins[1] * self.num_classes * self._box_code_size
            location_feature_map = slim.conv2d(net, location_feature_map_depth, [
             1, 1],
              activation_fn=None, scope='refined_locations')
            box_encodings = ops.batch_position_sensitive_crop_regions(location_feature_map,
              boxes=proposal_boxes,
              crop_size=(self._crop_size),
              num_spatial_bins=(self._num_spatial_bins),
              global_pool=True)
            box_encodings = tf.squeeze(box_encodings, axis=[2, 3])
            box_encodings = tf.reshape(box_encodings, [
             batch_size * num_boxes, 1, self.num_classes,
             self._box_code_size])
            total_classes = self.num_classes + 1
            class_feature_map_depth = self._num_spatial_bins[0] * self._num_spatial_bins[1] * total_classes
            class_feature_map = slim.conv2d(net, class_feature_map_depth, [1, 1], activation_fn=None,
              scope='class_predictions')
            class_predictions_with_background = ops.batch_position_sensitive_crop_regions(class_feature_map,
              boxes=proposal_boxes,
              crop_size=(self._crop_size),
              num_spatial_bins=(self._num_spatial_bins),
              global_pool=True)
            class_predictions_with_background = tf.squeeze(class_predictions_with_background,
              axis=[2, 3])
            class_predictions_with_background = tf.reshape(class_predictions_with_background, [
             batch_size * num_boxes, 1, total_classes])
        return {BOX_ENCODINGS: [box_encodings], 
         CLASS_PREDICTIONS_WITH_BACKGROUND: [
                                             class_predictions_with_background]}