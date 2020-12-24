# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\GrTiPy\Christoffel_n_ab.py
# Compiled at: 2018-11-01 04:17:59
# Size of source mod 2**32: 273 bytes
import numpy as np
from sympy import *

def Christoffel_n_ab(d, x, g, ginverse, n, a, b):
    summation = 0.0
    for i in range(d):
        summation = summation + ginverse[n][i] * (diff(g[i][a], x[b]) + diff(g[i][b], x[a]) - diff(g[a][b], x[i]))
        M = summation / 2

    return M