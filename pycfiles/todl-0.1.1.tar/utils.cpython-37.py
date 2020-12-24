# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/svpino/dev/tensorflow-object-detection-sagemaker/todl/tensorflow-object-detection/research/object_detection/tpu_exporters/utils.py
# Compiled at: 2020-04-05 19:50:58
# Size of source mod 2**32: 1785 bytes
"""Utilities for TPU inference."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import tensorflow as tf

def bfloat16_to_float32(tensor):
    """Converts a tensor to tf.float32 only if it is tf.bfloat16."""
    if tensor.dtype == tf.bfloat16:
        return tf.cast(tensor, dtype=(tf.float32))
    return tensor


def bfloat16_to_float32_nested(bfloat16_tensor_dict):
    """Converts bfloat16 tensors in a nested structure to float32.

  Other tensors not of dtype bfloat16 will be left as is.

  Args:
    bfloat16_tensor_dict: A Python dict, values being Tensor or Python
      list/tuple of Tensor.

  Returns:
    A Python dict with the same structure as `bfloat16_tensor_dict`,
    with all bfloat16 tensors converted to float32.
  """
    float32_tensor_dict = {}
    for k, v in bfloat16_tensor_dict.items():
        if isinstance(v, tf.Tensor):
            float32_tensor_dict[k] = bfloat16_to_float32(v)

    return float32_tensor_dict