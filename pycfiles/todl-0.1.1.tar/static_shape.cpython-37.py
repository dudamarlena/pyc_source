# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/svpino/dev/tensorflow-object-detection-sagemaker/todl/tensorflow-object-detection/research/object_detection/utils/static_shape.py
# Compiled at: 2020-04-05 19:50:58
# Size of source mod 2**32: 2295 bytes
"""Helper functions to access TensorShape values.

The rank 4 tensor_shape must be of the form [batch_size, height, width, depth].
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

def get_dim_as_int(dim):
    """Utility to get v1 or v2 TensorShape dim as an int.

  Args:
    dim: The TensorShape dimension to get as an int

  Returns:
    None or an int.
  """
    try:
        return dim.value
    except AttributeError:
        return dim


def get_batch_size(tensor_shape):
    """Returns batch size from the tensor shape.

  Args:
    tensor_shape: A rank 4 TensorShape.

  Returns:
    An integer representing the batch size of the tensor.
  """
    tensor_shape.assert_has_rank(rank=4)
    return get_dim_as_int(tensor_shape[0])


def get_height(tensor_shape):
    """Returns height from the tensor shape.

  Args:
    tensor_shape: A rank 4 TensorShape.

  Returns:
    An integer representing the height of the tensor.
  """
    tensor_shape.assert_has_rank(rank=4)
    return get_dim_as_int(tensor_shape[1])


def get_width(tensor_shape):
    """Returns width from the tensor shape.

  Args:
    tensor_shape: A rank 4 TensorShape.

  Returns:
    An integer representing the width of the tensor.
  """
    tensor_shape.assert_has_rank(rank=4)
    return get_dim_as_int(tensor_shape[2])


def get_depth(tensor_shape):
    """Returns depth from the tensor shape.

  Args:
    tensor_shape: A rank 4 TensorShape.

  Returns:
    An integer representing the depth of the tensor.
  """
    tensor_shape.assert_has_rank(rank=4)
    return get_dim_as_int(tensor_shape[3])