# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/model/space/op/cnn.py
# Compiled at: 2019-09-05 10:20:47
# Size of source mod 2**32: 8588 bytes
"""
Operations corresponding to convolution neural networks.

Learn more about different kind of convolution : https://towardsdatascience.com/types-of-convolutions-in-deep-learning-717013397f4d
"""
import tensorflow as tf
from ..op import Operation

class IdentityConv2D(Operation):
    __doc__ = 'Create a kind of identity operation.\n\n        Args:\n            num_filters (int): filter dimension that should be outputed by the operation.\n    '

    def __init__(self, num_filters=32, stride=1):
        self.num_filters = num_filters
        self.stride = stride

    def __call__(self, inputs, **kwargs):
        """Create the tensorflow operation.

        Args:
            inputs (list(Tensor)): list of input tensors.

        Return: a tensor corresponding to the operation.
        """
        out = tf.contrib.layers.conv2d(inputs=(inputs[0]),
          num_outputs=(self.num_filters),
          kernel_size=(
         self.stride, self.stride),
          stride=(self.stride),
          padding='SAME')
        out = tf.contrib.layers.batch_norm(out)
        return out


class Convolution2D(Operation):
    __doc__ = 'Classic convolution with 2 dimensions.\n\n    Create a 2 dimensions classic convolution operation.\n    https://www.tensorflow.org/versions/r1.0/api_docs/python/tf/contrib/layers/conv2d\n\n    Args:\n        filter_height (int): height of a filter or kernel.\n        filter_width (int): width of a filter or kernel.\n        num_filters (int): number of filters in the convolution operation.\n    '

    def __init__(self, filter_height, filter_width, num_filters=32, stride=1, padding='SAME'):
        self.filter_height = filter_height
        self.filter_width = filter_width
        self.num_filters = num_filters
        self.stride = stride
        self.padding = padding

    def __str__(self):
        return f"CNN2D_{self.filter_height}x{self.filter_width}_f{self.num_filters}"

    def __call__(self, inputs, **kwargs):
        """Create the tensorflow operation.

        Args:
            inputs (list(Tensor)): list of input tensors.

        Return: a tensor corresponding to the operation.
        """
        out = tf.contrib.layers.conv2d(inputs=(inputs[0]),
          num_outputs=(self.num_filters),
          kernel_size=(
         self.filter_height, self.filter_width),
          stride=(self.stride),
          padding=(self.padding))
        return out


class DepthwiseSeparable2D(Operation):
    __doc__ = 'Depthwise-separable convolution with 2 dimensions.\n\n    Create a 2 dimensions depthwise-separable convolution operation.\n    https://www.tensorflow.org/versions/r1.0/api_docs/python/tf/contrib/layers/separable_conv2d\n\n    Args:\n        filter_height (int): height of a filter or kernel.\n        filter_width (int): width of a filter or kernel.\n        num_filters (int): number of filters in the convolution operation.\n    '

    def __init__(self, filter_height, filter_width, num_filters=32, depth_multiplier=1, stride=1, padding='SAME'):
        self.filter_height = filter_height
        self.filter_width = filter_width
        self.num_filters = num_filters
        self.depth_multiplier = depth_multiplier
        self.stride = stride
        self.padding = padding

    def __str__(self):
        return f"DepSepCNN2D_{self.filter_height}x{self.filter_width}_f{self.num_filters}"

    def __call__(self, inputs, **kwargs):
        """Create the tensorflow operation.

        Args:
            inputs (list(Tensor)): list of input tensors.

        Return: a tensor corresponding to the operation.
        """
        out = tf.contrib.layers.separable_conv2d(inputs=(inputs[0]),
          num_outputs=(self.num_filters),
          depth_multiplier=(self.depth_multiplier),
          kernel_size=(
         self.filter_height, self.filter_width),
          stride=(self.stride),
          padding=(self.padding))
        return out


