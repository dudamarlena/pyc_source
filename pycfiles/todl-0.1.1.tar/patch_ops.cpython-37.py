# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/svpino/dev/tensorflow-object-detection-sagemaker/todl/tensorflow-object-detection/research/object_detection/utils/patch_ops.py
# Compiled at: 2020-04-05 19:50:58
# Size of source mod 2**32: 3438 bytes
"""Operations for image patches."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import tensorflow as tf

def get_patch_mask(y, x, patch_size, image_shape):
    """Creates a 2D mask array for a square patch of a given size and location.

  The mask is created with its center at the y and x coordinates, which must be
  within the image. While the mask center must be within the image, the mask
  itself can be partially outside of it. If patch_size is an even number, then
  the mask is created with lower-valued coordinates first (top and left).

  Args:
    y: An integer or scalar int32 tensor. The vertical coordinate of the
      patch mask center. Must be within the range [0, image_height).
    x: An integer or scalar int32 tensor. The horizontal coordinate of the
      patch mask center. Must be within the range [0, image_width).
    patch_size: An integer or scalar int32 tensor. The square size of the
      patch mask. Must be at least 1.
    image_shape: A list or 1D int32 tensor representing the shape of the image
      to which the mask will correspond, with the first two values being image
      height and width. For example, [image_height, image_width] or
      [image_height, image_width, image_channels].

  Returns:
    Boolean mask tensor of shape [image_height, image_width] with True values
    for the patch.

  Raises:
    tf.errors.InvalidArgumentError: if x is not in the range [0, image_width), y
      is not in the range [0, image_height), or patch_size is not at least 1.
  """
    image_hw = image_shape[:2]
    mask_center_yx = tf.stack([y, x])
    with tf.control_dependencies([
     tf.debugging.assert_greater_equal(patch_size,
       1, message='Patch size must be >= 1'),
     tf.debugging.assert_greater_equal(mask_center_yx,
       0, message='Patch center (y, x) must be >= (0, 0)'),
     tf.debugging.assert_less(mask_center_yx,
       image_hw, message='Patch center (y, x) must be < image (h, w)')]):
        mask_center_yx = tf.identity(mask_center_yx)
    half_patch_size = tf.cast(patch_size, dtype=(tf.float32)) / 2
    start_yx = mask_center_yx - tf.cast((tf.floor(half_patch_size)), dtype=(tf.int32))
    end_yx = mask_center_yx + tf.cast((tf.ceil(half_patch_size)), dtype=(tf.int32))
    start_yx = tf.maximum(start_yx, 0)
    end_yx = tf.minimum(end_yx, image_hw)
    start_y = start_yx[0]
    start_x = start_yx[1]
    end_y = end_yx[0]
    end_x = end_yx[1]
    lower_pad = image_hw[0] - end_y
    upper_pad = start_y
    left_pad = start_x
    right_pad = image_hw[1] - end_x
    mask = tf.ones([end_y - start_y, end_x - start_x], dtype=(tf.bool))
    return tf.pad(mask, [[upper_pad, lower_pad], [left_pad, right_pad]])