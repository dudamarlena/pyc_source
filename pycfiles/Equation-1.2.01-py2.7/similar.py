# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\Equation\similar.py
# Compiled at: 2014-06-12 23:02:16
r"""
.. _similar-module:

Equation.similar Module
=======================

Provides support for similar type comparsion, and allows the tolerance to be changed

Comparsions work by detriming if the following is true

.. math::
    
    1-\frac{\min(A,B)}{\max(A,B)}\leq tolerance
    
If it is true the :math:`A` and :math:`B` are considered to be equal

This module only needs to be imported if you need to change the tolerance for similarlity
tests, otherwise you just need to use the similarlity operators in your expression

.. code-block:: python

    >>> from Equation import Expression
    >>> fn = Expression("x ~ y")
    >>> fn(1,1.1)
    False
    >>> fn(1,1.00001)
    True
    >>> fn(1,1.001)
    False
    >>> from Equation.similar import set_tol
    >>> set_tol(1e-2)
    >>> fn(1,1.1)
    False
    >>> fn(1,1.00001)
    True
    >>> fn(1,1.001)
    True

By default the tolerance is :math:`10^{-5}` Hence 1.001 isn't condisered similar to 1, but by
changing the tolerance to :math:`10^{-2}`, 1.001 is condisered similar to 1
"""
_tol = 1e-05

def sim(a, b):
    global _tol
    if a == b:
        return True
    else:
        if a == 0 or b == 0:
            return False
        if a < b:
            return 1 - a / b <= _tol
        return 1 - b / a <= _tol


def nsim(a, b):
    if a == b:
        return False
    else:
        if a == 0 or b == 0:
            return True
        if a < b:
            return 1 - a / b > _tol
        return 1 - b / a > _tol


def gsim(a, b):
    if a >= b:
        return True
    return 1 - a / b <= _tol


def lsim(a, b):
    if a <= b:
        return True
    return 1 - b / a <= _tol


def set_tol(value=1e-05):
    r"""Set Error Tolerance
    
    Set the tolerance for detriming if two numbers are simliar, i.e
    :math:`\left|\frac{a}{b}\right| = 1 \pm tolerance`
    
    Parameters
    ----------
    value: float
        The Value to set the tolerance to show be very small as it respresents the
        percentage of acceptable error in detriming if two values are the same.
    """
    global _tol
    if isinstance(value, float):
        _tol = value
    else:
        raise TypeError(type(value))