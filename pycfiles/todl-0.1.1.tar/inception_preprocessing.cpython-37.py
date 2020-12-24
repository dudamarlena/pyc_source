# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/svpino/dev/tensorflow-object-detection-sagemaker/todl/tensorflow-object-detection/research/attention_ocr/python/inception_preprocessing.py
# Compiled at: 2020-04-05 19:50:57
# Size of source mod 2**32: 13658 bytes
"""Provides utilities to preprocess images for the Inception networks."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import tensorflow as tf
from tensorflow.python.ops import control_flow_ops

def apply_with_random_selector(x, func, num_cases):
    """Computes func(x, sel), with sel sampled from [0...num_cases-1].

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


def distort_color--- This code section failed: ---

 L.  67         0  LOAD_GLOBAL              tf
                2  LOAD_METHOD              name_scope
                4  LOAD_FAST                'scope'
                6  LOAD_STR                 'distort_color'
                8  LOAD_FAST                'image'
               10  BUILD_LIST_1          1 
               12  CALL_METHOD_3         3  '3 positional arguments'
            14_16  SETUP_WITH          446  'to 446'
               18  POP_TOP          

 L.  68        20  LOAD_FAST                'fast_mode'
               22  POP_JUMP_IF_FALSE   106  'to 106'

 L.  69        24  LOAD_FAST                'color_ordering'
               26  LOAD_CONST               0
               28  COMPARE_OP               ==
               30  POP_JUMP_IF_FALSE    68  'to 68'

 L.  70        32  LOAD_GLOBAL              tf
               34  LOAD_ATTR                image
               36  LOAD_ATTR                random_brightness
               38  LOAD_FAST                'image'
               40  LOAD_CONST               0.12549019607843137
               42  LOAD_CONST               ('max_delta',)
               44  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               46  STORE_FAST               'image'

 L.  71        48  LOAD_GLOBAL              tf
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

 L.  73        68  LOAD_GLOBAL              tf
               70  LOAD_ATTR                image
               72  LOAD_ATTR                random_saturation
               74  LOAD_FAST                'image'
               76  LOAD_CONST               0.5
               78  LOAD_CONST               1.5
               80  LOAD_CONST               ('lower', 'upper')
               82  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               84  STORE_FAST               'image'

 L.  74        86  LOAD_GLOBAL              tf
               88  LOAD_ATTR                image
               90  LOAD_ATTR                random_brightness
               92  LOAD_FAST                'image'
               94  LOAD_CONST               0.12549019607843137
               96  LOAD_CONST               ('max_delta',)
               98  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              100  STORE_FAST               'image'
          102_104  JUMP_FORWARD        432  'to 432'
            106_0  COME_FROM            22  '22'

 L.  76       106  LOAD_FAST                'color_ordering'
              108  LOAD_CONST               0
              110  COMPARE_OP               ==
              112  POP_JUMP_IF_FALSE   184  'to 184'

 L.  77       114  LOAD_GLOBAL              tf
              116  LOAD_ATTR                image
              118  LOAD_ATTR                random_brightness
              120  LOAD_FAST                'image'
              122  LOAD_CONST               0.12549019607843137
              124  LOAD_CONST               ('max_delta',)
              126  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              128  STORE_FAST               'image'

 L.  78       130  LOAD_GLOBAL              tf
              132  LOAD_ATTR                image
              134  LOAD_ATTR                random_saturation
              136  LOAD_FAST                'image'
              138  LOAD_CONST               0.5
              140  LOAD_CONST               1.5
              142  LOAD_CONST               ('lower', 'upper')
              144  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              146  STORE_FAST               'image'

 L.  79       148  LOAD_GLOBAL              tf
              150  LOAD_ATTR                image
              152  LOAD_ATTR                random_hue
              154  LOAD_FAST                'image'
              156  LOAD_CONST               0.2
              158  LOAD_CONST               ('max_delta',)
              160  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              162  STORE_FAST               'image'

 L.  80       164  LOAD_GLOBAL              tf
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

 L.  81       184  LOAD_FAST                'color_ordering'
              186  LOAD_CONST               1
              188  COMPARE_OP               ==
          190_192  POP_JUMP_IF_FALSE   264  'to 264'

 L.  82       194  LOAD_GLOBAL              tf
              196  LOAD_ATTR                image
              198  LOAD_ATTR                random_saturation
              200  LOAD_FAST                'image'
              202  LOAD_CONST               0.5
              204  LOAD_CONST               1.5
              206  LOAD_CONST               ('lower', 'upper')
              208  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              210  STORE_FAST               'image'

 L.  83       212  LOAD_GLOBAL              tf
              214  LOAD_ATTR                image
              216  LOAD_ATTR                random_brightness
              218  LOAD_FAST                'image'
              220  LOAD_CONST               0.12549019607843137
              222  LOAD_CONST               ('max_delta',)
              224  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              226  STORE_FAST               'image'

 L.  84       228  LOAD_GLOBAL              tf
              230  LOAD_ATTR                image
              232  LOAD_ATTR                random_contrast
              234  LOAD_FAST                'image'
              236  LOAD_CONST               0.5
              238  LOAD_CONST               1.5
              240  LOAD_CONST               ('lower', 'upper')
              242  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              244  STORE_FAST               'image'

 L.  85       246  LOAD_GLOBAL              tf
              248  LOAD_ATTR                image
              250  LOAD_ATTR                random_hue
              252  LOAD_FAST                'image'
              254  LOAD_CONST               0.2
              256  LOAD_CONST               ('max_delta',)
              258  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              260  STORE_FAST               'image'
              262  JUMP_FORWARD        432  'to 432'
            264_0  COME_FROM           190  '190'

 L.  86       264  LOAD_FAST                'color_ordering'
              266  LOAD_CONST               2
              268  COMPARE_OP               ==
          270_272  POP_JUMP_IF_FALSE   344  'to 344'

 L.  87       274  LOAD_GLOBAL              tf
              276  LOAD_ATTR                image
              278  LOAD_ATTR                random_contrast
              280  LOAD_FAST                'image'
              282  LOAD_CONST               0.5
              284  LOAD_CONST               1.5
              286  LOAD_CONST               ('lower', 'upper')
              288  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              290  STORE_FAST               'image'

 L.  88       292  LOAD_GLOBAL              tf
              294  LOAD_ATTR                image
              296  LOAD_ATTR                random_hue
              298  LOAD_FAST                'image'
              300  LOAD_CONST               0.2
              302  LOAD_CONST               ('max_delta',)
              304  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              306  STORE_FAST               'image'

 L.  89       308  LOAD_GLOBAL              tf
              310  LOAD_ATTR                image
              312  LOAD_ATTR                random_brightness
              314  LOAD_FAST                'image'
              316  LOAD_CONST               0.12549019607843137
              318  LOAD_CONST               ('max_delta',)
              320  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              322  STORE_FAST               'image'

 L.  90       324  LOAD_GLOBAL              tf
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

 L.  91       344  LOAD_FAST                'color_ordering'
              346  LOAD_CONST               3
              348  COMPARE_OP               ==
          350_352  POP_JUMP_IF_FALSE   424  'to 424'

 L.  92       354  LOAD_GLOBAL              tf
              356  LOAD_ATTR                image
              358  LOAD_ATTR                random_hue
              360  LOAD_FAST                'image'
              362  LOAD_CONST               0.2
              364  LOAD_CONST               ('max_delta',)
              366  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              368  STORE_FAST               'image'

 L.  93       370  LOAD_GLOBAL              tf
              372  LOAD_ATTR                image
              374  LOAD_ATTR                random_saturation
              376  LOAD_FAST                'image'
              378  LOAD_CONST               0.5
              380  LOAD_CONST               1.5
              382  LOAD_CONST               ('lower', 'upper')
              384  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              386  STORE_FAST               'image'

 L.  94       388  LOAD_GLOBAL              tf
              390  LOAD_ATTR                image
              392  LOAD_ATTR                random_contrast
            394_0  COME_FROM            66  '66'
              394  LOAD_FAST                'image'
              396  LOAD_CONST               0.5
              398  LOAD_CONST               1.5
              400  LOAD_CONST               ('lower', 'upper')
              402  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              404  STORE_FAST               'image'

 L.  95       406  LOAD_GLOBAL              tf
              408  LOAD_ATTR                image
              410  LOAD_ATTR                random_brightness
              412  LOAD_FAST                'image'
              414  LOAD_CONST               0.12549019607843137
              416  LOAD_CONST               ('max_delta',)
              418  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              420  STORE_FAST               'image'
              422  JUMP_FORWARD        432  'to 432'
            424_0  COME_FROM           350  '350'

 L.  97       424  LOAD_GLOBAL              ValueError
              426  LOAD_STR                 'color_ordering must be in [0, 3]'
              428  CALL_FUNCTION_1       1  '1 positional argument'
              430  RAISE_VARARGS_1       1  'exception instance'
            432_0  COME_FROM           422  '422'
            432_1  COME_FROM           342  '342'
            432_2  COME_FROM           262  '262'
            432_3  COME_FROM           182  '182'
            432_4  COME_FROM           102  '102'

 L. 100       432  LOAD_GLOBAL              tf
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


