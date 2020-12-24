# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/utils/static_shape.py
# Compiled at: 2018-06-15 01:29:00
# Size of source mod 2**32: 1895 bytes
"""Helper functions to access TensorShape values.

The rank 4 tensor_shape must be of the form [batch_size, height, width, depth].
"""

def get_batch_size(tensor_shape):
    """Returns batch size from the tensor shape.

  Args:
    tensor_shape: A rank 4 TensorShape.

  Returns:
    An integer representing the batch size of the tensor.
  """
    tensor_shape.assert_has_rank(rank=4)
    return tensor_shape[0].value


def get_height(tensor_shape):
    """Returns height from the tensor shape.

  Args:
    tensor_shape: A rank 4 TensorShape.

  Returns:
    An integer representing the height of the tensor.
  """
    tensor_shape.assert_has_rank(rank=4)
    return tensor_shape[1].value


def get_width(tensor_shape):
    """Returns width from the tensor shape.

  Args:
    tensor_shape: A rank 4 TensorShape.

  Returns:
    An integer representing the width of the tensor.
  """
    tensor_shape.assert_has_rank(rank=4)
    return tensor_shape[2].value


def get_depth(tensor_shape):
    """Returns depth from the tensor shape.

  Args:
    tensor_shape: A rank 4 TensorShape.

  Returns:
    An integer representing the depth of the tensor.
  """
    tensor_shape.assert_has_rank(rank=4)
    return tensor_shape[3].value