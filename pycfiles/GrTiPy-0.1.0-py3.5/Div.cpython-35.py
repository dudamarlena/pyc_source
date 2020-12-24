# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\GrTiPy\Div.py
# Compiled at: 2018-10-27 14:05:35
# Size of source mod 2**32: 323 bytes
import numpy as np
from sympy.matrices import Matrix
from sympy import *
from GrTiPy import *

def Div(d, g, x, V):
    pro = 1
    for i in range(d):
        pro = pro * g[i][i]

    Summ = 0.0
    for i in range(d):
        Summ = Summ + 1 / sqrt(pro) * diff(pro * V[i], x[i])

    LL = print('Div.V=', simplify(Summ))
    return LL