# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\dynn\parameter_initialization.py
# Compiled at: 2018-09-12 18:53:12
# Size of source mod 2**32: 1298 bytes
"""
Parameter initialization
========================

Some of those are just less verbose versions of
dynet's ``PyInitializer`` s
"""
import numpy as np, dynet as dy

def OneInit():
    """Initialize with :math:`1`

    Returns:
        :py:class:`dynet.PyInitializer`: ``dy.ConstInitializer(1)``
    """
    return dy.ConstInitializer(1)


def ZeroInit():
    """Initialize with :math:`0`

    Returns:
        :py:class:`dynet.PyInitializer`: dy.ConstInitializer(0)
    """
    return dy.ConstInitializer(0)


def UniformInit(scale=1.0):
    """Uniform initialization between ``-scale`` and ``scale``

    Args:
        scale (float): Scale of the distribution

    Returns:
        :py:class:`dynet.PyInitializer`:
            ``dy.UniformInitializer(scale)``
    """
    return dy.UniformInitializer(scale)


def NormalInit(mean=0, std=1):
    r"""Gaussian initialization

    Args:
        mean (int, optional): Mean (default: 0.0)
        std (int, optional): Standard deviation (:math:`\neq` variance)
            (default: 1.0)

    Returns:
        :py:class:`dynet.PyInitializer`:
            ``dy.NormalInitializer(mean, sqrt(std))``
    """
    return dy.NormalInitializer(mean, np.sqrt(std))