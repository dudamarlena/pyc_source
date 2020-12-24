# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/svpino/dev/tensorflow-object-detection-sagemaker/todl/tensorflow-object-detection/official/modeling/activations/gelu.py
# Compiled at: 2020-04-05 19:50:57
# Size of source mod 2**32: 1296 bytes
"""Gaussian error linear unit."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import math, tensorflow as tf

@tf.keras.utils.register_keras_serializable(package='Text')
def gelu(x):
    """Gaussian Error Linear Unit.

  This is a smoother version of the RELU.
  Original paper: https://arxiv.org/abs/1606.08415
  Args:
    x: float Tensor to perform activation.

  Returns:
    `x` with the GELU activation applied.
  """
    cdf = 0.5 * (1.0 + tf.tanh(math.sqrt(2 / math.pi) * (x + 0.044715 * tf.pow(x, 3))))
    return x * cdf