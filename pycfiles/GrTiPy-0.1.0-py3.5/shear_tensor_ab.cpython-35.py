# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\GrTiPy\shear_tensor_ab.py
# Compiled at: 2018-11-07 14:27:23
# Size of source mod 2**32: 1366 bytes
import numpy as np
from sympy import *

def U_i(d, g, V, i):
    uu = 0.0
    for j in range(d):
        uu = uu + V[j] * g[i][j]

    us = uu
    return us


def Christoffel_n_ab(d, x, g, ginverse, n, a, b):
    summation = 0.0
    for i in range(d):
        summation = summation + ginverse[n][i] * (diff(g[i][a], x[b]) + diff(g[i][b], x[a]) - diff(g[a][b], x[i]))
        M = summation / 2

    return M


def projection_tensor_ij(d, g, V, i, j):
    h = g[i][j] + U_i(d, g, V, i) * U_i(d, g, V, j)
    return h


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


def h(d, g, ginverse, V, i, j):
    hh = 0.0
    for k in range(d):
        hh = hh + ginverse[i][k] * projection_tensor_ij(d, g, V, k, j)

    hhh = hh
    return hh


def contrD(d, x, g, ginverse, V, a, b):
    fir = diff(U_i(d, g, V, a), x[b])
    si = 0.0
    for n in range(d):
        si = si + Christoffel_n_ab(d, x, g, ginverse, n, a, b) * U_i(d, g, V, n)

    con = fir - si
    return con


def shear_tensor_ab(d, x, g, ginverse, V, a, b):
    sher = contrD(d, x, g, ginverse, V, a, b) + contrD(d, x, g, ginverse, V, b, a)
    sher1 = sher / 2 - 0.3333333333333333 * expansion_scalar(d, x, g, ginverse, V) * projection_tensor_ij(d, g, V, a, b)
    return sher1