# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/fdasrsf/geometry.py
# Compiled at: 2019-04-10 18:31:59
# Size of source mod 2**32: 873 bytes
"""
geometry functions for SRSF Manipulations

moduleauthor:: Derek Tucker <jdtuck@sandia.gov>

"""
from numpy import arccos, sin, cos, linspace, zeros, sqrt
from scipy.integrate import trapz

def inv_exp_map(Psi, psi):
    tmp = inner_product(Psi, psi)
    if tmp > 1:
        tmp = 1
    else:
        if tmp < -1:
            tmp = -1
        theta = arccos(tmp)
        if theta < 1e-10:
            exp_inv = zeros(psi.shape[0])
        else:
            exp_inv = theta / sin(theta) * (psi - cos(theta) * Psi)
    return (
     exp_inv, theta)


def exp_map(psi, v):
    v_norm = L2norm(v)
    expgam = cos(v_norm) * psi + sin(v_norm) * v / v_norm
    return expgam


def inner_product(psi1, psi2):
    M = psi1.shape[0]
    t = linspace(0, 1, M)
    ip = trapz(psi1 * psi2, t)
    return ip


def L2norm(psi):
    M = psi.shape[0]
    t = linspace(0, 1, M)
    l2norm = sqrt(trapz(psi * psi, t))
    return l2norm