# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/svpino/dev/tensorflow-object-detection-sagemaker/todl/tensorflow-object-detection/research/object_detection/utils/autoaugment_utils.py
# Compiled at: 2020-04-05 19:50:58
# Size of source mod 2**32: 65203 bytes
"""AutoAugment util file."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import inspect, math, six, tensorflow as tf
_MAX_LEVEL = 10.0
_INVALID_BOX = [
 [
  -1.0, -1.0, -1.0, -1.0]]

def policy_v0():
    """Autoaugment policy that was used in AutoAugment Detection Paper."""
    policy = [
     [
      ('TranslateX_BBox', 0.6, 4), ('Equalize', 0.8, 10)],
     [
      ('TranslateY_Only_BBoxes', 0.2, 2), ('Cutout', 0.8, 8)],
     [
      ('Sharpness', 0.0, 8), ('ShearX_BBox', 0.4, 0)],
     [
      ('ShearY_BBox', 1.0, 2), ('TranslateY_Only_BBoxes', 0.6, 6)],
     [
      ('Rotate_BBox', 0.6, 10), ('Color', 1.0, 6)]]
    return policy


def policy_v1():
    """Autoaugment policy that was used in AutoAugment Detection Paper."""
    policy = [
     [
      ('TranslateX_BBox', 0.6, 4), ('Equalize', 0.8, 10)],
     [
      ('TranslateY_Only_BBoxes', 0.2, 2), ('Cutout', 0.8, 8)],
     [
      ('Sharpness', 0.0, 8), ('ShearX_BBox', 0.4, 0)],
     [
      ('ShearY_BBox', 1.0, 2), ('TranslateY_Only_BBoxes', 0.6, 6)],
     [
      ('Rotate_BBox', 0.6, 10), ('Color', 1.0, 6)],
     [
      ('Color', 0.0, 0), ('ShearX_Only_BBoxes', 0.8, 4)],
     [
      ('ShearY_Only_BBoxes', 0.8, 2), ('Flip_Only_BBoxes', 0.0, 10)],
     [
      ('Equalize', 0.6, 10), ('TranslateX_BBox', 0.2, 2)],
     [
      ('Color', 1.0, 10), ('TranslateY_Only_BBoxes', 0.4, 6)],
     [
      ('Rotate_BBox', 0.8, 10), ('Contrast', 0.0, 10)],
     [
      ('Cutout', 0.2, 2), ('Brightness', 0.8, 10)],
     [
      ('Color', 1.0, 6), ('Equalize', 1.0, 2)],
     [
      ('Cutout_Only_BBoxes', 0.4, 6), ('TranslateY_Only_BBoxes', 0.8, 2)],
     [
      ('Color', 0.2, 8), ('Rotate_BBox', 0.8, 10)],
     [
      ('Sharpness', 0.4, 4), ('TranslateY_Only_BBoxes', 0.0, 4)],
     [
      ('Sharpness', 1.0, 4), ('SolarizeAdd', 0.4, 4)],
     [
      ('Rotate_BBox', 1.0, 8), ('Sharpness', 0.2, 8)],
     [
      ('ShearY_BBox', 0.6, 10), ('Equalize_Only_BBoxes', 0.6, 8)],
     [
      ('ShearX_BBox', 0.2, 6), ('TranslateY_Only_BBoxes', 0.2, 10)],
     [
      ('SolarizeAdd', 0.6, 8), ('Brightness', 0.8, 10)]]
    return policy


def policy_vtest():
    """Autoaugment test policy for debugging."""
    policy = [
     [
      ('TranslateX_BBox', 1.0, 4), ('Equalize', 1.0, 10)]]
    return policy


def policy_v2():
    """Additional policy that performs well on object detection."""
    policy = [
     [
      ('Color', 0.0, 6), ('Cutout', 0.6, 8), ('Sharpness', 0.4, 8)],
     [
      ('Rotate_BBox', 0.4, 8), ('Sharpness', 0.4, 2),
      ('Rotate_BBox', 0.8, 10)],
     [
      ('TranslateY_BBox', 1.0, 8), ('AutoContrast', 0.8, 2)],
     [
      ('AutoContrast', 0.4, 6), ('ShearX_BBox', 0.8, 8),
      ('Brightness', 0.0, 10)],
     [
      ('SolarizeAdd', 0.2, 6), ('Contrast', 0.0, 10),
      ('AutoContrast', 0.6, 0)],
     [
      ('Cutout', 0.2, 0), ('Solarize', 0.8, 8), ('Color', 1.0, 4)],
     [
      ('TranslateY_BBox', 0.0, 4), ('Equalize', 0.6, 8),
      ('Solarize', 0.0, 10)],
     [
      ('TranslateY_BBox', 0.2, 2), ('ShearY_BBox', 0.8, 8),
      ('Rotate_BBox', 0.8, 8)],
     [
      ('Cutout', 0.8, 8), ('Brightness', 0.8, 8), ('Cutout', 0.2, 2)],
     [
      ('Color', 0.8, 4), ('TranslateY_BBox', 1.0, 6), ('Rotate_BBox', 0.6, 6)],
     [
      ('Rotate_BBox', 0.6, 10), ('BBox_Cutout', 1.0, 4), ('Cutout', 0.2, 8)],
     [
      ('Rotate_BBox', 0.0, 0), ('Equalize', 0.6, 6), ('ShearY_BBox', 0.6, 8)],
     [
      ('Brightness', 0.8, 8), ('AutoContrast', 0.4, 2),
      ('Brightness', 0.2, 2)],
     [
      ('TranslateY_BBox', 0.4, 8), ('Solarize', 0.4, 6),
      ('SolarizeAdd', 0.2, 10)],
     [
      ('Contrast', 1.0, 10), ('SolarizeAdd', 0.2, 8), ('Equalize', 0.2, 4)]]
    return policy


def policy_v3():
    """"Additional policy that performs well on object detection."""
    policy = [
     [
      ('Posterize', 0.8, 2), ('TranslateX_BBox', 1.0, 8)],
     [
      ('BBox_Cutout', 0.2, 10), ('Sharpness', 1.0, 8)],
     [
      ('Rotate_BBox', 0.6, 8), ('Rotate_BBox', 0.8, 10)],
     [
      ('Equalize', 0.8, 10), ('AutoContrast', 0.2, 10)],
     [
      ('SolarizeAdd', 0.2, 2), ('TranslateY_BBox', 0.2, 8)],
     [
      ('Sharpness', 0.0, 2), ('Color', 0.4, 8)],
     [
      ('Equalize', 1.0, 8), ('TranslateY_BBox', 1.0, 8)],
     [
      ('Posterize', 0.6, 2), ('Rotate_BBox', 0.0, 10)],
     [
      ('AutoContrast', 0.6, 0), ('Rotate_BBox', 1.0, 6)],
     [
      ('Equalize', 0.0, 4), ('Cutout', 0.8, 10)],
     [
      ('Brightness', 1.0, 2), ('TranslateY_BBox', 1.0, 6)],
     [
      ('Contrast', 0.0, 2), ('ShearY_BBox', 0.8, 0)],
     [
      ('AutoContrast', 0.8, 10), ('Contrast', 0.2, 10)],
     [
      ('Rotate_BBox', 1.0, 10), ('Cutout', 1.0, 10)],
     [
      ('SolarizeAdd', 0.8, 6), ('Equalize', 0.8, 8)]]
    return policy