def distorted_bounding_box_crop(image, bbox, min_object_covered=0.1, aspect_ratio_range=(0.75, 1.33), area_range=(0.05, 1.0), max_attempts=100, scope=None):
    """Generates cropped_image using a one of the bboxes randomly distorted.

  See `tf.image.sample_distorted_bounding_box` for more documentation.

  Args:
    image: 3-D Tensor of image (it will be converted to floats in [0, 1]).
    bbox: 3-D float Tensor of bounding boxes arranged [1, num_boxes, coords]
      where each coordinate is [0, 1) and the coordinates are arranged
      as [ymin, xmin, ymax, xmax]. If num_boxes is 0 then it would use the
      whole image.
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
    with tf.name_scopescope'distorted_bounding_box_crop'[image, bbox]:
        sample_distorted_bounding_box = tf.image.sample_distorted_bounding_box((tf.shape(image)),
          bounding_boxes=bbox,
          min_object_covered=min_object_covered,
          aspect_ratio_range=aspect_ratio_range,
          area_range=area_range,
          max_attempts=max_attempts,
          use_image_if_no_bounding_boxes=True)
        bbox_begin, bbox_size, distort_bbox = sample_distorted_bounding_box
        cropped_image = tf.sliceimagebbox_beginbbox_size
        return (cropped_image, distort_bbox)


def preprocess_for_train(image, height, width, bbox, fast_mode=True, scope=None):
    """Distort one image for training a network.

  Distorting images provides a useful technique for augmenting the data
  set during training in order to make the network invariant to aspects
  of the image that do not effect the label.

  Additionally it would create image_summaries to display the different
  transformations applied to the image.

  Args:
    image: 3-D Tensor of image. If dtype is tf.float32 then the range should be
      [0, 1], otherwise it would converted to tf.float32 assuming that the range
      is [0, MAX], where MAX is largest positive representable number for
      int(8/16/32) data type (see `tf.image.convert_image_dtype` for details).
    height: integer
    width: integer
    bbox: 3-D float Tensor of bounding boxes arranged [1, num_boxes, coords]
      where each coordinate is [0, 1) and the coordinates are arranged
      as [ymin, xmin, ymax, xmax].
    fast_mode: Optional boolean, if True avoids slower transformations (i.e.
      bi-cubic resizing, random_hue or random_contrast).
    scope: Optional scope for name_scope.
  Returns:
    3-D float Tensor of distorted image used for training with range [-1, 1].
  """
    with tf.name_scopescope'distort_image'[image, height, width, bbox]:
        if bbox is None:
            bbox = tf.constant([
             0.0, 0.0, 1.0, 1.0],
              dtype=(tf.float32), shape=[1, 1, 4])
        if image.dtype != tf.float32:
            image = tf.image.convert_image_dtype(image, dtype=(tf.float32))
        image_with_box = tf.image.draw_bounding_boxes(tf.expand_dims(image, 0), bbox)
        tf.summary.image('image_with_bounding_boxes', image_with_box)
        distorted_image, distorted_bbox = distorted_bounding_box_crop(image, bbox)
        distorted_image.set_shape([None, None, 3])
        image_with_distorted_box = tf.image.draw_bounding_boxes(tf.expand_dims(image, 0), distorted_bbox)
        tf.summary.image('images_with_distorted_bounding_box', image_with_distorted_box)
        num_resize_cases = 1 if fast_mode else 4
        distorted_image = apply_with_random_selector(distorted_image,
          (lambda x, method: tf.image.resize_images(x, [height, width], method=method)),
          num_cases=num_resize_cases)
        tf.summary.image('cropped_resized_image', tf.expand_dims(distorted_image, 0))
        distorted_image = tf.image.random_flip_left_right(distorted_image)
        distorted_image = apply_with_random_selector(distorted_image,
          (lambda x, ordering: distort_color(x, ordering, fast_mode)),
          num_cases=4)
        tf.summary.image('final_distorted_image', tf.expand_dims(distorted_image, 0))
        distorted_image = tf.subtract(distorted_image, 0.5)
        distorted_image = tf.multiply(distorted_image, 2.0)
        return distorted_image


def preprocess_for_eval(image, height, width, central_fraction=0.875, scope=None):
    """Prepare one image for evaluation.

  If height and width are specified it would output an image with that size by
  applying resize_bilinear.

  If central_fraction is specified it would cropt the central fraction of the
  input image.

  Args:
    image: 3-D Tensor of image. If dtype is tf.float32 then the range should be
      [0, 1], otherwise it would converted to tf.float32 assuming that the range
      is [0, MAX], where MAX is largest positive representable number for
      int(8/16/32) data type (see `tf.image.convert_image_dtype` for details)
    height: integer
    width: integer
    central_fraction: Optional Float, fraction of the image to crop.
    scope: Optional scope for name_scope.
  Returns:
    3-D float Tensor of prepared image.
  """
    with tf.name_scopescope'eval_image'[image, height, width]:
        if image.dtype != tf.float32:
            image = tf.image.convert_image_dtype(image, dtype=(tf.float32))
        else:
            if central_fraction:
                image = tf.image.central_crop(image, central_fraction=central_fraction)
            if height and width:
                image = tf.expand_dims(image, 0)
                image = tf.image.resize_bilinear(image,
                  [height, width], align_corners=False)
                image = tf.squeeze(image, [0])
        image = tf.subtract(image, 0.5)
        image = tf.multiply(image, 2.0)
        return image


def preprocess_image(image, height, width, is_training=False, bbox=None, fast_mode=True):
    """Pre-process one image for training or evaluation.

  Args:
    image: 3-D Tensor [height, width, channels] with the image.
    height: integer, image expected height.
    width: integer, image expected width.
    is_training: Boolean. If true it would transform an image for train,
      otherwise it would transform it for evaluation.
    bbox: 3-D float Tensor of bounding boxes arranged [1, num_boxes, coords]
      where each coordinate is [0, 1) and the coordinates are arranged as
      [ymin, xmin, ymax, xmax].
    fast_mode: Optional boolean, if True avoids slower transformations.

  Returns:
    3-D float Tensor containing an appropriately scaled image

  Raises:
    ValueError: if user does not provide bounding box
  """
    if is_training:
        return preprocess_for_train(image, height, width, bbox, fast_mode)
    return preprocess_for_eval(image, height, width)