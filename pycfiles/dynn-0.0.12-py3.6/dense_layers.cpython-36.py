# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\dynn\layers\dense_layers.py
# Compiled at: 2018-09-17 17:37:27
# Size of source mod 2**32: 4828 bytes
"""
Densely connected layers
========================
"""
import dynet as dy
from ..parameter_initialization import ZeroInit
from .base_layers import ParametrizedLayer

class DenseLayer(ParametrizedLayer):
    __doc__ = 'Densely connected layer\n\n    :math:`y=f(Wx+b)`\n\n    Args:\n        pc (:py:class:`dynet.ParameterCollection`): Parameter collection to\n            hold the parameters\n        input_dim (int): Input dimension\n        output_dim (int): Output dimension\n        activation (function, optional): activation function\n            (default: :py:class:`dynet.tanh`)\n        dropout (float, optional):  Dropout rate (default 0)\n        nobias (bool, optional): Omit the bias (default ``False``)\n    '

    def __init__(self, pc, input_dim, output_dim, activation=dy.tanh, dropout=0.0, nobias=False):
        super(DenseLayer, self).__init__(pc, 'dense')
        self.W_p = self.pc.add_parameters((output_dim, input_dim), name='W')
        if not nobias:
            self.b_p = self.pc.add_parameters(output_dim,
              name='b', init=(ZeroInit()))
        self.dropout = dropout
        self.nobias = nobias
        self.activation = activation

    def init(self, test=False, update=True):
        """Initialize the layer before performing computation

        Args:
            test (bool, optional): If test mode is set to ``True``,
                dropout is not applied (default: ``True``)
            update (bool, optional): Whether to update the parameters
                (default: ``True``)
        """
        self.W = self.W_p.expr(update)
        if not self.nobias:
            self.b = self.b_p.expr(update)
        self.test = test

    def __call__(self, x):
        """Forward pass

        Args:
            x (:py:class:`dynet.Expression`): Input expression (a vector)

        Returns:
            :py:class:`dynet.Expression`: :math:`y=f(Wx+b)`
        """
        if not self.test:
            if self.dropout > 0:
                x = dy.dropout(x, self.dropout)
        else:
            if self.nobias:
                self.h = self.W * x
            else:
                self.h = self.activation(dy.affine_transform([self.b, self.W, x]))
        return self.h


class GatedLayer(ParametrizedLayer):
    __doc__ = 'Gated linear layer:\n\n    :math:`y=(W_ox+b_o)\\circ \\sigma(W_gx+b_g)`\n\n    Args:\n        pc (:py:class:`dynet.ParameterCollection`): Parameter collection to\n            hold the parameters\n        input_dim (int): Input dimension\n        output_dim (int): Output dimension\n        activation (function, optional): activation function\n            (default: :py:class:`dynet.tanh`)\n        dropout (float, optional):  Dropout rate (default 0)\n    '

    def __init__(self, pc, input_dim, output_dim, activation=dy.tanh, dropout=0.0):
        super(GatedLayer, self).__init__(pc, 'gated')
        self.input_dim = input_dim
        self.output_dim = output_dim
        self.dropout = dropout
        self.activation = activation
        self.Wo_p = self.pc.add_parameters((output_dim, input_dim), name='Wo')
        self.bo_p = self.pc.add_parameters(output_dim,
          name='bo', init=(ZeroInit()))
        self.Wg_p = self.pc.add_parameters((output_dim, input_dim), name='Wg')
        self.bg_p = self.pc.add_parameters(output_dim,
          name='bg', init=(ZeroInit()))

    def init(self, test=False, update=True):
        """Initialize the layer before performing computation

        Args:
            test (bool, optional): If test mode is set to ``True``,
                dropout is not applied (default: ``True``)
            update (bool, optional): Whether to update the parameters
                (default: ``True``)
        """
        self.Wo = self.Wo_p.expr(update)
        self.bo = self.bo_p.expr(update)
        self.Wg = self.Wg_p.expr(update)
        self.bg = self.bg_p.expr(update)
        self.test = test

    def __call__(self, x):
        r"""Forward pass

        Args:
            x (:py:class:`dynet.Expression`): Input expression (a vector)

        Returns:
            :py:class:`dynet.Expression`:
                :math:`y=(W_ox+b_o)\circ \sigma(W_gx+b_g)`
        """
        self.o = self.activation(dy.affine_transform([self.bo, self.Wo, x]))
        self.g = dy.logistic(dy.affine_transform([self.bg, self.Wg, x]))
        return dy.cmult(self.g, self.o)