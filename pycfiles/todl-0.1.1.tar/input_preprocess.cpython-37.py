# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/svpino/dev/tensorflow-object-detection-sagemaker/todl/tensorflow-object-detection/research/deeplab/input_preprocess.py
# Compiled at: 2020-04-05 19:50:57
# Size of source mod 2**32: 5580 bytes
"""Prepares the data used for DeepLab training/evaluation."""
import tensorflow as tf
from deeplab.core import feature_extractor
from deeplab.core import preprocess_utils
_PROB_OF_FLIP = 0.5

def preprocess_image_and_label(image, label, crop_height, crop_width, min_resize_value=None, max_resize_value=None, resize_factor=None, min_scale_factor=1.0, max_scale_factor=1.0, scale_factor_step_size=0, ignore_label=255, is_training=True, model_variant=None):
    """Preprocesses the image and label.

  Args:
    image: Input image.
    label: Ground truth annotation label.
    crop_height: The height value used to crop the image and label.
    crop_width: The width value used to crop the image and label.
    min_resize_value: Desired size of the smaller image side.
    max_resize_value: Maximum allowed size of the larger image side.
    resize_factor: Resized dimensions are multiple of factor plus one.
    min_scale_factor: Minimum scale factor value.
    max_scale_factor: Maximum scale factor value.
    scale_factor_step_size: The step size from min scale factor to max scale
      factor. The input is randomly scaled based on the value of
      (min_scale_factor, max_scale_factor, scale_factor_step_size).
    ignore_label: The label value which will be ignored for training and
      evaluation.
    is_training: If the preprocessing is used for training or not.
    model_variant: Model variant (string) for choosing how to mean-subtract the
      images. See feature_extractor.network_map for supported model variants.

  Returns:
    original_image: Original image (could be resized).
    processed_image: Preprocessed image.
    label: Preprocessed ground truth segmentation label.

  Raises:
    ValueError: Ground truth label not provided during training.
  """
    if is_training:
        if label is None:
            raise ValueError('During training, label must be provided.')
    else:
        if model_variant is None:
            tf.logging.warning('Default mean-subtraction is performed. Please specify a model_variant. See feature_extractor.network_map for supported model variants.')
        original_image = image
        processed_image = tf.cast(image, tf.float32)
        if label is not None:
            label = tf.cast(label, tf.int32)
        if min_resize_value or max_resize_value:
            processed_image, label = preprocess_utils.resize_to_range(image=processed_image,
              label=label,
              min_size=min_resize_value,
              max_size=max_resize_value,
              factor=resize_factor,
              align_corners=True)
            original_image = tf.identity(processed_image)
        if is_training:
            scale = preprocess_utils.get_random_scale(min_scale_factor, max_scale_factor, scale_factor_step_size)
            processed_image, label = preprocess_utils.randomly_scale_image_and_label(processed_image, label, scale)
            processed_image.set_shape([None, None, 3])
        image_shape = tf.shape(processed_image)
        image_height = image_shape[0]
        image_width = image_shape[1]
        target_height = image_height + tf.maximum(crop_height - image_height, 0)
        target_width = image_width + tf.maximum(crop_width - image_width, 0)
        mean_pixel = tf.reshape(feature_extractor.mean_pixel(model_variant), [1, 1, 3])
        processed_image = preprocess_utils.pad_to_bounding_box(processed_image, 0, 0, target_height, target_width, mean_pixel)
        if label is not None:
            label = preprocess_utils.pad_to_bounding_box(label, 0, 0, target_height, target_width, ignore_label)
        if is_training and label is not None:
            processed_image, label = preprocess_utils.random_crop([
             processed_image, label], crop_height, crop_width)
    processed_image.set_shape([crop_height, crop_width, 3])
    if label is not None:
        label.set_shape([crop_height, crop_width, 1])
    if is_training:
        processed_image, label, _ = preprocess_utils.flip_dim([
         processed_image, label],
          _PROB_OF_FLIP, dim=1)
    return (original_image, processed_image, label)