class Dilation2D(Operation):
    __doc__ = 'Dilation convolution with 2 dimensions.\n\n    Create a 2 dimensions dilation convolution operation.\n    https://www.tensorflow.org/api_docs/python/tf/nn/dilation2d\n\n    Args:\n        filter_height (int): height of a filter or kernel.\n        filter_width (int): width of a filter or kernel.\n        num_filters (int): number of filters in the convolution operation.\n    '

    def __init__(self, filter_height, filter_width, num_filters=32, stride=1, rate_height=2, rate_width=2, padding='SAME'):
        self.filter_height = filter_height
        self.filter_width = filter_width
        self.num_filters = num_filters
        self.stride = stride
        self.rate_height = rate_height
        self.rate_width = rate_width
        self.padding = padding

    def __str__(self):
        return f"Dilation2D_{self.filter_height}x{self.filter_width}"

    def __call__(self, inputs, **kwargs):
        """Create the tensorflow operation.

        Args:
            inputs (list(Tensor)): list of input tensors.

        Return: a tensor corresponding to the operation.
        """
        rate_height = self.rate_height if self.stride == 1 else 1
        rate_width = self.rate_width if self.stride == 1 else 1
        out = tf.contrib.layers.conv2d(inputs=(inputs[0]),
          num_outputs=(self.num_filters),
          kernel_size=(
         self.filter_height, self.filter_width),
          rate=[
         rate_height, rate_width],
          stride=(self.stride),
          padding=(self.padding))
        return out


class MaxPooling2D(Operation):
    __doc__ = "Max pooling with 2 dimensions.\n\n    Create a 2 dimensions max pooling operation.\n    https://www.tensorflow.org/versions/r1.0/api_docs/python/tf/contrib/layers/max_pool2d\n\n    Args:\n        kernel_height (int):\n        kernel_width (int):\n        stride_height (int):\n        stride_width (int):\n        padding (string): 'SAME' or 'VALID'\n        num_filters (int): corresponding to the number of filters we need the output to have\n    "

    def __init__(self, kernel_height, kernel_width, stride=1, padding='SAME', num_filters=32):
        self.kernel_height = kernel_height
        self.kernel_width = kernel_width
        self.stride = stride
        self.padding = padding
        self.num_filters = num_filters

    def __str__(self):
        return f"MaxPool2D_k{self.kernel_height}x{self.kernel_width}_s{self.stride}"

    def __call__(self, inputs, **kwargs):
        """Create the tensorflow operation.

        Args:
            inputs (list(Tensor)): list of input tensors.

        Return: a tensor corresponding to the operation.
        """
        out = tf.contrib.layers.max_pool2d(inputs=(inputs[0]),
          kernel_size=(
         self.kernel_height, self.kernel_width),
          stride=(self.stride),
          padding=(self.padding))
        out = tf.contrib.layers.conv2d(inputs=out,
          num_outputs=(self.num_filters),
          kernel_size=(1, 1),
          stride=1,
          padding='SAME')
        out = tf.contrib.layers.batch_norm(out)
        return out


class AvgPooling2D(Operation):
    __doc__ = "Average pooling with 2 dimensions.\n\n    Create a 2 dimensions average pooling operation.\n    https://www.tensorflow.org/versions/r1.0/api_docs/python/tf/contrib/layers/avg_pool2d\n\n    Args:\n        kernel_height (int):\n        kernel_width (int):\n        stride_height (int):\n        stride_width (int):\n        padding (string): 'SAME' or 'VALID'\n        num_filters (int): corresponding to the number of filters we need the output to have\n    "

    def __init__(self, kernel_height, kernel_width, stride=1, padding='SAME', num_filters=32):
        self.kernel_height = kernel_height
        self.kernel_width = kernel_width
        self.stride = stride
        self.padding = padding
        self.num_filters = num_filters

    def __str__(self):
        return f"AvgPool2D_k{self.kernel_height}x{self.kernel_width}_s{self.stride}"

    def __call__(self, inputs, **kwargs):
        """Create the tensorflow operation.

        Args:
            inputs (list(Tensor)): list of input tensors.

        Return: a tensor corresponding to the operation.
        """
        out = tf.contrib.layers.avg_pool2d(inputs=(inputs[0]),
          kernel_size=(
         self.kernel_height, self.kernel_width),
          stride=(self.stride),
          padding=(self.padding))
        out = tf.contrib.layers.conv2d(inputs=out,
          num_outputs=(self.num_filters),
          kernel_size=(1, 1),
          stride=1,
          padding='SAME')
        out = tf.contrib.layers.batch_norm(out)
        return out