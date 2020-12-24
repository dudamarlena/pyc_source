# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\GrTiPy\Christoffel_All.py
# Compiled at: 2018-11-01 04:07:43
# Size of source mod 2**32: 873 bytes
import numpy as np
from sympy import *

def Christoffel_All(d, x, g, ginverse):
    christoffel = [[[[] for k in range(d)] for j in range(d)] for i in range(d)]
    christoffel = [[[[] for k in range(d)] for j in range(d)] for i in range(d)]
    for n in range(d):
        for a in range(d):
            for b in range(d):
                summation = 0.0
                for i in range(d):
                    summation = summation + ginverse[n][i] * (diff(g[i][a], x[b]) + diff(g[i][b], x[a]) - diff(g[a][b], x[i]))

                christoffel[n][a][b] = summation / 2

    for n in range(0, d):
        for a in range(0, d):
            for b in range(0, d):
                M = print('christoffel[', x[n], ',', x[a], ',', x[b], ']=', expand(simplify(christoffel[n][a][b])))

    return M