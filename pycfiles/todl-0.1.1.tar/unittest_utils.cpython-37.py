# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/svpino/dev/tensorflow-object-detection-sagemaker/todl/tensorflow-object-detection/research/attention_ocr/python/datasets/unittest_utils.py
# Compiled at: 2020-04-05 19:50:57
# Size of source mod 2**32: 2125 bytes
"""Functions to make unit testing easier."""
import numpy as np, io
from PIL import Image as PILImage
import tensorflow as tf

def create_random_image(image_format, shape):
    """Creates an image with random values.

  Args:
    image_format: An image format (PNG or JPEG).
    shape: A tuple with image shape (including channels).

  Returns:
    A tuple (<numpy ndarray>, <a string with encoded image>)
  """
    image = np.random.randint(low=0, high=255, size=shape, dtype='uint8')
    fd = io.BytesIO()
    image_pil = PILImage.fromarray(image)
    image_pil.save(fd, image_format, subsampling=0, quality=100)
    return (image, fd.getvalue())


def create_serialized_example(name_to_values):
    """Creates a tf.Example proto using a dictionary.

  It automatically detects type of values and define a corresponding feature.

  Args:
    name_to_values: A dictionary.

  Returns:
    tf.Example proto.
  """
    example = tf.train.Example()
    for name, values in name_to_values.items():
        feature = example.features.feature[name]
        if isinstance(values[0], str) or isinstance(values[0], bytes):
            add = feature.bytes_list.value.extend
        else:
            if isinstance(values[0], float):
                add = feature.float32_list.value.extend
            else:
                if isinstance(values[0], int):
                    add = feature.int64_list.value.extend
                else:
                    raise AssertionError('Unsupported type: %s' % type(values[0]))
        add(values)

    return example.SerializeToString()