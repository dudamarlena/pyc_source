# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/svpino/dev/tensorflow-object-detection-sagemaker/todl/tensorflow-object-detection/research/domain_adaptation/pixel_domain_adaptation/pixelda_preprocess.py
# Compiled at: 2020-04-05 19:50:57
# Size of source mod 2**32: 3917 bytes
"""Contains functions for preprocessing the inputs."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import tensorflow as tf

def preprocess_classification(image, labels, is_training=False):
    """Preprocesses the image and labels for classification purposes.

  Preprocessing includes shifting the images to be 0-centered between -1 and 1.
  This is not only a popular method of preprocessing (inception) but is also
  the mechanism used by DSNs.

  Args:
    image: A `Tensor` of size [height, width, 3].
    labels: A dictionary of labels.
    is_training: Whether or not we're training the model.

  Returns:
    The preprocessed image and labels.
  """
    image = tf.image.convert_image_dtype(image, tf.float32)
    image -= 0.5
    image *= 2
    return (
     image, labels)


def preprocess_style_transfer(image, labels, augment=False, size=None, is_training=False):
    """Preprocesses the image and labels for style transfer purposes.

  Args:
    image: A `Tensor` of size [height, width, 3].
    labels: A dictionary of labels.
    augment: Whether to apply data augmentation to inputs
    size: The height and width to which images should be resized. If left as
      `None`, then no resizing is performed
    is_training: Whether or not we're training the model

  Returns:
    The preprocessed image and labels. Scaled to [-1, 1]
  """
    image = tf.image.convert_image_dtype(image, tf.float32)
    if augment:
        if is_training:
            image = image_augmentation(image)
    if size:
        image = resize_image(image, size)
    image -= 0.5
    image *= 2
    return (
     image, labels)


def image_augmentation(image):
    """Performs data augmentation by randomly permuting the inputs.

  Args:
    image: A float `Tensor` of size [height, width, channels] with values
      in range[0,1].

  Returns:
    The mutated batch of images
  """
    num_channels = image.shape_as_list()[(-1)]
    if num_channels == 4:
        image, depth = image[:, :, 0:3], image[:, :, 3:4]
    else:
        if num_channels == 1:
            image = tf.image.grayscale_to_rgb(image)
        else:
            image = tf.image.random_brightness(image, max_delta=0.1)
            image = tf.image.random_saturation(image, lower=0.5, upper=1.5)
            image = tf.image.random_hue(image, max_delta=0.032)
            image = tf.image.random_contrast(image, lower=0.5, upper=1.5)
            image = tf.clip_by_value(image, 0, 1.0)
            if num_channels == 4:
                image = tf.concat(2, [image, depth])
            else:
                if num_channels == 1:
                    image = tf.image.rgb_to_grayscale(image)
        return image


def resize_image(image, size=None):
    """Resize image to target size.

  Args:
    image: A `Tensor` of size [height, width, 3].
    size: (height, width) to resize image to.

  Returns:
    resized image
  """
    if size is None:
        raise ValueError('Must specify size')
    if image.shape_as_list()[:2] == size:
        return image
    image = tf.expand_dims(image, 0)
    image = tf.image.resize_images(image, size)
    image = tf.squeeze(image, 0)
    return image