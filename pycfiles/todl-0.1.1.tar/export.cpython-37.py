# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/svpino/dev/tensorflow-object-detection-sagemaker/todl/tensorflow-object-detection/official/r1/utils/export.py
# Compiled at: 2020-04-05 19:50:57
# Size of source mod 2**32: 1931 bytes
"""Convenience functions for exporting models as SavedModels or other types."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import tensorflow as tf

def build_tensor_serving_input_receiver_fn(shape, dtype=tf.float32, batch_size=1):
    """Returns a input_receiver_fn that can be used during serving.

  This expects examples to come through as float tensors, and simply
  wraps them as TensorServingInputReceivers.

  Arguably, this should live in tf.estimator.export. Testing here first.

  Args:
    shape: list representing target size of a single example.
    dtype: the expected datatype for the input example
    batch_size: number of input tensors that will be passed for prediction

  Returns:
    A function that itself returns a TensorServingInputReceiver.
  """

    def serving_input_receiver_fn():
        features = tf.compat.v1.placeholder(dtype=dtype,
          shape=([batch_size] + shape),
          name='input_tensor')
        return tf.estimator.export.TensorServingInputReceiver(features=features,
          receiver_tensors=features)

    return serving_input_receiver_fn