def blend(image1, image2, factor):
    """Blend image1 and image2 using 'factor'.

  Factor can be above 0.0.  A value of 0.0 means only image1 is used.
  A value of 1.0 means only image2 is used.  A value between 0.0 and
  1.0 means we linearly interpolate the pixel values between the two
  images.  A value greater than 1.0 "extrapolates" the difference
  between the two pixel values, and we clip the results to values
  between 0 and 255.

  Args:
    image1: An image Tensor of type uint8.
    image2: An image Tensor of type uint8.
    factor: A floating point value above 0.0.

  Returns:
    A blended image Tensor of type uint8.
  """
    if factor == 0.0:
        return tf.convert_to_tensor(image1)
    else:
        if factor == 1.0:
            return tf.convert_to_tensor(image2)
        image1 = tf.to_float(image1)
        image2 = tf.to_float(image2)
        difference = image2 - image1
        scaled = factor * difference
        temp = tf.to_float(image1) + scaled
        if factor > 0.0 and factor < 1.0:
            return tf.cast(temp, tf.uint8)
    return tf.cast(tf.clip_by_value(temp, 0.0, 255.0), tf.uint8)


def cutout(image, pad_size, replace=0):
    """Apply cutout (https://arxiv.org/abs/1708.04552) to image.

  This operation applies a (2*pad_size x 2*pad_size) mask of zeros to
  a random location within `img`. The pixel values filled in will be of the
  value `replace`. The located where the mask will be applied is randomly
  chosen uniformly over the whole image.

  Args:
    image: An image Tensor of type uint8.
    pad_size: Specifies how big the zero mask that will be generated is that
      is applied to the image. The mask will be of size
      (2*pad_size x 2*pad_size).
    replace: What pixel value to fill in the image in the area that has
      the cutout mask applied to it.

  Returns:
    An image Tensor that is of type uint8.
  """
    image_height = tf.shape(image)[0]
    image_width = tf.shape(image)[1]
    cutout_center_height = tf.random_uniform(shape=[], minval=0, maxval=image_height, dtype=(tf.int32))
    cutout_center_width = tf.random_uniform(shape=[], minval=0, maxval=image_width, dtype=(tf.int32))
    lower_pad = tf.maximum(0, cutout_center_height - pad_size)
    upper_pad = tf.maximum(0, image_height - cutout_center_height - pad_size)
    left_pad = tf.maximum(0, cutout_center_width - pad_size)
    right_pad = tf.maximum(0, image_width - cutout_center_width - pad_size)
    cutout_shape = [
     image_height - (lower_pad + upper_pad),
     image_width - (left_pad + right_pad)]
    padding_dims = [[lower_pad, upper_pad], [left_pad, right_pad]]
    mask = tf.pad(tf.zeros(cutout_shape, dtype=(image.dtype)),
      padding_dims,
      constant_values=1)
    mask = tf.expand_dims(mask, -1)
    mask = tf.tile(mask, [1, 1, 3])
    image = tf.where(tf.equal(mask, 0), tf.ones_like(image, dtype=(image.dtype)) * replace, image)
    return image


def solarize(image, threshold=128):
    return tf.where(image < threshold, image, 255 - image)


def solarize_add(image, addition=0, threshold=128):
    added_image = tf.cast(image, tf.int64) + addition
    added_image = tf.cast(tf.clip_by_value(added_image, 0, 255), tf.uint8)
    return tf.where(image < threshold, added_image, image)


def color(image, factor):
    """Equivalent of PIL Color."""
    degenerate = tf.image.grayscale_to_rgb(tf.image.rgb_to_grayscale(image))
    return blend(degenerate, image, factor)


def contrast(image, factor):
    """Equivalent of PIL Contrast."""
    degenerate = tf.image.rgb_to_grayscale(image)
    degenerate = tf.cast(degenerate, tf.int32)
    hist = tf.histogram_fixed_width(degenerate, [0, 255], nbins=256)
    mean = tf.reduce_sum(tf.cast(hist, tf.float32)) / 256.0
    degenerate = tf.ones_like(degenerate, dtype=(tf.float32)) * mean
    degenerate = tf.clip_by_value(degenerate, 0.0, 255.0)
    degenerate = tf.image.grayscale_to_rgb(tf.cast(degenerate, tf.uint8))
    return blend(degenerate, image, factor)


def brightness(image, factor):
    """Equivalent of PIL Brightness."""
    degenerate = tf.zeros_like(image)
    return blend(degenerate, image, factor)


def posterize(image, bits):
    """Equivalent of PIL Posterize."""
    shift = 8 - bits
    return tf.bitwise.left_shift(tf.bitwise.right_shift(image, shift), shift)


def rotate(image, degrees, replace):
    """Rotates the image by degrees either clockwise or counterclockwise.

  Args:
    image: An image Tensor of type uint8.
    degrees: Float, a scalar angle in degrees to rotate all images by. If
      degrees is positive the image will be rotated clockwise otherwise it will
      be rotated counterclockwise.
    replace: A one or three value 1D tensor to fill empty pixels caused by
      the rotate operation.

  Returns:
    The rotated version of image.
  """
    degrees_to_radians = math.pi / 180.0
    radians = degrees * degrees_to_radians
    image = tf.contrib.image.rotate(wrap(image), radians)
    return unwrap(image, replace)


def random_shift_bbox(image, bbox, pixel_scaling, replace, new_min_bbox_coords=None):
    """Move the bbox and the image content to a slightly new random location.

  Args:
    image: 3D uint8 Tensor.
    bbox: 1D Tensor that has 4 elements (min_y, min_x, max_y, max_x)
      of type float that represents the normalized coordinates between 0 and 1.
      The potential values for the new min corner of the bbox will be between
      [old_min - pixel_scaling * bbox_height/2,
       old_min - pixel_scaling * bbox_height/2].
    pixel_scaling: A float between 0 and 1 that specifies the pixel range
      that the new bbox location will be sampled from.
    replace: A one or three value 1D tensor to fill empty pixels.
    new_min_bbox_coords: If not None, then this is a tuple that specifies the
      (min_y, min_x) coordinates of the new bbox. Normally this is randomly
      specified, but this allows it to be manually set. The coordinates are
      the absolute coordinates between 0 and image height/width and are int32.

  Returns:
    The new image that will have the shifted bbox location in it along with
    the new bbox that contains the new coordinates.
  """
    image_height = tf.to_float(tf.shape(image)[0])
    image_width = tf.to_float(tf.shape(image)[1])

    def clip_y(val):
        return tf.clip_by_value(val, 0, tf.to_int32(image_height) - 1)

    def clip_x(val):
        return tf.clip_by_value(val, 0, tf.to_int32(image_width) - 1)

    min_y = tf.to_int32(image_height * bbox[0])
    min_x = tf.to_int32(image_width * bbox[1])
    max_y = clip_y(tf.to_int32(image_height * bbox[2]))
    max_x = clip_x(tf.to_int32(image_width * bbox[3]))
    bbox_height, bbox_width = max_y - min_y + 1, max_x - min_x + 1
    image_height = tf.to_int32(image_height)
    image_width = tf.to_int32(image_width)
    minval_y = clip_y(min_y - tf.to_int32(pixel_scaling * tf.to_float(bbox_height) / 2.0))
    maxval_y = clip_y(min_y + tf.to_int32(pixel_scaling * tf.to_float(bbox_height) / 2.0))
    minval_x = clip_x(min_x - tf.to_int32(pixel_scaling * tf.to_float(bbox_width) / 2.0))
    maxval_x = clip_x(min_x + tf.to_int32(pixel_scaling * tf.to_float(bbox_width) / 2.0))
    if new_min_bbox_coords is None:
        unclipped_new_min_y = tf.random_uniform(shape=[], minval=minval_y, maxval=maxval_y, dtype=(tf.int32))
        unclipped_new_min_x = tf.random_uniform(shape=[], minval=minval_x, maxval=maxval_x, dtype=(tf.int32))
    else:
        unclipped_new_min_y, unclipped_new_min_x = clip_y(new_min_bbox_coords[0]), clip_x(new_min_bbox_coords[1])
    unclipped_new_max_y = unclipped_new_min_y + bbox_height - 1
    unclipped_new_max_x = unclipped_new_min_x + bbox_width - 1
    new_min_y, new_min_x, new_max_y, new_max_x = (
     clip_y(unclipped_new_min_y), clip_x(unclipped_new_min_x),
     clip_y(unclipped_new_max_y), clip_x(unclipped_new_max_x))
    shifted_min_y = new_min_y - unclipped_new_min_y + min_y
    shifted_max_y = max_y - (unclipped_new_max_y - new_max_y)
    shifted_min_x = new_min_x - unclipped_new_min_x + min_x
    shifted_max_x = max_x - (unclipped_new_max_x - new_max_x)
    new_bbox = tf.stack([
     tf.to_float(new_min_y) / tf.to_float(image_height),
     tf.to_float(new_min_x) / tf.to_float(image_width),
     tf.to_float(new_max_y) / tf.to_float(image_height),
     tf.to_float(new_max_x) / tf.to_float(image_width)])
    bbox_content = image[shifted_min_y:shifted_max_y + 1,
     shifted_min_x:shifted_max_x + 1, :]

    def mask_and_add_image(min_y_, min_x_, max_y_, max_x_, mask, content_tensor, image_):
        mask = tf.pad(mask, [
         [
          min_y_, image_height - 1 - max_y_],
         [
          min_x_, image_width - 1 - max_x_],
         [
          0, 0]],
          constant_values=1)
        content_tensor = tf.pad(content_tensor, [
         [
          min_y_, image_height - 1 - max_y_],
         [
          min_x_, image_width - 1 - max_x_],
         [
          0, 0]],
          constant_values=0)
        return image_ * mask + content_tensor

    mask = tf.zeros_like(image)[min_y:max_y + 1, min_x:max_x + 1, :]
    grey_tensor = tf.zeros_like(mask) + replace[0]
    image = mask_and_add_image(min_y, min_x, max_y, max_x, mask, grey_tensor, image)
    mask = tf.zeros_like(bbox_content)
    image = mask_and_add_image(new_min_y, new_min_x, new_max_y, new_max_x, mask, bbox_content, image)
    return (
     image, new_bbox)


