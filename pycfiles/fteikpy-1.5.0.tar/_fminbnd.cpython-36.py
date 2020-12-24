# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\keurf\Documents\GitHub\FTeikPy\examples\raytracer\_fminbnd.py
# Compiled at: 2018-02-06 17:58:23
# Size of source mod 2**32: 746 bytes
"""
Author: Keurfon Luu <keurfon.luu@mines-paristech.fr>
License: MIT
"""
import numpy as np
__all__ = [
 'fminbnd']

def fminbnd(f, lower, upper, eps=0.0001, args=(), kwargs={}):
    func = lambda x: f(x, *args, **kwargs)
    gr = 0.6180339887498948
    x1 = np.array([lower])
    x2 = np.array([upper])
    x3 = x2 - gr * (x2 - x1)
    x4 = x1 + gr * (x2 - x1)
    while np.abs(x3 - x4) > eps:
        if func(x3) < func(x4):
            x2 = x4
        else:
            x1 = x3
        x3 = x2 - gr * (x2 - x1)
        x4 = x1 + gr * (x2 - x1)

    xmin = 0.5 * (x1 + x2)
    return (xmin, func(xmin))