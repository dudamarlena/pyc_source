# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/svpino/dev/tensorflow-object-detection-sagemaker/todl/tensorflow-object-detection/research/object_detection/predictors/mask_rcnn_box_predictor.py
# Compiled at: 2020-04-05 19:50:57
# Size of source mod 2**32: 6113 bytes
"""Mask R-CNN Box Predictor."""
import tensorflow as tf
from object_detection.core import box_predictor
slim = tf.contrib.slim
BOX_ENCODINGS = box_predictor.BOX_ENCODINGS
CLASS_PREDICTIONS_WITH_BACKGROUND = box_predictor.CLASS_PREDICTIONS_WITH_BACKGROUND
MASK_PREDICTIONS = box_predictor.MASK_PREDICTIONS

class MaskRCNNBoxPredictor(box_predictor.BoxPredictor):
    __doc__ = 'Mask R-CNN Box Predictor.\n\n  See Mask R-CNN: He, K., Gkioxari, G., Dollar, P., & Girshick, R. (2017).\n  Mask R-CNN. arXiv preprint arXiv:1703.06870.\n\n  This is used for the second stage of the Mask R-CNN detector where proposals\n  cropped from an image are arranged along the batch dimension of the input\n  image_features tensor. Notice that locations are *not* shared across classes,\n  thus for each anchor, a separate prediction is made for each class.\n\n  In addition to predicting boxes and classes, optionally this class allows\n  predicting masks and/or keypoints inside detection boxes.\n\n  Currently this box predictor makes per-class predictions; that is, each\n  anchor makes a separate box prediction for each class.\n  '

    def __init__(self, is_training, num_classes, box_prediction_head, class_prediction_head, third_stage_heads):
        super(MaskRCNNBoxPredictor, self).__init__(is_training, num_classes)
        self._box_prediction_head = box_prediction_head
        self._class_prediction_head = class_prediction_head
        self._third_stage_heads = third_stage_heads

    @property
    def num_classes(self):
        return self._num_classes

    def get_second_stage_prediction_heads(self):
        return (
         BOX_ENCODINGS, CLASS_PREDICTIONS_WITH_BACKGROUND)

    def get_third_stage_prediction_heads(self):
        return sorted(self._third_stage_heads.keys())

    def _predict(self, image_features, num_predictions_per_location, prediction_stage=2):
        """Optionally computes encoded object locations, confidences, and masks.

    Predicts the heads belonging to the given prediction stage.

    Args:
      image_features: A list of float tensors of shape
        [batch_size, height_i, width_i, channels_i] containing roi pooled
        features for each image. The length of the list should be 1 otherwise
        a ValueError will be raised.
      num_predictions_per_location: A list of integers representing the number
        of box predictions to be made per spatial location for each feature map.
        Currently, this must be set to [1], or an error will be raised.
      prediction_stage: Prediction stage. Acceptable values are 2 and 3.

    Returns:
      A dictionary containing the predicted tensors that are listed in
      self._prediction_heads. A subset of the following keys will exist in the
      dictionary:
        BOX_ENCODINGS: A float tensor of shape
          [batch_size, 1, num_classes, code_size] representing the
          location of the objects.
        CLASS_PREDICTIONS_WITH_BACKGROUND: A float tensor of shape
          [batch_size, 1, num_classes + 1] representing the class
          predictions for the proposals.
        MASK_PREDICTIONS: A float tensor of shape
          [batch_size, 1, num_classes, image_height, image_width]

    Raises:
      ValueError: If num_predictions_per_location is not 1 or if
        len(image_features) is not 1.
      ValueError: if prediction_stage is not 2 or 3.
    """
        if len(num_predictions_per_location) != 1 or num_predictions_per_location[0] != 1:
            raise ValueError('Currently FullyConnectedBoxPredictor only supports predicting a single box per class per location.')
        else:
            if len(image_features) != 1:
                raise ValueError('length of `image_features` must be 1. Found {}'.format(len(image_features)))
            image_feature = image_features[0]
            predictions_dict = {}
            if prediction_stage == 2:
                predictions_dict[BOX_ENCODINGS] = self._box_prediction_head.predict(features=image_feature,
                  num_predictions_per_location=(num_predictions_per_location[0]))
                predictions_dict[CLASS_PREDICTIONS_WITH_BACKGROUND] = self._class_prediction_head.predict(features=image_feature,
                  num_predictions_per_location=(num_predictions_per_location[0]))
            else:
                if prediction_stage == 3:
                    for prediction_head in self.get_third_stage_prediction_heads():
                        head_object = self._third_stage_heads[prediction_head]
                        predictions_dict[prediction_head] = head_object.predict(features=image_feature,
                          num_predictions_per_location=(num_predictions_per_location[0]))

                else:
                    raise ValueError('prediction_stage should be either 2 or 3.')
        return predictions_dict