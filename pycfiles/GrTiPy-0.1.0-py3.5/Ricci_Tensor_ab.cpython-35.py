# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\GrTiPy\Ricci_Tensor_ab.py
# Compiled at: 2018-11-01 06:32:40
# Size of source mod 2**32: 908 bytes
import numpy as np
from sympy import *

def Christoffel_n_ab(d, x, g, ginverse, n, a, b):
    summation = 0.0
    for i in range(d):
        summation = summation + ginverse[n][i] * (diff(g[i][a], x[b]) + diff(g[i][b], x[a]) - diff(g[a][b], x[i]))
        M = summation / 2

    return M


def Riemann_nabc(d, x, g, ginverse, n, a, b, c):
    parials = diff(Christoffel_n_ab(d, x, g, ginverse, n, a, c), x[b]) - diff(Christoffel_n_ab(d, x, g, ginverse, n, a, b), x[c])
    summation = 0.0
    for i in range(d):
        summation = summation + Christoffel_n_ab(d, x, g, ginverse, n, b, i) * Christoffel_n_ab(d, x, g, ginverse, i, a, c) - Christoffel_n_ab(d, x, g, ginverse, n, c, i) * Christoffel_n_ab(d, x, g, ginverse, i, a, b)

    Rie = parials + summation
    return Rie


def Ricci_Tensor_ab(d, x, g, ginverse, a, c):
    summation = 0.0
    for i in range(d):
        summation = summation + Riemann_nabc(d, x, g, ginverse, i, a, i, c)

    RiiR = simplify(summation)
    return RiiR