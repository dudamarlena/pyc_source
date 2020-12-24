# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/MorphoTester/implicitfair.py
# Compiled at: 2015-10-02 14:09:25
"""
Created on Oct 10, 2012

Contains functions for executing an implicit fairing smooth on a 3D mesh.

@author: Julia M. Winchester
"""
import DNE
from math import acos, tan
from numpy import sqrt, spacing, diag, mat
from numpy.linalg import cholesky, solve, LinAlgError
from scipy.sparse import identity, lil_matrix

def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)


def My_Angle(u, v):
    du = sqrt(sum(u ** 2))
    dv = sqrt(sum(v ** 2))
    du = max(du, spacing(1))
    dv = max(dv, spacing(1))
    x = sum(u * v) / (du * dv)
    x = clamp(x, -1.0, 1.0)
    angle = acos(x)
    return angle


def laplaciantension(vertex, faceindex):
    n = len(vertex)
    L = lil_matrix((n, n))
    ring = DNE.vertexfacedict(faceindex, len(vertex))
    for i in range(0, n):
        for b in ring[i]:
            bf = faceindex[b]
            if bf[0] == i:
                v = (
                 bf[1], bf[2])
            elif bf[1] == i:
                v = (
                 bf[0], bf[2])
            elif bf[2] == i:
                v = (
                 bf[0], bf[1])
            else:
                print 'Problem in face ring.'
            j = v[0]
            k = v[1]
            vi = vertex[i]
            vj = vertex[j]
            vk = vertex[k]
            alpha = My_Angle(vk - vi, vk - vj)
            beta = My_Angle(vj - vi, vj - vk)
            if alpha == 0:
                cot_alpha = 0
            else:
                cot_alpha = 1 / tan(alpha)
            if beta == 0:
                cot_beta = 0
            else:
                cot_beta = 1 / tan(beta)
            L[(i, j)] = L[(i, j)] + cot_alpha
            L[(i, k)] = L[(i, k)] + cot_beta

    a = L.sum(axis=1)
    b = [ float(i) for i in a ]
    L = L - diag(b)
    return L


def smooth(vertex, faceindex, iternum, stepsize):
    L = laplaciantension(vertex, faceindex)
    sparseidentity = identity(len(vertex))
    tochol = sparseidentity - stepsize * L
    tochol = mat(tochol)
    try:
        R = cholesky(tochol).T
    except LinAlgError:
        print 'Cholesky decomposition cannot be computed, mesh matrix is not positive definite.'
        return '!'

    for k in range(0, iternum):
        Q = solve(R.H, vertex)
        vertex = solve(R, Q)

    return vertex