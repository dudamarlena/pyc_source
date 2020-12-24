# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\pyweights\entropy.py
# Compiled at: 2020-05-11 03:44:34
# Size of source mod 2**32: 1147 bytes
import numpy as np, numpy
__author__ = 'Xia Tian (xsumner@hotmail.com)'

def matrix_standardization(M):
    M = M.copy()
    M = (M - M.min()) / (M.max() - M.min())
    return M


def get_entropy(M):
    m, n = M.shape
    k = 1 / np.log(m)
    yij = M.sum(axis=0)
    pij = M / yij
    test = pij * np.log(pij)
    test = np.nan_to_num(test)
    ej = -k * test.sum(axis=0)
    wi = (1 - ej) / (n - np.sum(ej))
    return (
     ej, wi)


def get_score(M, W):
    W = W.copy()
    M = M.copy()
    S = W * M
    return S.sum(axis=0)