def _clip_bbox(min_y, min_x, max_y, max_x):
    """Clip bounding box coordinates between 0 and 1.

  Args:
    min_y: Normalized bbox coordinate of type float between 0 and 1.
    min_x: Normalized bbox coordinate of type float between 0 and 1.
    max_y: Normalized bbox coordinate of type float between 0 and 1.
    max_x: Normalized bbox coordinate of type float between 0 and 1.

  Returns:
    Clipped coordinate values between 0 and 1.
  """
    min_y = tf.clip_by_value(min_y, 0.0, 1.0)
    min_x = tf.clip_by_value(min_x, 0.0, 1.0)
    max_y = tf.clip_by_value(max_y, 0.0, 1.0)
    max_x = tf.clip_by_value(max_x, 0.0, 1.0)
    return (min_y, min_x, max_y, max_x)


def _check_bbox_area(min_y, min_x, max_y, max_x, delta=0.05):
    """Adjusts bbox coordinates to make sure the area is > 0.

  Args:
    min_y: Normalized bbox coordinate of type float between 0 and 1.
    min_x: Normalized bbox coordinate of type float between 0 and 1.
    max_y: Normalized bbox coordinate of type float between 0 and 1.
    max_x: Normalized bbox coordinate of type float between 0 and 1.
    delta: Float, this is used to create a gap of size 2 * delta between
      bbox min/max coordinates that are the same on the boundary.
      This prevents the bbox from having an area of zero.

  Returns:
    Tuple of new bbox coordinates between 0 and 1 that will now have a
    guaranteed area > 0.
  """
    height = max_y - min_y
    width = max_x - min_x

    def _adjust_bbox_boundaries(min_coord, max_coord):
        max_coord = tf.maximum(max_coord, 0.0 + delta)
        min_coord = tf.minimum(min_coord, 1.0 - delta)
        return (min_coord, max_coord)

    min_y, max_y = tf.cond(tf.equal(height, 0.0), lambda : _adjust_bbox_boundaries(min_y, max_y), lambda : (
     min_y, max_y))
    min_x, max_x = tf.cond(tf.equal(width, 0.0), lambda : _adjust_bbox_boundaries(min_x, max_x), lambda : (
     min_x, max_x))
    return (min_y, min_x, max_y, max_x)


def _scale_bbox_only_op_probability(prob):
    """Reduce the probability of the bbox-only operation.

  Probability is reduced so that we do not distort the content of too many
  bounding boxes that are close to each other. The value of 3.0 was a chosen
  hyper parameter when designing the autoaugment algorithm that we found
  empirically to work well.

  Args:
    prob: Float that is the probability of applying the bbox-only operation.

  Returns:
    Reduced probability.
  """
    return prob / 3.0


def _apply_bbox_augmentation(image, bbox, augmentation_func, *args):
    """Applies augmentation_func to the subsection of image indicated by bbox.

  Args:
    image: 3D uint8 Tensor.
    bbox: 1D Tensor that has 4 elements (min_y, min_x, max_y, max_x)
      of type float that represents the normalized coordinates between 0 and 1.
    augmentation_func: Augmentation function that will be applied to the
      subsection of image.
    *args: Additional parameters that will be passed into augmentation_func
      when it is called.

  Returns:
    A modified version of image, where the bbox location in the image will
    have `ugmentation_func applied to it.
  """
    image_height = tf.to_float(tf.shape(image)[0])
    image_width = tf.to_float(tf.shape(image)[1])
    min_y = tf.to_int32(image_height * bbox[0])
    min_x = tf.to_int32(image_width * bbox[1])
    max_y = tf.to_int32(image_height * bbox[2])
    max_x = tf.to_int32(image_width * bbox[3])
    image_height = tf.to_int32(image_height)
    image_width = tf.to_int32(image_width)
    max_y = tf.minimum(max_y, image_height - 1)
    max_x = tf.minimum(max_x, image_width - 1)
    bbox_content = image[min_y:max_y + 1, min_x:max_x + 1, :]
    augmented_bbox_content = augmentation_func(bbox_content, *args)
    augmented_bbox_content = tf.pad(augmented_bbox_content, [
     [
      min_y, image_height - 1 - max_y],
     [
      min_x, image_width - 1 - max_x],
     [
      0, 0]])
    mask_tensor = tf.zeros_like(bbox_content)
    mask_tensor = tf.pad(mask_tensor, [
     [
      min_y, image_height - 1 - max_y],
     [
      min_x, image_width - 1 - max_x],
     [
      0, 0]],
      constant_values=1)
    image = image * mask_tensor + augmented_bbox_content
    return image


def _concat_bbox(bbox, bboxes):
    """Helper function that concates bbox to bboxes along the first dimension."""
    bboxes_sum_check = tf.reduce_sum(bboxes)
    bbox = tf.expand_dims(bbox, 0)
    bboxes = tf.cond(tf.equal(bboxes_sum_check, -4.0), lambda : bbox, lambda : tf.concat([bboxes, bbox], 0))
    return bboxes


def _apply_bbox_augmentation_wrapper(image, bbox, new_bboxes, prob, augmentation_func, func_changes_bbox, *args):
    """Applies _apply_bbox_augmentation with probability prob.

  Args:
    image: 3D uint8 Tensor.
    bbox: 1D Tensor that has 4 elements (min_y, min_x, max_y, max_x)
      of type float that represents the normalized coordinates between 0 and 1.
    new_bboxes: 2D Tensor that is a list of the bboxes in the image after they
      have been altered by aug_func. These will only be changed when
      func_changes_bbox is set to true. Each bbox has 4 elements
      (min_y, min_x, max_y, max_x) of type float that are the normalized
      bbox coordinates between 0 and 1.
    prob: Float that is the probability of applying _apply_bbox_augmentation.
    augmentation_func: Augmentation function that will be applied to the
      subsection of image.
    func_changes_bbox: Boolean. Does augmentation_func return bbox in addition
      to image.
    *args: Additional parameters that will be passed into augmentation_func
      when it is called.

  Returns:
    A tuple. Fist element is a modified version of image, where the bbox
    location in the image will have augmentation_func applied to it if it is
    chosen to be called with probability `prob`. The second element is a
    Tensor of Tensors of length 4 that will contain the altered bbox after
    applying augmentation_func.
  """
    should_apply_op = tf.cast(tf.floor(tf.random_uniform([], dtype=(tf.float32)) + prob), tf.bool)
    if func_changes_bbox:
        augmented_image, bbox = tf.cond(should_apply_op, lambda : augmentation_func(image, bbox, *args), lambda : (
         image, bbox))
    else:
        augmented_image = tf.cond(should_apply_op, lambda : _apply_bbox_augmentation(image, bbox, augmentation_func, *args), lambda : image)
    new_bboxes = _concat_bbox(bbox, new_bboxes)
    return (augmented_image, new_bboxes)


