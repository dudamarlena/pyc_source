# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib64/python3.6/site-packages/ioflo/aid/blending.py
# Compiled at: 2017-12-17 08:35:26
# Size of source mod 2**32: 2237 bytes
"""aiding.py constants and basic functions

"""
from __future__ import absolute_import, division, print_function
import math
from .sixing import *
from ..base import excepting
from .consoling import getConsole
console = getConsole()

def blend0(d=0.0, u=1.0, s=1.0):
    """
       blending function trapezoid
       d = delta x = xabs - xdr
       u = uncertainty radius of xabs estimate error
       s = tuning scale factor

       returns blend
    """
    d = float(abs(d))
    u = float(abs(u))
    s = float(abs(s))
    v = d - u
    if v >= s:
        b = 0.0
    else:
        if v <= 0.0:
            b = 1.0
        else:
            b = 1.0 - v / s
    return b


Blend0 = blend0

def blend1(d=0.0, u=1.0, s=1.0):
    """
       blending function pisig
       d = delta x = xabs - xdr
       u = uncertainty radius of xabs estimate error
       s = tuning scale factor

       returns blend
    """
    v = float(abs(u * s))
    a = float(abs(d))
    if a >= v or v == 0.0:
        b = 1.0
    else:
        if a < v / 2.0:
            b = 2.0 * (a * a) / (v * v)
        else:
            b = 1.0 - 2.0 * (a - v) * (a - v) / (v * v)
    return b


Blend1 = blend1

def blend2(d=0.0, u=1.0, s=5.0):
    """
       blending function gaussian
       d = delta x = xabs - xdr
       u = uncertainty radius of xabs estimate error
       s = tuning scale factor

       returns blend
    """
    d = float(d)
    u = float(u)
    s = float(abs(s))
    b = 1.0 - math.exp(-s * (d * d) / (u * u))
    return b


Blend2 = blend2

def blend3(d=0.0, u=1.0, s=0.05):
    """
       blending function polynomial
       d = delta x = xabs - xdr
       u = uncertainty radius of xabs estimate error
       s = tuning scale factor

       returns blend
    """
    d = float(d)
    u = float(u)
    s = min(1.0, float(abs(s)))
    b = 1.0 - s ** (d * d / (u * u))
    return b


Blend3 = blend3