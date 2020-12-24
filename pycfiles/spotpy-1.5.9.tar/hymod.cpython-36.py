# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\houska-t\Desktop\github\spotpy\spotpy\examples\hymod_python\hymod.py
# Compiled at: 2018-11-01 10:23:32
# Size of source mod 2**32: 2724 bytes
from numba import jit

@jit
def hymod(Precip, PET, cmax, bexp, alpha, Rs, Rq):
    """
    See https://www.proc-iahs.net/368/180/2015/piahs-368-180-2015.pdf for a scientific paper.

    :param cmax:
    :param bexp:
    :param alpha:
    :param Rs:
    :param Rq:
    :return: Dataset of water in hymod (has to be calculated in litres)
    :rtype: list
    """
    x_loss = 0.0
    x_slow = 2.3503 / (Rs * 22.5)
    x_slow = 0
    x_quick = [
     0, 0, 0]
    t = 0
    outflow = []
    output = []
    while t <= len(Precip) - 1:
        Pval = Precip[t]
        PETval = PET[t]
        ER1, ER2, x_loss = excess(x_loss, cmax, bexp, Pval, PETval)
        ET = ER1 + ER2
        UQ = alpha * ET
        US = (1 - alpha) * ET
        x_slow, QS = linres(x_slow, US, Rs)
        inflow = UQ
        for i in range(3):
            x_quick[i], outflow = linres(x_quick[i], inflow, Rq)
            inflow = outflow

        output.append(QS + outflow)
        t = t + 1

    return output


@jit
def power(X, Y):
    X = abs(X)
    return X ** Y


@jit
def linres(x_slow, inflow, Rs):
    x_slow = (1 - Rs) * x_slow + (1 - Rs) * inflow
    outflow = Rs / (1 - Rs) * x_slow
    return (x_slow, outflow)


@jit
def excess(x_loss, cmax, bexp, Pval, PETval):
    xn_prev = x_loss
    ct_prev = cmax * (1 - power(1 - (bexp + 1) * xn_prev / cmax, 1 / (bexp + 1)))
    ER1 = max(Pval - cmax + ct_prev, 0.0)
    Pval = Pval - ER1
    dummy = min((ct_prev + Pval) / cmax, 1)
    xn = cmax / (bexp + 1) * (1 - power(1 - dummy, bexp + 1))
    ER2 = max(Pval - (xn - xn_prev), 0)
    evap = (1 - (cmax / (bexp + 1) - xn) / (cmax / (bexp + 1))) * PETval
    xn = max(xn - evap, 0)
    return (
     ER1, ER2, xn)