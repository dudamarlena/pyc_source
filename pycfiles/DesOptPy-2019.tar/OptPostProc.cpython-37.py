# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/wehrle/opt/DesOptPy/DesOptPy/OptPostProc.py
# Compiled at: 2019-06-04 05:44:19
# Size of source mod 2**32: 1390 bytes
"""
Title:    OptPostProc.py
Author:   E. J. Wehrle
Date:     June 4, 2019
-------------------------------------------------------------------------------
Description:
Postprocessing of optimization problem via optimality check and shadow prices
-------------------------------------------------------------------------------
"""
import numpy as np
from numpy.linalg import pinv, norm

def CalcLagrangeMult(fNabla, gNabla):
    lam = -(fNabla @ pinv(gNabla)).T
    return lam


def CheckKKT(lam, fNabla, gNabla, g, kkteps=0.001):
    if np.size(g) == 0:
        OptResidual = fNabla
        kktOpt = np.abs(norm(fNabla)) < kkteps
    else:
        if np.size(lam) == 1:
            OptResidual = fNabla + float(lam) * gNabla
        else:
            OptResidual = fNabla + lam.T @ gNabla.T
        PrimalFeas = np.max(g) < kkteps
        ComplSlack = np.abs(g @ lam) < kkteps
        DualFeas = np.min(lam) > -kkteps
        kktOpt = bool(PrimalFeas * DualFeas * ComplSlack)
    Opt1Order = norm(OptResidual)
    kktMax = np.max(np.abs(OptResidual))
    return (kktOpt, Opt1Order, OptResidual, kktMax)


def CalcShadowPrice(lam, gc, gcType, DesVarNorm):
    SP = np.zeros(len(lam))
    for ii, lamii in enumerate(lam):
        if not gc[ii] == 0.0:
            if gcType[ii] == 'Bound':
                if DesVarNorm in (None, 'None', False):
                    SP[ii] = lamii
            SP[ii] = lamii / gc[ii]

    return SP