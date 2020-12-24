# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\dynn\layers\pooling_layers.py
# Compiled at: 2018-09-19 16:40:05
# Size of source mod 2**32: 6247 bytes
"""
Pooling layers
==============
"""
from __future__ import print_function, division
import dynet as dy
from .. import util, operations
from .base_layers import BaseLayer

def max_pool_dim(x, d=0, kernel_width=None, stride=1):
    """Efficent max pooling on GPU, assuming x is a matrix
    or a list of vectors"""
    h = util.list_to_matrix(x)
    h = util.matrix_to_image(h)
    (d1, d2, _), bsize = h.dim()
    kernel_size = [
     d1, d2]
    kernel_size[1 - d] = 1
    if kernel_width is not None:
        kernel_size[d] = kernel_width
    max_pooled = dy.maxpooling2d(h, ksize=kernel_size, stride=[1, stride])
    output_dim = d1 if d == 0 else d2
    output = dy.reshape(max_pooled, (output_dim,), batch_size=bsize)
    return output


class MaxPooling1DLayer(BaseLayer):
    __doc__ = '1D max pooling\n\n    Args:\n        default_kernel_size (int, optional): Default kernel size. If this is\n            not specified, the default is to pool over the full sequence\n            (default: ``None``)\n        stride (int, optional): Default temporal stride (default: ``1``)\n    '

    def __init__(self, default_kernel_size=None, default_stride=1):
        super(MaxPooling1DLayer, self).__init__('maxpool1d')
        self.kernel_size = default_kernel_size
        self.stride = default_stride

    def __call__(self, x, kernel_size=None, stride=None):
        """Max pooling over the first dimension.

        This takes either a list of ``N`` ``d``-dimensional vectors or
        a ``N x d`` matrix.

        The output will be a matrix of dimension
        ``(N - kernel_size + 1) // stride x d``

        Args:
            x (:py:class:`dynet.Expression`): Input matrix or list of vectors
            dim (int, optional): The reduction dimension (default: ``0``)
            kernel_size (int, optional): Kernel size. If this is not
                specified, the default size specified in the constructor
                is used.
            stride (int, optional): Temporal stride. If this is not specified,
                the default stride specified in the constructor is used.

        Returns:
            :py:class:`dynet.Expression`: Pooled sequence.
        """
        x = util.list_to_matrix(x)
        x_dim, _ = x.dim()
        img = operations.unsqueeze(x, d=1)
        kernel_size = [
         kernel_size or self.kernel_size or x_dim[0], 1]
        max_pooled_img = dy.maxpooling2d(img,
          ksize=kernel_size,
          stride=[
         stride or self.stride, 1],
          is_valid=True)
        output = operations.squeeze(max_pooled_img, 1)
        return output


class MaxPooling2DLayer(BaseLayer):
    __doc__ = '2D max pooling.\n\n    Args:\n        kernel_size (list, optional): Default kernel size. This is a list of\n            two elements, one per dimension. If either is not specified, the\n            default is to pool over the entire dimension\n            (default: ``[None, None]``)\n        default_strides (list, optional): Stride along each dimension\n            (list of size 2, defaults to ``[1, 1]``).\n    '

    def __init__(self, default_kernel_size=None, default_strides=None):
        super(MaxPooling2DLayer, self).__init__('maxpool1d')
        self.kernel_size = util._default_value(default_kernel_size, [None, None])
        self.strides = util._default_value(default_strides, [1, 1])

    def __call__(self, x, kernel_size=None, strides=None):
        """Max pooling over the first dimension.

        If either of the ``kernel_size`` elements is not specified, the
        pooling will be done over the full dimension (and the stride is
        ignored)

        Args:
            x (:py:class:`dynet.Expression`): Input image (3-d tensor) or
                matrix.
            kernel_size (list, optional): Size of the pooling kernel. If this
                is not specified, the default specified in the constructor is
                used.
            strides (list, optional): Stride along width/height. If this is not
                specified, the default specified in the constructor is used.

        Returns:
            :py:class:`dynet.Expression`: Pooled sequence.
        """
        x = util.list_to_matrix(x)
        x_dim, _ = x.dim()
        if len(x_dim) < 3:
            x = operations.unsqueeze(x, d=(-1))
        kernel_size = util._default_value(kernel_size, [None, None])
        kernel_size = [
         kernel_size[0] or self.kernel_size[0] or x_dim[0],
         kernel_size[1] or self.kernel_size[1] or x_dim[1]]
        strides = util._default_value(strides, [None, None])
        strides = [
         strides[0] or self.strides[0] or 1,
         strides[1] or self.strides[1] or 1]
        max_pooled_img = dy.maxpooling2d(x,
          ksize=kernel_size, stride=strides, is_valid=True)
        if len(x_dim) < 3:
            max_pooled_img = operations.squeeze(max_pooled_img, d=(-1))
        return max_pooled_img