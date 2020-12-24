# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\GrTiPy\Scalar_Brans_Dicke_field_Equation.py
# Compiled at: 2018-10-27 14:37:42
# Size of source mod 2**32: 602 bytes
from GrTiPy.Tr import Tr
import GrTiPy.Tr as Tr
from GrTiPy.Tr import Tr
import numpy as np
from sympy import *
import numpy as np, sympy as sp
from sympy import *

def Scalar_Brans_Dicke_field_Equation(d, x, g, ginverse, psi, T):
    lamda, omaga, pi = symbols('lamda omaga pi')
    pro = 1
    for i in range(d):
        pro = -pro * g[i][i]

    sum = 0
    for k in range(d):
        for i in range(d):
            sum = sum + 1 / sqrt(pro) * diff(sqrt(pro) * ginverse[k][i] * diff(psi, x[i]), x[k])

    Lap = expand(sum) - 8 * pi / (3 + 2 * omaga) * Tr(T) + 2 * lamda * psi / (3 + 2 * omaga)
    return Lap