def _apply_multi_bbox_augmentation(image, bboxes, prob, aug_func, func_changes_bbox, *args):
    """Applies aug_func to the image for each bbox in bboxes.

  Args:
    image: 3D uint8 Tensor.
    bboxes: 2D Tensor that is a list of the bboxes in the image. Each bbox
      has 4 elements (min_y, min_x, max_y, max_x) of type float.
    prob: Float that is the probability of applying aug_func to a specific
      bounding box within the image.
    aug_func: Augmentation function that will be applied to the
      subsections of image indicated by the bbox values in bboxes.
    func_changes_bbox: Boolean. Does augmentation_func return bbox in addition
      to image.
    *args: Additional parameters that will be passed into augmentation_func
      when it is called.

  Returns:
    A modified version of image, where each bbox location in the image will
    have augmentation_func applied to it if it is chosen to be called with
    probability prob independently across all bboxes. Also the final
    bboxes are returned that will be unchanged if func_changes_bbox is set to
    false and if true, the new altered ones will be returned.
  """
    new_bboxes = tf.constant(_INVALID_BOX)
    bboxes = tf.cond(tf.equal(tf.size(bboxes), 0), lambda : tf.constant(_INVALID_BOX), lambda : bboxes)
    bboxes = tf.ensure_shape(bboxes, (None, 4))
    wrapped_aug_func = lambda _image, bbox, _new_bboxes: _apply_bbox_augmentation_wrapper(_image, bbox, _new_bboxes, prob, aug_func, func_changes_bbox, *args)
    num_bboxes = tf.shape(bboxes)[0]
    idx = tf.constant(0)
    cond = lambda _idx, _images_and_bboxes: tf.less(_idx, num_bboxes)
    if not func_changes_bbox:
        loop_bboxes = tf.random.shuffle(bboxes)
    else:
        loop_bboxes = bboxes
    body = lambda _idx, _images_and_bboxes: [
     _idx + 1,
     wrapped_aug_func(_images_and_bboxes[0], loop_bboxes[_idx], _images_and_bboxes[1])]
    _, (image, new_bboxes) = tf.while_loop(cond,
      body, [idx, (image, new_bboxes)], shape_invariants=[
     idx.get_shape(),
     (
      image.get_shape(), tf.TensorShape([None, 4]))])
    if func_changes_bbox:
        final_bboxes = new_bboxes
    else:
        final_bboxes = bboxes
    return (
     image, final_bboxes)


def _apply_multi_bbox_augmentation_wrapper(image, bboxes, prob, aug_func, func_changes_bbox, *args):
    """Checks to be sure num bboxes > 0 before calling inner function."""
    num_bboxes = tf.shape(bboxes)[0]
    image, bboxes = tf.cond(tf.equal(num_bboxes, 0), lambda : (
     image, bboxes), lambda : _apply_multi_bbox_augmentation(image, bboxes, prob, aug_func, func_changes_bbox, *args))
    return (
     image, bboxes)


def rotate_only_bboxes(image, bboxes, prob, degrees, replace):
    """Apply rotate to each bbox in the image with probability prob."""
    func_changes_bbox = False
    prob = _scale_bbox_only_op_probability(prob)
    return _apply_multi_bbox_augmentation_wrapper(image, bboxes, prob, rotate, func_changes_bbox, degrees, replace)


def shear_x_only_bboxes(image, bboxes, prob, level, replace):
    """Apply shear_x to each bbox in the image with probability prob."""
    func_changes_bbox = False
    prob = _scale_bbox_only_op_probability(prob)
    return _apply_multi_bbox_augmentation_wrapper(image, bboxes, prob, shear_x, func_changes_bbox, level, replace)


def shear_y_only_bboxes(image, bboxes, prob, level, replace):
    """Apply shear_y to each bbox in the image with probability prob."""
    func_changes_bbox = False
    prob = _scale_bbox_only_op_probability(prob)
    return _apply_multi_bbox_augmentation_wrapper(image, bboxes, prob, shear_y, func_changes_bbox, level, replace)


def translate_x_only_bboxes(image, bboxes, prob, pixels, replace):
    """Apply translate_x to each bbox in the image with probability prob."""
    func_changes_bbox = False
    prob = _scale_bbox_only_op_probability(prob)
    return _apply_multi_bbox_augmentation_wrapper(image, bboxes, prob, translate_x, func_changes_bbox, pixels, replace)


def translate_y_only_bboxes(image, bboxes, prob, pixels, replace):
    """Apply translate_y to each bbox in the image with probability prob."""
    func_changes_bbox = False
    prob = _scale_bbox_only_op_probability(prob)
    return _apply_multi_bbox_augmentation_wrapper(image, bboxes, prob, translate_y, func_changes_bbox, pixels, replace)


def flip_only_bboxes(image, bboxes, prob):
    """Apply flip_lr to each bbox in the image with probability prob."""
    func_changes_bbox = False
    prob = _scale_bbox_only_op_probability(prob)
    return _apply_multi_bbox_augmentation_wrapper(image, bboxes, prob, tf.image.flip_left_right, func_changes_bbox)


def solarize_only_bboxes(image, bboxes, prob, threshold):
    """Apply solarize to each bbox in the image with probability prob."""
    func_changes_bbox = False
    prob = _scale_bbox_only_op_probability(prob)
    return _apply_multi_bbox_augmentation_wrapper(image, bboxes, prob, solarize, func_changes_bbox, threshold)


def equalize_only_bboxes(image, bboxes, prob):
    """Apply equalize to each bbox in the image with probability prob."""
    func_changes_bbox = False
    prob = _scale_bbox_only_op_probability(prob)
    return _apply_multi_bbox_augmentation_wrapper(image, bboxes, prob, equalize, func_changes_bbox)


def cutout_only_bboxes(image, bboxes, prob, pad_size, replace):
    """Apply cutout to each bbox in the image with probability prob."""
    func_changes_bbox = False
    prob = _scale_bbox_only_op_probability(prob)
    return _apply_multi_bbox_augmentation_wrapper(image, bboxes, prob, cutout, func_changes_bbox, pad_size, replace)


def _rotate_bbox(bbox, image_height, image_width, degrees):
    """Rotates the bbox coordinated by degrees.

  Args:
    bbox: 1D Tensor that has 4 elements (min_y, min_x, max_y, max_x)
      of type float that represents the normalized coordinates between 0 and 1.
    image_height: Int, height of the image.
    image_width: Int, height of the image.
    degrees: Float, a scalar angle in degrees to rotate all images by. If
      degrees is positive the image will be rotated clockwise otherwise it will
      be rotated counterclockwise.

  Returns:
    A tensor of the same shape as bbox, but now with the rotated coordinates.
  """
    image_height, image_width = tf.to_float(image_height), tf.to_float(image_width)
    degrees_to_radians = math.pi / 180.0
    radians = degrees * degrees_to_radians
    min_y = -tf.to_int32(image_height * (bbox[0] - 0.5))
    min_x = tf.to_int32(image_width * (bbox[1] - 0.5))
    max_y = -tf.to_int32(image_height * (bbox[2] - 0.5))
    max_x = tf.to_int32(image_width * (bbox[3] - 0.5))
    coordinates = tf.stack([
     [
      min_y, min_x], [min_y, max_x], [max_y, min_x], [max_y, max_x]])
    coordinates = tf.cast(coordinates, tf.float32)
    rotation_matrix = tf.stack([
     [
      tf.cos(radians), tf.sin(radians)],
     [
      -tf.sin(radians), tf.cos(radians)]])
    new_coords = tf.cast(tf.matmul(rotation_matrix, tf.transpose(coordinates)), tf.int32)
    min_y = -(tf.to_float(tf.reduce_max(new_coords[0, :])) / image_height - 0.5)
    min_x = tf.to_float(tf.reduce_min(new_coords[1, :])) / image_width + 0.5
    max_y = -(tf.to_float(tf.reduce_min(new_coords[0, :])) / image_height - 0.5)
    max_x = tf.to_float(tf.reduce_max(new_coords[1, :])) / image_width + 0.5
    min_y, min_x, max_y, max_x = _clip_bbox(min_y, min_x, max_y, max_x)
    min_y, min_x, max_y, max_x = _check_bbox_area(min_y, min_x, max_y, max_x)
    return tf.stack([min_y, min_x, max_y, max_x])


