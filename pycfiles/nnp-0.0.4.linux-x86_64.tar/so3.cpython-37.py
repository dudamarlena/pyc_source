# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/hostedtoolcache/Python/3.7.5/x64/lib/python3.7/site-packages/nnp/so3.py
# Compiled at: 2019-11-24 03:15:15
# Size of source mod 2**32: 3309 bytes
"""
SO(3) Lie Group Operations
==========================

The module ``nnp.so3`` contains tools to rotate point clouds in 3D space.
"""
import torch
import scipy.linalg as scipy_expm
from torch import Tensor
levi_civita = torch.zeros(3, 3, 3)
levi_civita[(0, 1, 2)] = levi_civita[(1, 2, 0)] = levi_civita[(2, 0, 1)] = 1
levi_civita[(0, 2, 1)] = levi_civita[(2, 1, 0)] = levi_civita[(1, 0, 2)] = -1

def expm(matrix: Tensor) -> Tensor:
    ndarray = matrix.detach().cpu().numpy()
    return torch.from_numpy(scipy_expm(ndarray)).to(matrix)


def rotate_along(axis: Tensor) -> Tensor:
    r"""Compute group elements of rotating along an axis passing origin.

    Arguments:
        axis: a vector (x, y, z) whose direction specifies the axis of the rotation,
            length specifies the radius to rotate, and sign specifies clockwise
            or anti-clockwise.

    Return:
        the rotational matrix :math:`\exp{\left(\theta W\right)}`.
    """
    W = torch.einsum('ijk,j->ik', levi_civita.to(axis), axis)
    return expm(W)