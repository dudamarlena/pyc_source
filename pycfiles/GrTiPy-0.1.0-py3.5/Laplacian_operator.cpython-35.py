# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\GrTiPy\Laplacian_operator.py
# Compiled at: 2018-10-23 15:43:07
# Size of source mod 2**32: 383 bytes
import numpy as np
from sympy import *
from GrTiPy.Det import Det
from GrTiPy.Det import Det
import GrTiPy.Det as Det

def Laplacian_operator(d, x, g, ginverse, psi):
    pro = -Det(g)
    sum = 0
    for k in range(d):
        for i in range(d):
            sum = sum + 1 / sqrt(pro) * diff(sqrt(pro) * ginverse[k][i] * diff(psi, x[i]), x[k])

    Lap = expand(sum)
    return Lap