def rotate_with_bboxes(image, bboxes, degrees, replace):
    """Equivalent of PIL Rotate that rotates the image and bbox.

  Args:
    image: 3D uint8 Tensor.
    bboxes: 2D Tensor that is a list of the bboxes in the image. Each bbox
      has 4 elements (min_y, min_x, max_y, max_x) of type float.
    degrees: Float, a scalar angle in degrees to rotate all images by. If
      degrees is positive the image will be rotated clockwise otherwise it will
      be rotated counterclockwise.
    replace: A one or three value 1D tensor to fill empty pixels.

  Returns:
    A tuple containing a 3D uint8 Tensor that will be the result of rotating
    image by degrees. The second element of the tuple is bboxes, where now
    the coordinates will be shifted to reflect the rotated image.
  """
    image = rotate(image, degrees, replace)
    image_height = tf.shape(image)[0]
    image_width = tf.shape(image)[1]
    wrapped_rotate_bbox = lambda bbox: _rotate_bbox(bbox, image_height, image_width, degrees)
    bboxes = tf.map_fn(wrapped_rotate_bbox, bboxes)
    return (image, bboxes)


def translate_x(image, pixels, replace):
    """Equivalent of PIL Translate in X dimension."""
    image = tf.contrib.image.translate(wrap(image), [-pixels, 0])
    return unwrap(image, replace)


def translate_y(image, pixels, replace):
    """Equivalent of PIL Translate in Y dimension."""
    image = tf.contrib.image.translate(wrap(image), [0, -pixels])
    return unwrap(image, replace)


def _shift_bbox(bbox, image_height, image_width, pixels, shift_horizontal):
    """Shifts the bbox coordinates by pixels.

  Args:
    bbox: 1D Tensor that has 4 elements (min_y, min_x, max_y, max_x)
      of type float that represents the normalized coordinates between 0 and 1.
    image_height: Int, height of the image.
    image_width: Int, width of the image.
    pixels: An int. How many pixels to shift the bbox.
    shift_horizontal: Boolean. If true then shift in X dimension else shift in
      Y dimension.

  Returns:
    A tensor of the same shape as bbox, but now with the shifted coordinates.
  """
    pixels = tf.to_int32(pixels)
    min_y = tf.to_int32(tf.to_float(image_height) * bbox[0])
    min_x = tf.to_int32(tf.to_float(image_width) * bbox[1])
    max_y = tf.to_int32(tf.to_float(image_height) * bbox[2])
    max_x = tf.to_int32(tf.to_float(image_width) * bbox[3])
    if shift_horizontal:
        min_x = tf.maximum(0, min_x - pixels)
        max_x = tf.minimum(image_width, max_x - pixels)
    else:
        min_y = tf.maximum(0, min_y - pixels)
        max_y = tf.minimum(image_height, max_y - pixels)
    min_y = tf.to_float(min_y) / tf.to_float(image_height)
    min_x = tf.to_float(min_x) / tf.to_float(image_width)
    max_y = tf.to_float(max_y) / tf.to_float(image_height)
    max_x = tf.to_float(max_x) / tf.to_float(image_width)
    min_y, min_x, max_y, max_x = _clip_bbox(min_y, min_x, max_y, max_x)
    min_y, min_x, max_y, max_x = _check_bbox_area(min_y, min_x, max_y, max_x)
    return tf.stack([min_y, min_x, max_y, max_x])


def translate_bbox(image, bboxes, pixels, replace, shift_horizontal):
    """Equivalent of PIL Translate in X/Y dimension that shifts image and bbox.

  Args:
    image: 3D uint8 Tensor.
    bboxes: 2D Tensor that is a list of the bboxes in the image. Each bbox
      has 4 elements (min_y, min_x, max_y, max_x) of type float with values
      between [0, 1].
    pixels: An int. How many pixels to shift the image and bboxes
    replace: A one or three value 1D tensor to fill empty pixels.
    shift_horizontal: Boolean. If true then shift in X dimension else shift in
      Y dimension.

  Returns:
    A tuple containing a 3D uint8 Tensor that will be the result of translating
    image by pixels. The second element of the tuple is bboxes, where now
    the coordinates will be shifted to reflect the shifted image.
  """
    if shift_horizontal:
        image = translate_x(image, pixels, replace)
    else:
        image = translate_y(image, pixels, replace)
    image_height = tf.shape(image)[0]
    image_width = tf.shape(image)[1]
    wrapped_shift_bbox = lambda bbox: _shift_bbox(bbox, image_height, image_width, pixels, shift_horizontal)
    bboxes = tf.map_fn(wrapped_shift_bbox, bboxes)
    return (image, bboxes)


def shear_x(image, level, replace):
    """Equivalent of PIL Shearing in X dimension."""
    image = tf.contrib.image.transform(wrap(image), [1.0, level, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0])
    return unwrap(image, replace)


def shear_y(image, level, replace):
    """Equivalent of PIL Shearing in Y dimension."""
    image = tf.contrib.image.transform(wrap(image), [1.0, 0.0, 0.0, level, 1.0, 0.0, 0.0, 0.0])
    return unwrap(image, replace)


def _shear_bbox(bbox, image_height, image_width, level, shear_horizontal):
    """Shifts the bbox according to how the image was sheared.

  Args:
    bbox: 1D Tensor that has 4 elements (min_y, min_x, max_y, max_x)
      of type float that represents the normalized coordinates between 0 and 1.
    image_height: Int, height of the image.
    image_width: Int, height of the image.
    level: Float. How much to shear the image.
    shear_horizontal: If true then shear in X dimension else shear in
      the Y dimension.

  Returns:
    A tensor of the same shape as bbox, but now with the shifted coordinates.
  """
    image_height, image_width = tf.to_float(image_height), tf.to_float(image_width)
    min_y = tf.to_int32(image_height * bbox[0])
    min_x = tf.to_int32(image_width * bbox[1])
    max_y = tf.to_int32(image_height * bbox[2])
    max_x = tf.to_int32(image_width * bbox[3])
    coordinates = tf.stack([
     [
      min_y, min_x], [min_y, max_x], [max_y, min_x], [max_y, max_x]])
    coordinates = tf.cast(coordinates, tf.float32)
    if shear_horizontal:
        translation_matrix = tf.stack([
         [
          1, 0], [-level, 1]])
    else:
        translation_matrix = tf.stack([
         [
          1, -level], [0, 1]])
    translation_matrix = tf.cast(translation_matrix, tf.float32)
    new_coords = tf.cast(tf.matmul(translation_matrix, tf.transpose(coordinates)), tf.int32)
    min_y = tf.to_float(tf.reduce_min(new_coords[0, :])) / image_height
    min_x = tf.to_float(tf.reduce_min(new_coords[1, :])) / image_width
    max_y = tf.to_float(tf.reduce_max(new_coords[0, :])) / image_height
    max_x = tf.to_float(tf.reduce_max(new_coords[1, :])) / image_width
    min_y, min_x, max_y, max_x = _clip_bbox(min_y, min_x, max_y, max_x)
    min_y, min_x, max_y, max_x = _check_bbox_area(min_y, min_x, max_y, max_x)
    return tf.stack([min_y, min_x, max_y, max_x])


