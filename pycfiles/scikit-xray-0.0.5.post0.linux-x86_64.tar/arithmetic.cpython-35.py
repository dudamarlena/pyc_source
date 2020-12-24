# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/edill/mc/lib/python3.5/site-packages/skxray/core/arithmetic.py
# Compiled at: 2016-03-04 05:19:32
# Size of source mod 2**32: 7064 bytes
"""
The included functions supplement the logical operations currently provided
in numpy in order to provide a complete set of logical operations.
"""
from __future__ import absolute_import, division, print_function
import six
from numpy import logical_and, logical_or, logical_not, logical_xor, add, subtract, multiply, divide
__all__ = [
 'add', 'subtract', 'multiply', 'divide', 'logical_and',
 'logical_or', 'logical_nor', 'logical_xor', 'logical_not',
 'logical_sub', 'logical_nand']

def logical_nand(x1, x2, out=None):
    """Computes the truth value of NOT (x1 AND x2) element wise.

    This function enables the computation of the LOGICAL_NAND of two image or
    volume data sets. This function enables easy isolation of all data points
    NOT INCLUDED IN BOTH SOURCE DATA SETS. This function can be used for data
    comparison, material isolation, noise removal, or mask
    application/generation.

    Parameters
    ----------
    x1, x2 : array-like
        Input arrays. `x1` and `x2` must be of the same shape.

    output : array-like
        Boolean result with the same shape as `x1` and `x2` of the logical
        operation on corresponding elements of `x1` and `x2`.

    Returns
    -------
    output : {ndarray, bool}
        Boolean result with the same shape as `x1` and `x2` of the logical
        NAND operation on corresponding elements of `x1` and `x2`.

    Example
    -------
    >>> x1 = [[0,0,1,0,0], [2,1,1,1,2], [2,0,1,0,2]]
    >>> x2 = [[0,0,0,0,0], [2,1,1,1,2], [0,0,0,0,0]]
    >>> logical_nand(x1, x2)
    array([[ True,  True,  True,  True,  True],
           [False, False, False, False, False],
           [ True,  True,  True,  True,  True]], dtype=bool)

    """
    return logical_not(logical_and(x1, x2, out), out)


def logical_nor(x1, x2, out=None):
    """Compute truth value of NOT (x1 OR x2)) element wise.

    This function enables the computation of the LOGICAL_NOR of two image or
    volume data sets. This function enables easy isolation of all data points
    NOT INCLUDED IN EITHER OF THE SOURCE DATA SETS. This function can be used
    for data comparison, material isolation, noise removal, or mask
    application/generation.

    Parameters
    ----------
    x1, x2 : array-like
        Input arrays. `x1` and `x2` must be of the same shape.

    output : array-like
        Boolean result with the same shape as `x1` and `x2` of the logical
        operation on corresponding elements of `x1` and `x2`.

    Returns
    -------
    output : {ndarray, bool}
        Boolean result with the same shape as `x1` and `x2` of the logical
        NOR operation on corresponding elements of `x1` and `x2`.

    Example
    -------
    >>> x1 = [[0,0,1,0,0], [2,1,1,1,2], [2,0,1,0,2]]
    >>> x2 = [[0,0,0,0,0], [2,1,1,1,2], [0,0,0,0,0]]
    >>> logical_nor(x1, x2)
    array([[ True,  True, False,  True,  True],
           [False, False, False, False, False],
           [False,  True, False,  True, False]], dtype=bool)
    """
    return logical_not(logical_or(x1, x2, out), out)


def logical_sub(x1, x2, out=None):
    """Compute truth value of x1 AND (NOT (x1 AND x2)) element wise.

    This function enables LOGICAL SUBTRACTION of one binary image or volume data
    set from another. This function can be used to remove phase information,
    interface boundaries, or noise, present in two data sets, without having to
    worry about mislabeling of pixels which would result from arithmetic
    subtraction. This function will evaluate as true for all "true" voxels
    present ONLY in Source Dataset 1. This function can be used for data
    cleanup, or boundary/interface analysis.

    Parameters
    ----------
    x1, x2 : array-like
        Input arrays. `x1` and `x2` must be of the same shape.

    output : array-like
        Boolean result with the same shape as `x1` and `x2` of the logical
        operation on corresponding elements of `x1` and `x2`.

    Returns
    -------
    output : {ndarray, bool}
        Boolean result with the same shape as `x1` and `x2` of the logical
        SUBTRACT operation on corresponding elements of `x1` and `x2`.

    Example
    -------
    >>> x1 = [[0,0,1,0,0], [2,1,1,1,2], [2,0,1,0,2]]
    >>> x2 = [[0,0,0,0,0], [2,1,1,1,2], [0,0,0,0,0]]
    >>> logical_sub(x1, x2)
    array([[False, False,  True, False, False],
           [False, False, False, False, False],
           [ True, False,  True, False,  True]], dtype=bool)
    """
    return logical_and(x1, logical_not(logical_and(x1, x2, out), out), out)