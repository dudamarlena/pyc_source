# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/MEEGbuddy/pci.py
# Compiled at: 2019-02-12 17:24:47
# Size of source mod 2**32: 3499 bytes
import numpy as np
from bitarray import bitarray

def calculate_pci_lower(D):
    """
        Computes a lower bound of the PCI for the binary matrix D.

        The PCI is computed on the ordered matrix D (i.e. the channels are ranked based on the evoked activity).
        A speed up in the calculation is achieved removing the zero-rows (see Casali's MATLAB code).
    """
    Irank = np.sum(D, axis=1).argsort()
    S = D[Irank, :].sum(axis=1)
    Izero = np.where(S == 0)[0]
    number0removed = D.shape[1] * len(Izero)
    Dnew = D[Irank, :][Izero[(-1)] + 1:, :]
    a = lz_complexity_2D(Dnew)
    nValues = float(D.shape[0] * D.shape[1])
    p1 = np.sum(D) / nValues
    p0 = 1 - p1
    N = np.log2(nValues) / nValues
    H = -p1 * np.log2(p1) - p0 * np.log2(p0)
    PCI = N * np.array(ct) / H
    return PCI


def calculate(D):
    return lz_complexity_2D(D) / pci_norm_factor(D)


def pci_norm_factor(D):
    L = D.shape[0] * D.shape[1]
    p1 = sum(1.0 * (D.flatten() == 1)) / L
    p0 = 1 - p1
    H = -p1 * np.log2(p1) - p0 * np.log2(p0)
    S = L * H / np.log2(L)
    return S


def lz_complexity_2D(D):
    if len(D.shape) != 2:
        raise Exception('data has to be 2D!')
    L1, L2 = D.shape
    c = 1
    r = 1
    q = 1
    k = 1
    i = 1
    stop = False
    bits = [
     None] * L2
    for y in range(0, L2):
        bits[y] = bitarray(D[:, y].tolist())

    def end_of_column(r, c, i, q, k, stop):
        r += 1
        if r > L2:
            c += 1
            stop = True
        else:
            i = 0
            q = r - 1
            k = 1
        return (
         r, c, i, q, k, stop)

    ct = []
    while not stop:
        if q == r:
            a = i + k - 1
        else:
            a = L1
        found = not not bits[(q - 1)][0:a].search(bits[(r - 1)][i:i + k], 1)
        if found:
            k += 1
            if i + k > L1:
                r, c, i, q, k, stop = end_of_column(r, c, i, q, k, stop)
                ct.append(c)
        else:
            q -= 1
            if q < 1:
                c += 1
                i = i + k
                if i + 1 > L1:
                    r, c, i, q, k, stop = end_of_column(r, c, i, q, k, stop)
                    ct.append(c)
                else:
                    q = r
                    k = 1

    return np.array(ct)