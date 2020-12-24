# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\dynn\layers\normalization_layers.py
# Compiled at: 2018-09-13 15:05:55
# Size of source mod 2**32: 1690 bytes
"""
Normalization layers
====================
"""
import dynet as dy
from ..parameter_initialization import ZeroInit, OneInit
from .base_layers import ParametrizedLayer

class LayerNormalization(ParametrizedLayer):
    __doc__ = 'Layer normalization layer:\n\n    :math:`y=\\frac{g}{\\sigma(x)}\\cdot(x-\\mu(x)+b)`\n\n    Args:\n        input_dim (int): Input dimension\n        pc (:py:class:`dynet.ParameterCollection`): Parameter collection to\n            hold the parameters\n    '

    def __init__(self, input_dim, pc):
        super(LayerNormalization, self).__init__(pc, 'layer-norm')
        self.input_dim = input_dim
        self.gain_p = self.pc.add_parameters(input_dim,
          name='gain', init=(OneInit()))
        self.bias_p = self.pc.add_parameters(input_dim,
          name='bias', init=(ZeroInit()))

    def init(self, update=True):
        """Initialize the layer before performing computation

        Args:
            update (bool, optional): Whether to update the parameters
                (default: ``True``)
        """
        self.gain = self.gain_p.expr(update)
        self.bias = self.bias_p.expr(update)

    def __call__(self, x):
        r"""Layer-normalize the input

        Args:
            x (:py:class:`dynet.Expression`): Input expression

        Returns:
            :py:class:`dynet.Expression`:
                :math:`y=\frac{g}{\sigma(x)}\cdot(x-\mu(x)+b)`
        """
        self.output = dy.layer_norm(x, self.gain, self.bias)
        return self.output