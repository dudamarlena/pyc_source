# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\GrTiPy\expansion_scalar.py
# Compiled at: 2018-11-06 17:23:16
# Size of source mod 2**32: 575 bytes
import numpy as np
from sympy import *

def Christoffel_n_ab(d, x, g, ginverse, n, a, b):
    summation = 0.0
    for i in range(d):
        summation = summation + ginverse[n][i] * (diff(g[i][a], x[b]) + diff(g[i][b], x[a]) - diff(g[a][b], x[i]))
        M = summation / 2

    return M


def expansion_scalar(d, x, g, ginverse, V):
    Summ = 0.0
    for i in range(d):
        Summ = Summ + diff(V[i], x[i])
        sm = 0.0
        for i in range(d):
            for v in range(d):
                sm = sm + Christoffel_n_ab(d, x, g, ginverse, i, v, i) * V[v]

    expan = Summ + sm
    return expan