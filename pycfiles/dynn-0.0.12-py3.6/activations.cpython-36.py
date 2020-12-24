# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\dynn\activations.py
# Compiled at: 2018-09-12 18:51:16
# Size of source mod 2**32: 1213 bytes
"""
Activation functions
====================

Common activation functions for neural networks.

Most of those are wrappers around standard dynet operations
(eg. ``rectify`` -> ``relu``)
"""
import dynet as dy

def identity(x):
    """The identity function

    :math:`y=x`

    Args:
        x (:py:class:`dynet.Expression`): Input expression

    Returns:
        :py:class:`dynet.Expression`: :math:`x`
    """
    return x


def tanh(x):
    r"""The hyperbolic tangent function

    :math:`y=\tanh(x)`

    Args:
        x (:py:class:`dynet.Expression`): Input expression

    Returns:
        :py:class:`dynet.Expression`: :math:`\tanh(x)`
    """
    return dy.tanh(x)


def sigmoid(x):
    r"""The sigmoid function

    :math:`y=\frac{1}{1+e^{-x}}`

    Args:
        x (:py:class:`dynet.Expression`): Input expression

    Returns:
        :py:class:`dynet.Expression`: :math:`\frac{1}{1+e^{-x}}`
    """
    return dy.logistic(x)


def relu(x):
    r"""The REctified Linear Unit

    :math:`y=\max(0,x)`

    Args:
        x (:py:class:`dynet.Expression`): Input expression

    Returns:
        :py:class:`dynet.Expression`: :math:`\max(0,x)`
    """
    return dy.rectify(x)