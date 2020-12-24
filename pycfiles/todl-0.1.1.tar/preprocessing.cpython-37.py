# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/svpino/dev/tensorflow-object-detection-sagemaker/todl/tensorflow-object-detection/research/tcn/preprocessing.py
# Compiled at: 2020-04-05 19:50:58
# Size of source mod 2**32: 26422 bytes
"""Image preprocessing helpers."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import cv2
from scipy import ndimage
import tensorflow as tf
from tensorflow.python.ops import control_flow_ops

def apply_with_random_selector(x, func, num_cases):
    """Computes func(x, sel), with sel sampled from [0...num_cases-1].

  TODO(coreylynch): add as a dependency, when slim or tensorflow/models are
  pipfied.
  Source:
  https://raw.githubusercontent.com/tensorflow/models/a9d0e6e8923a4/slim/preprocessing/inception_preprocessing.py

  Args:
    x: input Tensor.
    func: Python function to apply.
    num_cases: Python int32, number of cases to sample sel from.
  Returns:
    The result of func(x, sel), where func receives the value of the
    selector as a python integer, but sel is sampled dynamically.
  """
    sel = tf.random_uniform([], maxval=num_cases, dtype=(tf.int32))
    return control_flow_ops.merge([func(control_flow_ops.switch(x, tf.equal(sel, case))[1], case) for case in range(num_cases)])[0]


def distorted_bounding_box_crop(image, bbox, min_object_covered=0.1, aspect_ratio_range=(0.75, 1.33), area_range=(0.05, 1.0), max_attempts=100, scope=None):
    """Generates cropped_image using a one of the bboxes randomly distorted.

  TODO(coreylynch): add as a dependency, when slim or tensorflow/models are
  pipfied.
  Source:
  https://raw.githubusercontent.com/tensorflow/models/a9d0e6e8923a4/slim/preprocessing/inception_preprocessing.py

  See `tf.image.sample_distorted_bounding_box` for more documentation.

  Args:
    image: 3-D Tensor of image (it will be converted to floats in [0, 1]).
    bbox: 3-D float Tensor of bounding boxes arranged [1, num_boxes, coords]
      where each coordinate is [0, 1) and the coordinates are arranged
      as [ymin, xmin, ymax, xmax]. If num_boxes is 0 then it would use the whole
      image.
    min_object_covered: An optional `float`. Defaults to `0.1`. The cropped
      area of the image must contain at least this fraction of any bounding box
      supplied.
    aspect_ratio_range: An optional list of `floats`. The cropped area of the
      image must have an aspect ratio = width / height within this range.
    area_range: An optional list of `floats`. The cropped area of the image
      must contain a fraction of the supplied image within in this range.
    max_attempts: An optional `int`. Number of attempts at generating a cropped
      region of the image of the specified constraints. After `max_attempts`
      failures, return the entire image.
    scope: Optional scope for name_scope.
  Returns:
    A tuple, a 3-D Tensor cropped_image and the distorted bbox
  """
    with tf.name_scope(scope, 'distorted_bounding_box_crop', [image, bbox]):
        sample_distorted_bounding_box = tf.image.sample_distorted_bounding_box((tf.shape(image)),
          bounding_boxes=bbox,
          min_object_covered=min_object_covered,
          aspect_ratio_range=aspect_ratio_range,
          area_range=area_range,
          max_attempts=max_attempts,
          use_image_if_no_bounding_boxes=True)
        bbox_begin, bbox_size, distort_bbox = sample_distorted_bounding_box
        cropped_image = tf.slice(image, bbox_begin, bbox_size)
        return (cropped_image, distort_bbox)


def distort_color--- This code section failed: ---

 L. 135         0  LOAD_GLOBAL              tf
                2  LOAD_METHOD              name_scope
                4  LOAD_FAST                'scope'
                6  LOAD_STR                 'distort_color'
                8  LOAD_FAST                'image'
               10  BUILD_LIST_1          1 
               12  CALL_METHOD_3         3  '3 positional arguments'
            14_16  SETUP_WITH          446  'to 446'
               18  POP_TOP          

 L. 136        20  LOAD_FAST                'fast_mode'
               22  POP_JUMP_IF_FALSE   106  'to 106'

 L. 137        24  LOAD_FAST                'color_ordering'
               26  LOAD_CONST               0
               28  COMPARE_OP               ==
               30  POP_JUMP_IF_FALSE    68  'to 68'

 L. 138        32  LOAD_GLOBAL              tf
               34  LOAD_ATTR                image
               36  LOAD_ATTR                random_brightness
               38  LOAD_FAST                'image'
               40  LOAD_CONST               0.12549019607843137
               42  LOAD_CONST               ('max_delta',)
               44  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               46  STORE_FAST               'image'

 L. 139        48  LOAD_GLOBAL              tf
               50  LOAD_ATTR                image
               52  LOAD_ATTR                random_saturation
               54  LOAD_FAST                'image'
               56  LOAD_CONST               0.5
               58  LOAD_CONST               1.5
               60  LOAD_CONST               ('lower', 'upper')
               62  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               64  STORE_FAST               'image'
               66  JUMP_FORWARD        432  'to 432'
             68_0  COME_FROM            30  '30'

 L. 141        68  LOAD_GLOBAL              tf
               70  LOAD_ATTR                image
               72  LOAD_ATTR                random_saturation
               74  LOAD_FAST                'image'
               76  LOAD_CONST               0.5
               78  LOAD_CONST               1.5
               80  LOAD_CONST               ('lower', 'upper')
               82  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               84  STORE_FAST               'image'

 L. 142        86  LOAD_GLOBAL              tf
               88  LOAD_ATTR                image
               90  LOAD_ATTR                random_brightness
               92  LOAD_FAST                'image'
               94  LOAD_CONST               0.12549019607843137
               96  LOAD_CONST               ('max_delta',)
               98  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              100  STORE_FAST               'image'
          102_104  JUMP_FORWARD        432  'to 432'
            106_0  COME_FROM            22  '22'

 L. 144       106  LOAD_FAST                'color_ordering'
              108  LOAD_CONST               0
              110  COMPARE_OP               ==
              112  POP_JUMP_IF_FALSE   184  'to 184'

 L. 145       114  LOAD_GLOBAL              tf
              116  LOAD_ATTR                image
              118  LOAD_ATTR                random_brightness
              120  LOAD_FAST                'image'
              122  LOAD_CONST               0.12549019607843137
              124  LOAD_CONST               ('max_delta',)
              126  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              128  STORE_FAST               'image'

 L. 146       130  LOAD_GLOBAL              tf
              132  LOAD_ATTR                image
              134  LOAD_ATTR                random_saturation
              136  LOAD_FAST                'image'
              138  LOAD_CONST               0.5
              140  LOAD_CONST               1.5
              142  LOAD_CONST               ('lower', 'upper')
              144  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              146  STORE_FAST               'image'

 L. 147       148  LOAD_GLOBAL              tf
              150  LOAD_ATTR                image
              152  LOAD_ATTR                random_hue
              154  LOAD_FAST                'image'
              156  LOAD_CONST               0.2
              158  LOAD_CONST               ('max_delta',)
              160  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              162  STORE_FAST               'image'

 L. 148       164  LOAD_GLOBAL              tf
              166  LOAD_ATTR                image
              168  LOAD_ATTR                random_contrast
              170  LOAD_FAST                'image'
              172  LOAD_CONST               0.5
              174  LOAD_CONST               1.5
              176  LOAD_CONST               ('lower', 'upper')
              178  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              180  STORE_FAST               'image'
              182  JUMP_FORWARD        432  'to 432'
            184_0  COME_FROM           112  '112'

 L. 149       184  LOAD_FAST                'color_ordering'
              186  LOAD_CONST               1
              188  COMPARE_OP               ==
          190_192  POP_JUMP_IF_FALSE   264  'to 264'

 L. 150       194  LOAD_GLOBAL              tf
              196  LOAD_ATTR                image
              198  LOAD_ATTR                random_saturation
              200  LOAD_FAST                'image'
              202  LOAD_CONST               0.5
              204  LOAD_CONST               1.5
              206  LOAD_CONST               ('lower', 'upper')
              208  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              210  STORE_FAST               'image'

 L. 151       212  LOAD_GLOBAL              tf
              214  LOAD_ATTR                image
              216  LOAD_ATTR                random_brightness
              218  LOAD_FAST                'image'
              220  LOAD_CONST               0.12549019607843137
              222  LOAD_CONST               ('max_delta',)
              224  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              226  STORE_FAST               'image'

 L. 152       228  LOAD_GLOBAL              tf
              230  LOAD_ATTR                image
              232  LOAD_ATTR                random_contrast
              234  LOAD_FAST                'image'
              236  LOAD_CONST               0.5
              238  LOAD_CONST               1.5
              240  LOAD_CONST               ('lower', 'upper')
              242  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              244  STORE_FAST               'image'

 L. 153       246  LOAD_GLOBAL              tf
              248  LOAD_ATTR                image
              250  LOAD_ATTR                random_hue
              252  LOAD_FAST                'image'
              254  LOAD_CONST               0.2
              256  LOAD_CONST               ('max_delta',)
              258  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              260  STORE_FAST               'image'
              262  JUMP_FORWARD        432  'to 432'
            264_0  COME_FROM           190  '190'

 L. 154       264  LOAD_FAST                'color_ordering'
              266  LOAD_CONST               2
              268  COMPARE_OP               ==
          270_272  POP_JUMP_IF_FALSE   344  'to 344'

 L. 155       274  LOAD_GLOBAL              tf
              276  LOAD_ATTR                image
              278  LOAD_ATTR                random_contrast
              280  LOAD_FAST                'image'
              282  LOAD_CONST               0.5
              284  LOAD_CONST               1.5
              286  LOAD_CONST               ('lower', 'upper')
              288  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              290  STORE_FAST               'image'

 L. 156       292  LOAD_GLOBAL              tf
              294  LOAD_ATTR                image
              296  LOAD_ATTR                random_hue
              298  LOAD_FAST                'image'
              300  LOAD_CONST               0.2
              302  LOAD_CONST               ('max_delta',)
              304  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              306  STORE_FAST               'image'

 L. 157       308  LOAD_GLOBAL              tf
              310  LOAD_ATTR                image
              312  LOAD_ATTR                random_brightness
              314  LOAD_FAST                'image'
              316  LOAD_CONST               0.12549019607843137
              318  LOAD_CONST               ('max_delta',)
              320  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              322  STORE_FAST               'image'

 L. 158       324  LOAD_GLOBAL              tf
              326  LOAD_ATTR                image
              328  LOAD_ATTR                random_saturation
              330  LOAD_FAST                'image'
              332  LOAD_CONST               0.5
              334  LOAD_CONST               1.5
              336  LOAD_CONST               ('lower', 'upper')
              338  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              340  STORE_FAST               'image'
              342  JUMP_FORWARD        432  'to 432'
            344_0  COME_FROM           270  '270'

 L. 159       344  LOAD_FAST                'color_ordering'
              346  LOAD_CONST               3
              348  COMPARE_OP               ==
          350_352  POP_JUMP_IF_FALSE   424  'to 424'

 L. 160       354  LOAD_GLOBAL              tf
              356  LOAD_ATTR                image
              358  LOAD_ATTR                random_hue
              360  LOAD_FAST                'image'
              362  LOAD_CONST               0.2
              364  LOAD_CONST               ('max_delta',)
              366  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              368  STORE_FAST               'image'

 L. 161       370  LOAD_GLOBAL              tf
              372  LOAD_ATTR                image
              374  LOAD_ATTR                random_saturation
              376  LOAD_FAST                'image'
              378  LOAD_CONST               0.5
              380  LOAD_CONST               1.5
              382  LOAD_CONST               ('lower', 'upper')
              384  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              386  STORE_FAST               'image'

 L. 162       388  LOAD_GLOBAL              tf
              390  LOAD_ATTR                image
              392  LOAD_ATTR                random_contrast
            394_0  COME_FROM            66  '66'
              394  LOAD_FAST                'image'
              396  LOAD_CONST               0.5
              398  LOAD_CONST               1.5
              400  LOAD_CONST               ('lower', 'upper')
              402  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              404  STORE_FAST               'image'

 L. 163       406  LOAD_GLOBAL              tf
              408  LOAD_ATTR                image
              410  LOAD_ATTR                random_brightness
              412  LOAD_FAST                'image'
              414  LOAD_CONST               0.12549019607843137
              416  LOAD_CONST               ('max_delta',)
              418  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              420  STORE_FAST               'image'
              422  JUMP_FORWARD        432  'to 432'
            424_0  COME_FROM           350  '350'

 L. 165       424  LOAD_GLOBAL              ValueError
              426  LOAD_STR                 'color_ordering must be in [0, 3]'
              428  CALL_FUNCTION_1       1  '1 positional argument'
              430  RAISE_VARARGS_1       1  'exception instance'
            432_0  COME_FROM           422  '422'
            432_1  COME_FROM           342  '342'
            432_2  COME_FROM           262  '262'
            432_3  COME_FROM           182  '182'
            432_4  COME_FROM           102  '102'

 L. 168       432  LOAD_GLOBAL              tf
              434  LOAD_METHOD              clip_by_value
              436  LOAD_FAST                'image'
              438  LOAD_CONST               0.0
              440  LOAD_CONST               1.0
              442  CALL_METHOD_3         3  '3 positional arguments'
              444  RETURN_VALUE     
            446_0  COME_FROM_WITH       14  '14'
              446  WITH_CLEANUP_START
              448  WITH_CLEANUP_FINISH
              450  END_FINALLY      

Parse error at or near `COME_FROM' instruction at offset 394_0


def crop_center(image):
    """Returns a cropped square image."""
    shape = tf.shape(image)
    new_shape = tf.minimum(shape[0], shape[1])
    offset_y = tf.maximum(shape[0] - shape[1], 0) // 2
    offset_x = tf.maximum(shape[1] - shape[0], 0) // 2
    image = tf.image.crop_to_bounding_box(image, offset_y, offset_x, new_shape, new_shape)
    return image


def pad(image):
    """Returns an image padded to be square."""
    shape = tf.shape(image)
    new_shape = tf.maximum(shape[0], shape[1])
    height = shape[0]
    width = shape[1]
    offset_x = tf.maximum(height - width, 0) // 2
    offset_y = tf.maximum(width - height, 0) // 2
    image = tf.image.pad_to_bounding_box(image, offset_y, offset_x, new_shape, new_shape)
    return image


def pad_200(image):
    """Returns an image padded width-padded with 200 pixels."""
    shape = tf.shape(image)
    image = tf.image.pad_to_bounding_box(image, 0, 200, shape[0], shape[1] + 400)
    shape = tf.shape(image)
    new_shape = tf.minimum(shape[0], shape[1])
    offset_y = tf.maximum(shape[0] - shape[1], 0) // 2
    offset_x = tf.maximum(shape[1] - shape[0], 0) // 2
    image = tf.image.crop_to_bounding_box(image, offset_y, offset_x, new_shape, new_shape)
    return image


def pad_crop_central(image, central_fraction=0.875):
    """Pads the image to the maximum length, crops the central fraction."""
    image = pad(image)
    image = tf.image.central_crop(image, central_fraction=central_fraction)
    return image


def crop_image_by_strategy(image, cropping):
    """Crops an image according to a strategy defined in config.

  Args:
    image: 3-d image tensor.
    cropping: str, name of cropping strategy.
  Returns:
    image: cropped image.
  Raises:
    ValueError: When unknown cropping strategy is specified.
  """
    strategy_to_method = {'crop_center':crop_center, 
     'pad':pad, 
     'pad200':pad_200, 
     'pad_crop_central':pad_crop_central}
    tf.logging.info('Cropping strategy: %s.' % cropping)
    if cropping not in strategy_to_method:
        raise ValueError('Unknown cropping strategy: %s' % cropping)
    return strategy_to_method[cropping](image)


def scale_augment_crop(image, central_bbox, area_range, min_object_covered):
    """Training time scale augmentation.

  Args:
    image: 3-d float tensor.
    central_bbox: Bounding box defining the central region of interest.
    area_range: Range of allowed areas for the augmented bounding box.
    min_object_covered: Constraint for the fraction of original image in
      augmented bounding box.
  Returns:
    distort_image: The scaled, cropped image.
  """
    distorted_image, _ = distorted_bounding_box_crop(image,
      central_bbox, area_range=area_range, aspect_ratio_range=(1.0, 1.0),
      min_object_covered=min_object_covered)
    distorted_image.set_shape([None, None, 3])
    return distorted_image


def scale_to_inception_range(image):
    """Scales an image in the range [0,1] to [-1,1] as expected by inception."""
    with tf.control_dependencies([
     tf.assert_less_equal(tf.reduce_max(image), 1.0),
     tf.assert_greater_equal(tf.reduce_min(image), 0.0)]):
        image = tf.subtract(image, 0.5)
        image = tf.multiply(image, 2.0)
        return image


def resize_image(image, height, width):
    """Resizes an image to a target height and width."""
    image = tf.expand_dims(image, 0)
    image = tf.image.resize_bilinear(image, [height, width], align_corners=False)
    image = tf.squeeze(image, [0])
    return image


def crop_or_pad(image, curr_height, curr_width, new, height=True, crop=True):
    """Crops or pads an image.

  Args:
    image: 3-D float32 `Tensor` image.
    curr_height: Int, current height.
    curr_width: Int, current width.
    new: Int, new width or height.
    height: Boolean, cropping or padding for height.
    crop: Boolean, True if we're cropping, False if we're padding.
  Returns:
    image: 3-D float32 `Tensor` image.
  """
    abs_diff = tf.abs(new - curr_height) // 2 if height else tf.abs(new - curr_width) // 2
    offset_x = 0 if height else abs_diff
    offset_y = abs_diff if height else 0
    target_height = new
    target_width = curr_width if height else new
    if crop:
        image = tf.image.crop_to_bounding_box(image, offset_y, offset_x, target_height, target_width)
    else:
        image = tf.image.pad_to_bounding_box(image, offset_y, offset_x, target_height, target_width)
    return image


def get_central_bbox(min_side, new_size):
    """Gets the central bounding box for an image.

  If image is square, returns bounding box [0,0,1,1].
  Otherwise, returns the bounding box containing the central
  smallest side x smallest side square.

  Args:
    min_side: Int, size of smallest side in pixels.
    new_size: Int, resize image to a square of new_size x new_size pixels.
  Returns:
    bbox: A 4-D Int `Tensor`, holding the coordinates of the central bounding
      box.
  """
    max_shape = tf.cast(new_size, tf.float32)
    min_shape = tf.cast(min_side, tf.float32)
    top_xy = (max_shape - min_shape) / 2 / max_shape
    bottom_xy = (min_shape + (max_shape - min_shape) / 2) / max_shape
    bbox = tf.stack([[[top_xy, top_xy, bottom_xy, bottom_xy]]])
    bbox.set_shape([1, 1, 4])
    return bbox


def pad_to_max(image, max_scale):
    """Pads an image to max_scale times the current center crop size.

  E.g.: For an image with dimensions 1920x1080 and a max_scale of 1.5,
  returns an image that is 1.5 * (1080x1080).

  Args:
    image: 3-D float32 `Tensor` image.
    max_scale: Float, maximum scale of the image, as a multiplier on the
      central bounding box.
  Returns:
    image: 3-D float32 `Tensor` image.
  """
    orig_shape = tf.shape(image)
    orig_height = orig_shape[0]
    orig_width = orig_shape[1]
    min_side = tf.cast(tf.minimum(orig_height, orig_width), tf.float32)
    new_shape = tf.cast(tf.sqrt(max_scale * min_side * min_side), tf.int32)
    image = tf.cond(orig_height >= new_shape, lambda : crop_or_pad(image,
      orig_height, orig_width, new_shape, height=True, crop=True), lambda : crop_or_pad(image,
      orig_height, orig_width, new_shape, height=True, crop=False))
    image = tf.cond(orig_width >= new_shape, lambda : crop_or_pad(image,
      orig_height, orig_width, new_shape, height=False, crop=True), lambda : crop_or_pad(image,
      orig_height, orig_width, new_shape, height=False, crop=False))
    original_bounding_box = get_central_bbox(min_side, new_shape)
    return (image, original_bounding_box)


def scale_up_augmentation(image, max_scale):
    """Scales an image randomly >100% up to some max scale."""
    image, original_central_bbox = pad_to_max(image, max_scale)
    aug_max = 1.0
    aug_min = 1.0 / max_scale
    area_range = (aug_min, aug_max)
    min_object_covered = 1.0
    image = scale_augment_crop(image, original_central_bbox, area_range, min_object_covered)
    return image


def scale_down_augmentation(image, min_scale):
    """Scales an image randomly <100% down to some min scale."""
    image = crop_center(image)
    bbox = tf.constant([0.0, 0.0, 1.0, 1.0], dtype=(tf.float32), shape=[1, 1, 4])
    area_range = (
     min_scale, 1.0)
    image = scale_augment_crop(image, bbox, area_range, min_scale)
    return image


def augment_image_scale(image, min_scale, max_scale, p_scale_up):
    """Training time scale augmentation.

  Args:
    image: 3-d float tensor representing image.
    min_scale: minimum scale augmentation allowed, as a fraction of the
      central min_side * min_side area of the original image.
    max_scale: maximum scale augmentation allowed, as a fraction of the
      central min_side * min_side area of the original image.
    p_scale_up: Fraction of images scaled up.
  Returns:
    image: The scale-augmented image.
  """
    if not max_scale >= 1.0:
        raise AssertionError
    else:
        if not min_scale <= 1.0:
            raise AssertionError
        else:
            if min_scale == max_scale == 1.0:
                tf.logging.info('Min and max scale are 1.0, don`t augment.')
                return crop_center(image)
            if max_scale == 1.0 and min_scale < 1.0:
                tf.logging.info('Max scale is 1.0, only scale down augment.')
                return scale_down_augmentation(image, min_scale)
        if min_scale == 1.0 and max_scale > 1.0:
            tf.logging.info('Min scale is 1.0, only scale up augment.')
            return scale_up_augmentation(image, max_scale)
    tf.logging.info('Sample both augmentations.')
    rn = tf.random_uniform([], minval=0.0, maxval=1.0, dtype=(tf.float32))
    image = tf.cond(rn >= p_scale_up, lambda : scale_up_augmentation(image, max_scale), lambda : scale_down_augmentation(image, min_scale))
    return image


def decode_image(image_str):
    """Decodes a jpeg-encoded image string into a image in range [0,1]."""
    image = tf.image.decode_jpeg(image_str, channels=3)
    if image.dtype != tf.float32:
        image = tf.image.convert_image_dtype(image, dtype=(tf.float32))
    return image


def decode_images(image_strs):
    """Decodes a tensor of image strings."""
    return tf.map_fn(decode_image, image_strs, dtype=(tf.float32))


def preprocess_training_images(images, height, width, min_scale, max_scale, p_scale_up, aug_color=True, fast_mode=True):
    """Preprocesses a batch of images for training.

  This applies training-time scale and color augmentation, crops/resizes,
  and scales images to the [-1,1] range expected by pre-trained Inception nets.

  Args:
    images: A 4-D float32 `Tensor` holding raw images to be preprocessed.
    height: Int, height in pixels to resize image to.
    width: Int, width in pixels to resize image to.
    min_scale: Float, minimum scale augmentation allowed, as a fraction of the
      central min_side * min_side area of the original image.
    max_scale: Float, maximum scale augmentation allowed, as a fraction of the
      central min_side * min_side area of the original image.
    p_scale_up: Float, fraction of images scaled up.
    aug_color: Whether or not to do color augmentation.
    fast_mode: Boolean, avoids slower ops (random_hue and random_contrast).
  Returns:
    preprocessed_images: A 4-D float32 `Tensor` holding preprocessed images.
  """

    def _prepro_train(im):
        return preprocess_training_image(im,
          height, width, min_scale, max_scale, p_scale_up, aug_color=aug_color,
          fast_mode=fast_mode)

    return tf.map_fn(_prepro_train, images)


def preprocess_training_image(image, height, width, min_scale, max_scale, p_scale_up, aug_color=True, fast_mode=True):
    """Preprocesses an image for training.

  Args:
    image: A 3-d float tensor representing the image.
    height: Target image height.
    width: Target image width.
    min_scale: Minimum scale of bounding box (as a percentage of full
      bounding box) used to crop image during scale augmentation.
    max_scale: Minimum scale of bounding box (as a percentage of full
      bounding box) used to crop image during scale augmentation.
    p_scale_up: Fraction of images to scale >100%.
    aug_color: Whether or not to do color augmentation.
    fast_mode: Avoids slower ops (random_hue and random_contrast).
  Returns:
    scaled_image: An scaled image tensor in the range [-1,1].
  """
    image = augment_image_scale(image, min_scale, max_scale, p_scale_up)
    image = tf.expand_dims(image, 0)
    image = tf.image.resize_bilinear(image, [height, width], align_corners=False)
    image = tf.squeeze(image, [0])
    if aug_color:
        image = apply_with_random_selector(image,
          (lambda x, ordering: distort_color(x,
          ordering, fast_mode=fast_mode)),
          num_cases=4)
    scaled_image = scale_to_inception_range(image)
    return scaled_image


def preprocess_test_image(image, height, width, crop_strategy):
    """Preprocesses an image for test/inference.

  Args:
    image: A 3-d float tensor representing the image.
    height: Target image height.
    width: Target image width.
    crop_strategy: String, name of the strategy used to crop test-time images.
      Can be: 'crop_center', 'pad', 'pad_200', 'pad_crop_central'.
  Returns:
    scaled_image: An scaled image tensor in the range [-1,1].
  """
    image = crop_image_by_strategy(image, crop_strategy)
    image = resize_image(image, height, width)
    image = scale_to_inception_range(image)
    return image


def preprocess_test_images(images, height, width, crop_strategy):
    """Apply test-time preprocessing to a batch of images.

  This crops images (given a named strategy for doing so), resizes them,
  and scales them to the [-1,1] range expected by pre-trained Inception nets.

  Args:
    images: A 4-D float32 `Tensor` holding raw images to be preprocessed.
    height: Int, height in pixels to resize image to.
    width: Int, width in pixels to resize image to.
    crop_strategy: String, name of the strategy used to crop test-time images.
      Can be: 'crop_center', 'pad', 'pad_200', 'pad_crop_central'.
  Returns:
    preprocessed_images: A 4-D float32 `Tensor` holding preprocessed images.
  """

    def _prepro_test(im):
        return preprocess_test_image(im, height, width, crop_strategy)

    if len(images.shape) == 3:
        return _prepro_test(images)
    return tf.map_fn(_prepro_test, images)


def preprocess_images(images, is_training, height, width, min_scale=1.0, max_scale=1.0, p_scale_up=0.0, aug_color=True, fast_mode=True, crop_strategy='pad_crop_central'):
    """Preprocess a batch of images.

  Args:
    images: A 4-D float32 `Tensor` holding raw images to be preprocessed.
    is_training: Boolean, whether to preprocess them for training or test.
    height: Int, height in pixels to resize image to.
    width: Int, width in pixels to resize image to.
    min_scale: Float, minimum scale augmentation allowed, as a fraction of the
      central min_side * min_side area of the original image.
    max_scale: Float, maximum scale augmentation allowed, as a fraction of the
      central min_side * min_side area of the original image.
    p_scale_up: Float, fraction of images scaled up.
    aug_color: Whether or not to do color augmentation.
    fast_mode: Boolean, avoids slower ops (random_hue and random_contrast).
    crop_strategy: String, name of the strategy used to crop test-time images.
      Can be: 'crop_center', 'pad', 'pad_200', 'pad_crop_central'.
  Returns:
    preprocessed_images: A 4-D float32 `Tensor` holding preprocessed images.
  """
    if is_training:
        return preprocess_training_images(images, height, width, min_scale, max_scale, p_scale_up, aug_color, fast_mode)
    return preprocess_test_images(images, height, width, crop_strategy)


def cv2rotateimage(image, angle):
    """Efficient rotation if 90 degrees rotations, slow otherwise.

  Not a tensorflow function, using cv2 and scipy on numpy arrays.

  Args:
    image: a numpy array with shape [height, width, channels].
    angle: the rotation angle in degrees in the range [-180, 180].
  Returns:
    The rotated image.
  """
    if angle <= 180:
        if not angle >= -180:
            raise AssertionError
        if angle == 0:
            return image
        if angle == -90:
            image = cv2.transpose(image)
            image = cv2.flip(image, 0)
    elif angle == 90:
        image = cv2.transpose(image)
        image = cv2.flip(image, 1)
    else:
        if angle == 180 or angle == -180:
            image = cv2.flip(image, 0)
            image = cv2.flip(image, 1)
        else:
            image = ndimage.interpolation.rotate(image, 270)
    return image


def cv2resizeminedge(image, min_edge_size):
    """Resize smallest edge of image to min_edge_size."""
    if not min_edge_size >= 0:
        raise AssertionError
    else:
        height, width = image.shape[0], image.shape[1]
        new_height, new_width = (0, 0)
        if height > width:
            new_width = min_edge_size
            new_height = int(height * new_width / float(width))
        else:
            new_height = min_edge_size
        new_width = int(width * new_height / float(height))
    return cv2.resize(image, (new_width, new_height), interpolation=(cv2.INTER_AREA))


def shapestring(array):
    """Returns a compact string describing shape of an array."""
    shape = array.shape
    s = str(shape[0])
    for i in range(1, len(shape)):
        s += 'x' + str(shape[i])

    return s


def unscale_jpeg_encode(ims):
    """Unscales pixel values and jpeg encodes preprocessed image.

  Args:
    ims: A 4-D float32 `Tensor` holding preprocessed images.
  Returns:
    im_strings: A 1-D string `Tensor` holding images that have been unscaled
      (reversing the inception [-1,1] scaling), and jpeg encoded.
  """
    ims /= 2.0
    ims += 0.5
    ims *= 255.0
    ims = tf.clip_by_value(ims, 0, 255)
    ims = tf.cast(ims, tf.uint8)
    im_strings = tf.map_fn((lambda x: tf.image.encode_jpeg(x, format='rgb', quality=100)),
      ims,
      dtype=(tf.string))
    return im_strings