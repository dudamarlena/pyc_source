# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/krm58/Desktop/OneDrive/Documents/Duke/Statistics/Biclustering-SSVD/Biclustering-SSVD/ssvd_fast.py
# Compiled at: 2017-05-01 16:15:33
# Size of source mod 2**32: 4043 bytes
import pandas as pd, numpy as np
from numba import jit
from matplotlib import pyplot as plt
from sklearn.datasets import make_checkerboard
from sklearn.datasets import samples_generator as sg
from sklearn.cluster.bicluster import SpectralBiclustering
from sklearn.metrics import consensus_score

@jit(nopython=True)
def gt(a, b):
    """
    Helper function to compare floats
    a and b must be the same length
    """
    result = np.zeros((len(a)), dtype=(np.float64))
    for i in range(len(a)):
        result[i] = a[i] >= b[i]

    return result


@jit(nopython=True)
def updateU(Bu, tmpI, n, d, ru, tu, winu, z, X, v1, sigsq):
    for i in range(0, ru):
        luc = tu[tmpI[i]]
        paralambda = luc / winu[(winu != 0)]
        tmp = np.multiply(np.sign(z[(winu != 0)]), gt(np.abs(z[(winu != 0)]), paralambda))
        uc = np.multiply(tmp, np.abs(z[(winu != 0)]) - paralambda)
        acc = np.zeros(len(v1))
        acccum = 0
        for j in range(len(uc)):
            for k in range(len(v1)):
                acc[k] = acc[k] + (X[j][k] - uc[j] * v1[k]) ** 2

        for c in range(len(v1)):
            acccum += acc[c]

        Bu[i] = acccum / sigsq + (i + 1) * np.log(n * d)

    return Bu


@jit(nopython=True)
def updateV(Bv, tmpI, n, d, rv, tv, winv, z, u0, X, sigsq):
    for i in range(0, rv):
        lvc = tv[tmpI[i]]
        paralambda = lvc / winv[(winv != 0)]
        tmp = np.multiply(np.sign(z[(winv != 0)]), gt(np.abs(z[(winv != 0)]), paralambda))
        vc = np.multiply(tmp, np.abs(z[(winv != 0)]) - paralambda)
        acc = np.zeros(len(vc))
        acccum = 0
        for j in range(len(u0)):
            for k in range(len(vc)):
                acc[k] = acc[k] + (X[j][k] - u0[j] * vc[k]) ** 2

        for c in range(len(vc)):
            acccum += acc[c]

        Bv[i] = acccum / sigsq + (i + 1) * np.log(n * d)

    return Bv


def ssvd(X, param=None):
    n, d = X.shape
    threu = 1
    threv = 1
    gamu = 0
    gamv = 0
    t1, t2, t3 = np.linalg.svd(X)
    t3 = t3.T
    u0 = t1[:, 0]
    v0 = t3[:, 0]
    merr = 0.0001
    niter = 100
    ud = 1
    vd = 1
    iters = 0
    SST = np.sum(X ** 2)
    a = 3.7
    while ud > merr or vd > merr:
        iters = iters + 1
        z = np.matmul(X.T, u0)
        winv = np.abs(z) ** gamv
        sigsq = (SST - np.sum(z ** 2)) / (n * d - d)
        tv = np.sort(np.append(np.abs(z ** winv), 0))
        rv = np.sum(tv > 0)
        Bv = np.ones(d + 1) * np.Inf
        tmpI = np.arange(d - 1, -1, -1)
        Bv = updateV(Bv, tmpI, n, d, rv, tv, winv, z, u0, X, sigsq)
        Iv = np.argmin(Bv) + 1
        temp = np.sort(np.append(np.abs(np.multiply(z, winv)), 0))
        lv = temp[(d - Iv)]
        paralambda = np.multiply(lv, winv[(winv != 0)])
        tmp = np.multiply(np.sign(z[(winv != 0)]), gt(np.abs(z[(winv != 0)]), paralambda))
        v1 = np.multiply(tmp, np.abs(z[(winv != 0)]) - paralambda)
        v1 = v1 / np.sqrt(np.sum(v1 ** 2))
        z = np.matmul(X, v1)
        winu = np.abs(z) ** gamu
        sigsq = (SST - np.sum(z ** 2)) / (n * d - n)
        tu = np.sort(np.append(np.abs(np.multiply(z, winu)), 0))
        ru = np.sum((tu > 0).astype('int'))
        Bu = np.ones(n + 1) * np.Inf
        tmpI = np.arange(n - 1, -1, -1)
        Bu = updateU(Bu, tmpI, n, d, ru, tu, winu, z, X, v1, sigsq)
        Iu = np.argmin(Bu) + 1
        temp = np.sort(np.append(np.abs(np.multiply(z, winu)), 0))
        lu = temp[(n - Iu)]
        paralambda = lu / winu[(winu != 0)]
        tmp = np.multiply(np.sign(z[(winu != 0)]), gt(np.abs(z[(winu != 0)]), paralambda))
        u1 = np.multiply(tmp, np.abs(z[(winu != 0)]) - paralambda)
        u1 = u1 / np.sqrt(np.sum(u1 ** 2))
        ud = np.sqrt(np.sum((u0 - u1) ** 2))
        vd = np.sqrt(np.sum((v0 - v1) ** 2))
        if iters > niter:
            print('Fail to converge! Increase the niter!')
            break
        u0 = u1
        v0 = v1

    u = u1
    v = v1
    return (u, v, iters)