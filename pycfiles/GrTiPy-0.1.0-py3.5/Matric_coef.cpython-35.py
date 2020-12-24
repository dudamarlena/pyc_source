# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\GrTiPy\Matric_coef.py
# Compiled at: 2018-10-23 15:03:39
# Size of source mod 2**32: 371 bytes
"""
Created on Sun Oct 14 00:12:59 2018

@author: Windows 7
"""
import numpy as np
from sympy import *
from sympy.matrices import Matrix

def Matric_coef(d, x, y):
    for i in range(d):
        for j in range(d):
            m = diff(y, x[i]).dot(diff(y, x[j]))
            F = print('G(', x[i], ',', x[j], ')=', simplify(m))

    return F