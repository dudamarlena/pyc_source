# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\GrTiPy\Ricci_Tensor_All.py
# Compiled at: 2018-11-01 05:29:49
# Size of source mod 2**32: 1504 bytes
import numpy as np
from sympy import *

def Ricci_Tensor_All(d, x, g, ginverse):
    christoffel = [[[[] for k in range(d)] for j in range(d)] for i in range(d)]
    for n in range(d):
        for a in range(d):
            for b in range(d):
                summation = 0.0
                for i in range(d):
                    summation = summation + ginverse[n][i] * (diff(g[i][a], x[b]) + diff(g[i][b], x[a]) - diff(g[a][b], x[i]))

                christoffel[n][a][b] = summation / 2

    Riemann = [[[[[] for l in range(d)] for k in range(d)] for j in range(d)] for i in range(d)]
    for n in range(d):
        for a in range(d):
            for b in range(d):
                for c in range(d):
                    parials = diff(christoffel[n][a][c], x[b]) - diff(christoffel[n][a][b], x[c])
                    summation = 0.0
                    for i in range(d):
                        summation = summation + christoffel[n][b][i] * christoffel[i][a][c] - christoffel[n][c][i] * christoffel[i][a][b]

                    Riemann[n][a][b][c] = parials + summation

    Ricci = [[[] for j in range(d)] for i in range(d)]
    for a in range(d):
        for c in range(d):
            summation = 0.0
            for i in range(d):
                summation = summation + simplify(Riemann[i][a][i][c])

            Ricci[a][c] = simplify(summation)

    for a in range(d):
        for c in range(d):
            Ricc = print('Ricci[', x[a], ',', x[c], ']=', simplify(Ricci[a][c]))

    return Ricc