def shear_with_bboxes(image, bboxes, level, replace, shear_horizontal):
    """Applies Shear Transformation to the image and shifts the bboxes.

  Args:
    image: 3D uint8 Tensor.
    bboxes: 2D Tensor that is a list of the bboxes in the image. Each bbox
      has 4 elements (min_y, min_x, max_y, max_x) of type float with values
      between [0, 1].
    level: Float. How much to shear the image. This value will be between
      -0.3 to 0.3.
    replace: A one or three value 1D tensor to fill empty pixels.
    shear_horizontal: Boolean. If true then shear in X dimension else shear in
      the Y dimension.

  Returns:
    A tuple containing a 3D uint8 Tensor that will be the result of shearing
    image by level. The second element of the tuple is bboxes, where now
    the coordinates will be shifted to reflect the sheared image.
  """
    if shear_horizontal:
        image = shear_x(image, level, replace)
    else:
        image = shear_y(image, level, replace)
    image_height = tf.shape(image)[0]
    image_width = tf.shape(image)[1]
    wrapped_shear_bbox = lambda bbox: _shear_bbox(bbox, image_height, image_width, level, shear_horizontal)
    bboxes = tf.map_fn(wrapped_shear_bbox, bboxes)
    return (image, bboxes)


def autocontrast(image):
    """Implements Autocontrast function from PIL using TF ops.

  Args:
    image: A 3D uint8 tensor.

  Returns:
    The image after it has had autocontrast applied to it and will be of type
    uint8.
  """

    def scale_channel(image):
        """Scale the 2D image using the autocontrast rule."""
        lo = tf.to_float(tf.reduce_min(image))
        hi = tf.to_float(tf.reduce_max(image))

        def scale_values(im):
            scale = 255.0 / (hi - lo)
            offset = -lo * scale
            im = tf.to_float(im) * scale + offset
            im = tf.clip_by_value(im, 0.0, 255.0)
            return tf.cast(im, tf.uint8)

        result = tf.cond(hi > lo, lambda : scale_values(image), lambda : image)
        return result

    s1 = scale_channel(image[:, :, 0])
    s2 = scale_channel(image[:, :, 1])
    s3 = scale_channel(image[:, :, 2])
    image = tf.stack([s1, s2, s3], 2)
    return image


def sharpness(image, factor):
    """Implements Sharpness function from PIL using TF ops."""
    orig_image = image
    image = tf.cast(image, tf.float32)
    image = tf.expand_dims(image, 0)
    kernel = tf.constant([
     [
      1, 1, 1], [1, 5, 1], [1, 1, 1]],
      dtype=(tf.float32), shape=[
     3, 3, 1, 1]) / 13.0
    kernel = tf.tile(kernel, [1, 1, 3, 1])
    strides = [1, 1, 1, 1]
    degenerate = tf.nn.depthwise_conv2d(image,
      kernel, strides, padding='VALID', rate=[1, 1])
    degenerate = tf.clip_by_value(degenerate, 0.0, 255.0)
    degenerate = tf.squeeze(tf.cast(degenerate, tf.uint8), [0])
    mask = tf.ones_like(degenerate)
    padded_mask = tf.pad(mask, [[1, 1], [1, 1], [0, 0]])
    padded_degenerate = tf.pad(degenerate, [[1, 1], [1, 1], [0, 0]])
    result = tf.where(tf.equal(padded_mask, 1), padded_degenerate, orig_image)
    return blend(result, orig_image, factor)


