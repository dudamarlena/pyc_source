# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\GrTiPy\Geodesics.py
# Compiled at: 2018-10-26 13:36:57
# Size of source mod 2**32: 872 bytes
import numpy as np
from sympy import *

def Geodesics(d, x, g, ginverse):
    christoffel = [[[[] for k in range(d)] for j in range(d)] for i in range(d)]
    f = symbols('f')
    for n in range(d):
        for a in range(d):
            for b in range(d):
                summation = 0.0
                for i in range(d):
                    summation = summation + ginverse[n][i] * (diff(g[i][a], x[b]) + diff(g[i][b], x[a]) - diff(g[a][b], x[i]))

                christoffel[n][a][b] = summation / 2

    geod = [[] for k in range(d)]
    for i in range(d):
        sum = 0.0
        for j in range(d):
            for k in range(d):
                sum = sum + christoffel[i][j][k] * f(x[j]) * f(x[k])

        geod[i] = -sum
        Ge = print('d', f(x[i]), '/ ds=', simplify(geod[i]))

    return Ge