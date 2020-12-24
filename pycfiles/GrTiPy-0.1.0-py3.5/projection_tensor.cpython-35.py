# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\GrTiPy\projection_tensor.py
# Compiled at: 2018-10-25 20:36:52
# Size of source mod 2**32: 725 bytes
import numpy as np
from sympy import *

def projection_tensor(d, g, u_sup):
    uscr = [[] for i in range(d)]
    uvv = [[[] for l in range(d)] for k in range(d)]
    HH = [[[] for l in range(d)] for k in range(d)]
    for i in range(d):
        usum = 0.0
        for j in range(d):
            usum = usum + g[i][j] * u_sup[j]

        uscr[i] = usum

    for i in range(d):
        for j in range(d):
            s = uscr[i] * uscr[j]
            uvv[i][j] = s

    for i in range(d):
        for j in range(d):
            h = g[i][j] + uvv[i][j]
            HH[i][j] = h

    for a in range(d):
        for b in range(d):
            HIJ = print('projection_tensor(', a, ',', b, ')=', HH[a][b])

    return HIJ