def equalize(image):
    """Implements Equalize function from PIL using TF ops."""

    def scale_channel(im, c):
        """Scale the data in the channel to implement equalize."""
        im = tf.cast(im[:, :, c], tf.int32)
        histo = tf.histogram_fixed_width(im, [0, 255], nbins=256)
        nonzero = tf.where(tf.not_equal(histo, 0))
        nonzero_histo = tf.reshape(tf.gather(histo, nonzero), [-1])
        step = (tf.reduce_sum(nonzero_histo) - nonzero_histo[(-1)]) // 255

        def build_lut(histo, step):
            lut = (tf.cumsum(histo) + step // 2) // step
            lut = tf.concat([[0], lut[:-1]], 0)
            return tf.clip_by_value(lut, 0, 255)

        result = tf.cond(tf.equal(step, 0), lambda : im, lambda : tf.gather(build_lut(histo, step), im))
        return tf.cast(result, tf.uint8)

    s1 = scale_channel(image, 0)
    s2 = scale_channel(image, 1)
    s3 = scale_channel(image, 2)
    image = tf.stack([s1, s2, s3], 2)
    return image


def wrap(image):
    """Returns 'image' with an extra channel set to all 1s."""
    shape = tf.shape(image)
    extended_channel = tf.ones([shape[0], shape[1], 1], image.dtype)
    extended = tf.concat([image, extended_channel], 2)
    return extended


def unwrap(image, replace):
    """Unwraps an image produced by wrap.

  Where there is a 0 in the last channel for every spatial position,
  the rest of the three channels in that spatial dimension are grayed
  (set to 128).  Operations like translate and shear on a wrapped
  Tensor will leave 0s in empty locations.  Some transformations look
  at the intensity of values to do preprocessing, and we want these
  empty pixels to assume the 'average' value, rather than pure black.

  Args:
    image: A 3D Image Tensor with 4 channels.
    replace: A one or three value 1D tensor to fill empty pixels.

  Returns:
    image: A 3D image Tensor with 3 channels.
  """
    image_shape = tf.shape(image)
    flattened_image = tf.reshape(image, [-1, image_shape[2]])
    alpha_channel = flattened_image[:, 3]
    replace = tf.concat([replace, tf.ones([1], image.dtype)], 0)
    flattened_image = tf.where(tf.equal(alpha_channel, 0), tf.ones_like(flattened_image, dtype=(image.dtype)) * replace, flattened_image)
    image = tf.reshape(flattened_image, image_shape)
    image = tf.slice(image, [0, 0, 0], [image_shape[0], image_shape[1], 3])
    return image


def _cutout_inside_bbox(image, bbox, pad_fraction):
    """Generates cutout mask and the mean pixel value of the bbox.

  First a location is randomly chosen within the image as the center where the
  cutout mask will be applied. Note this can be towards the boundaries of the
  image, so the full cutout mask may not be applied.

  Args:
    image: 3D uint8 Tensor.
    bbox: 1D Tensor that has 4 elements (min_y, min_x, max_y, max_x)
      of type float that represents the normalized coordinates between 0 and 1.
    pad_fraction: Float that specifies how large the cutout mask should be in
      in reference to the size of the original bbox. If pad_fraction is 0.25,
      then the cutout mask will be of shape
      (0.25 * bbox height, 0.25 * bbox width).

  Returns:
    A tuple. Fist element is a tensor of the same shape as image where each
    element is either a 1 or 0 that is used to determine where the image
    will have cutout applied. The second element is the mean of the pixels
    in the image where the bbox is located.
  """
    image_height = tf.shape(image)[0]
    image_width = tf.shape(image)[1]
    bbox = tf.squeeze(bbox)
    min_y = tf.to_int32(tf.to_float(image_height) * bbox[0])
    min_x = tf.to_int32(tf.to_float(image_width) * bbox[1])
    max_y = tf.to_int32(tf.to_float(image_height) * bbox[2])
    max_x = tf.to_int32(tf.to_float(image_width) * bbox[3])
    mean = tf.reduce_mean((image[min_y:max_y + 1, min_x:max_x + 1]), reduction_indices=[
     0, 1])
    box_height = max_y - min_y + 1
    box_width = max_x - min_x + 1
    pad_size_height = tf.to_int32(pad_fraction * (box_height / 2))
    pad_size_width = tf.to_int32(pad_fraction * (box_width / 2))
    cutout_center_height = tf.random_uniform(shape=[], minval=min_y, maxval=(max_y + 1), dtype=(tf.int32))
    cutout_center_width = tf.random_uniform(shape=[], minval=min_x, maxval=(max_x + 1), dtype=(tf.int32))
    lower_pad = tf.maximum(0, cutout_center_height - pad_size_height)
    upper_pad = tf.maximum(0, image_height - cutout_center_height - pad_size_height)
    left_pad = tf.maximum(0, cutout_center_width - pad_size_width)
    right_pad = tf.maximum(0, image_width - cutout_center_width - pad_size_width)
    cutout_shape = [
     image_height - (lower_pad + upper_pad),
     image_width - (left_pad + right_pad)]
    padding_dims = [[lower_pad, upper_pad], [left_pad, right_pad]]
    mask = tf.pad(tf.zeros(cutout_shape, dtype=(image.dtype)),
      padding_dims,
      constant_values=1)
    mask = tf.expand_dims(mask, 2)
    mask = tf.tile(mask, [1, 1, 3])
    return (
     mask, mean)


def bbox_cutout(image, bboxes, pad_fraction, replace_with_mean):
    """Applies cutout to the image according to bbox information.

  This is a cutout variant that using bbox information to make more informed
  decisions on where to place the cutout mask.

  Args:
    image: 3D uint8 Tensor.
    bboxes: 2D Tensor that is a list of the bboxes in the image. Each bbox
      has 4 elements (min_y, min_x, max_y, max_x) of type float with values
      between [0, 1].
    pad_fraction: Float that specifies how large the cutout mask should be in
      in reference to the size of the original bbox. If pad_fraction is 0.25,
      then the cutout mask will be of shape
      (0.25 * bbox height, 0.25 * bbox width).
    replace_with_mean: Boolean that specified what value should be filled in
      where the cutout mask is applied. Since the incoming image will be of
      uint8 and will not have had any mean normalization applied, by default
      we set the value to be 128. If replace_with_mean is True then we find
      the mean pixel values across the channel dimension and use those to fill
      in where the cutout mask is applied.

  Returns:
    A tuple. First element is a tensor of the same shape as image that has
    cutout applied to it. Second element is the bboxes that were passed in
    that will be unchanged.
  """

    def apply_bbox_cutout(image, bboxes, pad_fraction):
        random_index = tf.random_uniform(shape=[], maxval=(tf.shape(bboxes)[0]), dtype=(tf.int32))
        chosen_bbox = tf.gather(bboxes, random_index)
        mask, mean = _cutout_inside_bbox(image, chosen_bbox, pad_fraction)
        replace = mean if replace_with_mean else 128
        image = tf.where(tf.equal(mask, 0), tf.cast((tf.ones_like(image, dtype=(image.dtype)) * replace), dtype=(image.dtype)), image)
        return image

    image = tf.cond(tf.equal(tf.size(bboxes), 0), lambda : image, lambda : apply_bbox_cutout(image, bboxes, pad_fraction))
    return (
     image, bboxes)


NAME_TO_FUNC = {'AutoContrast':autocontrast, 
 'Equalize':equalize, 
 'Posterize':posterize, 
 'Solarize':solarize, 
 'SolarizeAdd':solarize_add, 
 'Color':color, 
 'Contrast':contrast, 
 'Brightness':brightness, 
 'Sharpness':sharpness, 
 'Cutout':cutout, 
 'BBox_Cutout':bbox_cutout, 
 'Rotate_BBox':rotate_with_bboxes, 
 'TranslateX_BBox':lambda image, bboxes, pixels, replace: translate_bbox(image,
   bboxes, pixels, replace, shift_horizontal=True), 
 'TranslateY_BBox':lambda image, bboxes, pixels, replace: translate_bbox(image,
   bboxes, pixels, replace, shift_horizontal=False), 
 'ShearX_BBox':lambda image, bboxes, level, replace: shear_with_bboxes(image,
   bboxes, level, replace, shear_horizontal=True), 
 'ShearY_BBox':lambda image, bboxes, level, replace: shear_with_bboxes(image,
   bboxes, level, replace, shear_horizontal=False), 
 'Rotate_Only_BBoxes':rotate_only_bboxes, 
 'ShearX_Only_BBoxes':shear_x_only_bboxes, 
 'ShearY_Only_BBoxes':shear_y_only_bboxes, 
 'TranslateX_Only_BBoxes':translate_x_only_bboxes, 
 'TranslateY_Only_BBoxes':translate_y_only_bboxes, 
 'Flip_Only_BBoxes':flip_only_bboxes, 
 'Solarize_Only_BBoxes':solarize_only_bboxes, 
 'Equalize_Only_BBoxes':equalize_only_bboxes, 
 'Cutout_Only_BBoxes':cutout_only_bboxes}

def _randomly_negate_tensor(tensor):
    """With 50% prob turn the tensor negative."""
    should_flip = tf.cast(tf.floor(tf.random_uniform([]) + 0.5), tf.bool)
    final_tensor = tf.cond(should_flip, lambda : tensor, lambda : -tensor)
    return final_tensor


def _rotate_level_to_arg(level):
    level = level / _MAX_LEVEL * 30.0
    level = _randomly_negate_tensor(level)
    return (level,)


def _shrink_level_to_arg(level):
    """Converts level to ratio by which we shrink the image content."""
    if level == 0:
        return (1.0, )
    level = 2.0 / (_MAX_LEVEL / level) + 0.9
    return (level,)


def _enhance_level_to_arg(level):
    return (
     level / _MAX_LEVEL * 1.8 + 0.1,)


def _shear_level_to_arg(level):
    level = level / _MAX_LEVEL * 0.3
    level = _randomly_negate_tensor(level)
    return (level,)


def _translate_level_to_arg(level, translate_const):
    level = level / _MAX_LEVEL * float(translate_const)
    level = _randomly_negate_tensor(level)
    return (level,)


def _bbox_cutout_level_to_arg(level, hparams):
    cutout_pad_fraction = level / _MAX_LEVEL * hparams.cutout_max_pad_fraction
    return (cutout_pad_fraction,
     hparams.cutout_bbox_replace_with_mean)


def level_to_arg(hparams):
    return {'AutoContrast':lambda level: (), 
     'Equalize':lambda level: (), 
     'Posterize':lambda level: (
      int(level / _MAX_LEVEL * 4),), 
     'Solarize':lambda level: (
      int(level / _MAX_LEVEL * 256),), 
     'SolarizeAdd':lambda level: (
      int(level / _MAX_LEVEL * 110),), 
     'Color':_enhance_level_to_arg, 
     'Contrast':_enhance_level_to_arg, 
     'Brightness':_enhance_level_to_arg, 
     'Sharpness':_enhance_level_to_arg, 
     'Cutout':lambda level: (
      int(level / _MAX_LEVEL * hparams.cutout_const),), 
     'BBox_Cutout':lambda level: _bbox_cutout_level_to_arg(level, hparams), 
     'TranslateX_BBox':lambda level: _translate_level_to_arg(level, hparams.translate_const), 
     'TranslateY_BBox':lambda level: _translate_level_to_arg(level, hparams.translate_const), 
     'ShearX_BBox':_shear_level_to_arg, 
     'ShearY_BBox':_shear_level_to_arg, 
     'Rotate_BBox':_rotate_level_to_arg, 
     'Rotate_Only_BBoxes':_rotate_level_to_arg, 
     'ShearX_Only_BBoxes':_shear_level_to_arg, 
     'ShearY_Only_BBoxes':_shear_level_to_arg, 
     'TranslateX_Only_BBoxes':lambda level: _translate_level_to_arg(level, hparams.translate_bbox_const), 
     'TranslateY_Only_BBoxes':lambda level: _translate_level_to_arg(level, hparams.translate_bbox_const), 
     'Flip_Only_BBoxes':lambda level: (), 
     'Solarize_Only_BBoxes':lambda level: (
      int(level / _MAX_LEVEL * 256),), 
     'Equalize_Only_BBoxes':lambda level: (), 
     'Cutout_Only_BBoxes':lambda level: (
      int(level / _MAX_LEVEL * hparams.cutout_bbox_const),)}


def bbox_wrapper(func):
    """Adds a bboxes function argument to func and returns unchanged bboxes."""

    def wrapper(images, bboxes, *args, **kwargs):
        return (
         func(images, *args, **kwargs), bboxes)

    return wrapper


def _parse_policy_info(name, prob, level, replace_value, augmentation_hparams):
    """Return the function that corresponds to `name` and update `level` param."""
    func = NAME_TO_FUNC[name]
    args = level_to_arg(augmentation_hparams)[name](level)
    if six.PY2:
        arg_spec = inspect.getargspec(func)
    else:
        arg_spec = inspect.getfullargspec(func)
    if 'prob' in arg_spec[0]:
        args = tuple([prob] + list(args))
    if 'replace' in arg_spec[0]:
        assert 'replace' == arg_spec[0][(-1)]
        args = tuple(list(args) + [replace_value])
    if 'bboxes' not in arg_spec[0]:
        func = bbox_wrapper(func)
    return (
     func, prob, args)


def _apply_func_with_prob(func, image, args, prob, bboxes):
    """Apply `func` to image w/ `args` as input with probability `prob`."""
    if not isinstance(args, tuple):
        raise AssertionError
    elif six.PY2:
        arg_spec = inspect.getargspec(func)
    else:
        arg_spec = inspect.getfullargspec(func)
    assert 'bboxes' == arg_spec[0][1]
    if 'prob' in arg_spec[0]:
        prob = 1.0
    should_apply_op = tf.cast(tf.floor(tf.random_uniform([], dtype=(tf.float32)) + prob), tf.bool)
    augmented_image, augmented_bboxes = tf.cond(should_apply_op, lambda : func(image, bboxes, *args), lambda : (
     image, bboxes))
    return (augmented_image, augmented_bboxes)


def select_and_apply_random_policy--- This code section failed: ---

 L.1541         0  LOAD_GLOBAL              tf
                2  LOAD_ATTR                random_uniform
                4  BUILD_LIST_0          0 
                6  LOAD_GLOBAL              len
                8  LOAD_FAST                'policies'
               10  CALL_FUNCTION_1       1  '1 positional argument'
               12  LOAD_GLOBAL              tf
               14  LOAD_ATTR                int32
               16  LOAD_CONST               ('maxval', 'dtype')
               18  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               20  STORE_FAST               'policy_to_select'

 L.1544        22  SETUP_LOOP           94  'to 94'
               24  LOAD_GLOBAL              enumerate
               26  LOAD_FAST                'policies'
               28  CALL_FUNCTION_1       1  '1 positional argument'
               30  GET_ITER         
               32  FOR_ITER             92  'to 92'
               34  UNPACK_SEQUENCE_2     2 
               36  STORE_FAST               'i'
               38  STORE_FAST               'policy'

 L.1545        40  LOAD_GLOBAL              tf
               42  LOAD_METHOD              cond

 L.1546        44  LOAD_GLOBAL              tf
               46  LOAD_METHOD              equal
               48  LOAD_FAST                'i'
               50  LOAD_FAST                'policy_to_select'
               52  CALL_METHOD_2         2  '2 positional arguments'

 L.1547        54  LOAD_FAST                'policy'
               56  BUILD_TUPLE_1         1 
               58  LOAD_CLOSURE             'bboxes'
               60  LOAD_CLOSURE             'image'
               62  BUILD_TUPLE_2         2 
               64  LOAD_LAMBDA              '<code_object <lambda>>'
               66  LOAD_STR                 'select_and_apply_random_policy.<locals>.<lambda>'
               68  MAKE_FUNCTION_9          'default, closure'

 L.1548        70  LOAD_CLOSURE             'bboxes'
               72  LOAD_CLOSURE             'image'
               74  BUILD_TUPLE_2         2 
               76  LOAD_LAMBDA              '<code_object <lambda>>'
               78  LOAD_STR                 'select_and_apply_random_policy.<locals>.<lambda>'
               80  MAKE_FUNCTION_8          'closure'
               82  CALL_METHOD_3         3  '3 positional arguments'
               84  UNPACK_SEQUENCE_2     2 
               86  STORE_DEREF              'image'
               88  STORE_DEREF              'bboxes'
               90  JUMP_BACK            32  'to 32'
               92  POP_BLOCK        
             94_0  COME_FROM_LOOP       22  '22'

 L.1549        94  LOAD_DEREF               'image'
               96  LOAD_DEREF               'bboxes'
               98  BUILD_TUPLE_2         2 
              100  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `MAKE_FUNCTION_9' instruction at offset 68


def build_and_apply_nas_policy(policies, image, bboxes, augmentation_hparams):
    """Build a policy from the given policies passed in and apply to image.

  Args:
    policies: list of lists of tuples in the form `(func, prob, level)`, `func`
      is a string name of the augmentation function, `prob` is the probability
      of applying the `func` operation, `level` is the input argument for
      `func`.
    image: tf.Tensor that the resulting policy will be applied to.
    bboxes:
    augmentation_hparams: Hparams associated with the NAS learned policy.

  Returns:
    A version of image that now has data augmentation applied to it based on
    the `policies` pass into the function. Additionally, returns bboxes if
    a value for them is passed in that is not None
  """
    replace_value = [
     128, 128, 128]
    tf_policies = []
    for policy in policies:
        tf_policy = []
        for policy_info in policy:
            policy_info = list(policy_info) + [replace_value, augmentation_hparams]
            tf_policy.append(_parse_policy_info(*policy_info))

        def make_final_policy(tf_policy_):

            def final_policy(image_, bboxes_):
                for func, prob, args in tf_policy_:
                    image_, bboxes_ = _apply_func_with_prob(func, image_, args, prob, bboxes_)

                return (
                 image_, bboxes_)

            return final_policy

        tf_policies.append(make_final_policy(tf_policy))

    augmented_image, augmented_bbox = select_and_apply_random_policy(tf_policies, image, bboxes)
    return (
     augmented_image, augmented_bbox)


def distort_image_with_autoaugment(image, bboxes, augmentation_name):
    """Applies the AutoAugment policy to `image` and `bboxes`.

  Args:
    image: `Tensor` of shape [height, width, 3] representing an image.
    bboxes: `Tensor` of shape [N, 4] representing ground truth boxes that are
      normalized between [0, 1].
    augmentation_name: The name of the AutoAugment policy to use. The available
      options are `v0`, `v1`, `v2`, `v3` and `test`. `v0` is the policy used for
      all of the results in the paper and was found to achieve the best results
      on the COCO dataset. `v1`, `v2` and `v3` are additional good policies
      found on the COCO dataset that have slight variation in what operations
      were used during the search procedure along with how many operations are
      applied in parallel to a single image (2 vs 3).

  Returns:
    A tuple containing the augmented versions of `image` and `bboxes`.
  """
    image = tf.cast(image, tf.uint8)
    available_policies = {'v0':policy_v0,  'v1':policy_v1,  'v2':policy_v2,  'v3':policy_v3, 
     'test':policy_vtest}
    if augmentation_name not in available_policies:
        raise ValueError('Invalid augmentation_name: {}'.format(augmentation_name))
    policy = available_policies[augmentation_name]()
    augmentation_hparams = tf.contrib.training.HParams(cutout_max_pad_fraction=0.75,
      cutout_bbox_replace_with_mean=False,
      cutout_const=100,
      translate_const=250,
      cutout_bbox_const=50,
      translate_bbox_const=120)
    augmented_image, augmented_bbox = build_and_apply_nas_policy(policy, image, bboxes, augmentation_hparams)
    augmented_image = tf.cast(augmented_image, tf.float32)
    return (augmented_image, augmented_bbox)