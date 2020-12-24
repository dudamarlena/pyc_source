# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\GrTiPy\Spin_connection_first.py
# Compiled at: 2018-11-02 12:44:21
# Size of source mod 2**32: 878 bytes
import numpy as np
from sympy import *
import sympy as sp

def C_n_ab(d, x, g, ginverse, n, a, b):
    summation = 0.0
    for i in range(d):
        summation = summation + ginverse[n][i] * diff(g[i][a], x[b])
        M = summation

    return M


def Spin_connection_first(d, x, e, ein):
    omag = [[[[] for k in range(d)] for j in range(d)] for i in range(d)]
    for n in range(d):
        for a in range(d):
            for b in range(d):
                summ = 0.0
                for r in range(d):
                    for v in range(d):
                        summ = summ + (e[r][a] * ein[b][v] * C_n_ab(d, x, e, ein, v, n, r) - e[v][a] * diff(ein[v][a], x[n]))

                omag[n][a][b] = summ

    for n in range(d):
        for a in range(d):
            for b in range(d):
                M = print('omag[', x[n], ',', x[a], ',', x[b], ']=', simplify(omag[n][a][b]))

    return M