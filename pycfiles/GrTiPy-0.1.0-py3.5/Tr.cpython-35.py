# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\GrTiPy\Tr.py
# Compiled at: 2018-10-19 15:50:48
# Size of source mod 2**32: 128 bytes
import numpy as np, sympy as sp
from sympy import *

def Tr(metric):
    return np.array(sp.Matrix(metric).trace())