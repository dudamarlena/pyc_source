# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/svpino/dev/tensorflow-object-detection-sagemaker/todl/tensorflow-object-detection/research/object_detection/predictors/mask_rcnn_keras_box_predictor.py
# Compiled at: 2020-04-05 19:50:57
# Size of source mod 2**32: 5825 bytes
"""Mask R-CNN Box Predictor."""
from object_detection.core import box_predictor
BOX_ENCODINGS = box_predictor.BOX_ENCODINGS
CLASS_PREDICTIONS_WITH_BACKGROUND = box_predictor.CLASS_PREDICTIONS_WITH_BACKGROUND
MASK_PREDICTIONS = box_predictor.MASK_PREDICTIONS

class MaskRCNNKerasBoxPredictor(box_predictor.KerasBoxPredictor):
    __doc__ = 'Mask R-CNN Box Predictor.\n\n  See Mask R-CNN: He, K., Gkioxari, G., Dollar, P., & Girshick, R. (2017).\n  Mask R-CNN. arXiv preprint arXiv:1703.06870.\n\n  This is used for the second stage of the Mask R-CNN detector where proposals\n  cropped from an image are arranged along the batch dimension of the input\n  image_features tensor. Notice that locations are *not* shared across classes,\n  thus for each anchor, a separate prediction is made for each class.\n\n  In addition to predicting boxes and classes, optionally this class allows\n  predicting masks and/or keypoints inside detection boxes.\n\n  Currently this box predictor makes per-class predictions; that is, each\n  anchor makes a separate box prediction for each class.\n  '

    def __init__(self, is_training, num_classes, freeze_batchnorm, box_prediction_head, class_prediction_head, third_stage_heads, name=None):
        """Constructor.

    Args:
      is_training: Indicates whether the BoxPredictor is in training mode.
      num_classes: number of classes.  Note that num_classes *does not*
        include the background category, so if groundtruth labels take values
        in {0, 1, .., K-1}, num_classes=K (and not K+1, even though the
        assigned classification targets can range from {0,... K}).
      freeze_batchnorm: Whether to freeze batch norm parameters during
        training or not. When training with a small batch size (e.g. 1), it is
        desirable to freeze batch norm update and use pretrained batch norm
        params.
      box_prediction_head: The head that predicts the boxes in second stage.
      class_prediction_head: The head that predicts the classes in second stage.
      third_stage_heads: A dictionary mapping head names to mask rcnn head
        classes.
      name: A string name scope to assign to the model. If `None`, Keras
        will auto-generate one from the class name.
    """
        super(MaskRCNNKerasBoxPredictor, self).__init__(is_training,
          num_classes, freeze_batchnorm=freeze_batchnorm, inplace_batchnorm_update=False,
          name=name)
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

    def _predict(self, image_features, prediction_stage=2, **kwargs):
        """Optionally computes encoded object locations, confidences, and masks.

    Predicts the heads belonging to the given prediction stage.

    Args:
      image_features: A list of float tensors of shape
        [batch_size, height_i, width_i, channels_i] containing roi pooled
        features for each image. The length of the list should be 1 otherwise
        a ValueError will be raised.
      prediction_stage: Prediction stage. Acceptable values are 2 and 3.
      **kwargs: Unused Keyword args

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
        if len(image_features) != 1:
            raise ValueError('length of `image_features` must be 1. Found {}'.format(len(image_features)))
        else:
            image_feature = image_features[0]
            predictions_dict = {}
            if prediction_stage == 2:
                predictions_dict[BOX_ENCODINGS] = self._box_prediction_head(image_feature)
                predictions_dict[CLASS_PREDICTIONS_WITH_BACKGROUND] = self._class_prediction_head(image_feature)
            else:
                if prediction_stage == 3:
                    for prediction_head in self.get_third_stage_prediction_heads():
                        head_object = self._third_stage_heads[prediction_head]
                        predictions_dict[prediction_head] = head_object(image_feature)

                else:
                    raise ValueError('prediction_stage should be either 2 or 3.')
        return predictions_dict