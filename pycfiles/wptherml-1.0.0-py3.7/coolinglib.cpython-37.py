# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/wptherml/coolinglib.py
# Compiled at: 2019-08-20 10:23:08
# Size of source mod 2**32: 3495 bytes
"""
Created on Thu Oct 11 13:14:46 2018

@author: varnerj
"""
from wptherml import tmm
import wptherml.datalib as datalib
from wptherml import stpvlib
import numpy as np
import matplotlib.pyplot as plt
import wptherml.numlib as numlib

def E_atm(theta, lam):
    T = datalib.ATData(lam)
    b = 1.0 / np.cos(theta)
    Eatm = (1 - T) ** b
    return Eatm


def Prad(TEP, TES, lam, theta, w):
    dlam = np.abs(lam[0] - lam[1])
    x = 0
    for i in range(0, len(w)):
        prad_som = 0
        for j in range(0, len(lam)):
            prad_som = prad_som + (0.5 * TEP[i][j] + 0.5 * TES[i][j]) * dlam

        x = x + prad_som * (np.sin(theta[i]) * w[i])

    return 2 * np.pi * x


def Patm(EPS_P, EPS_S, T_amb, lam, theta, w):
    dlam = np.abs(lam[0] - lam[1])
    atm_T = datalib.ATData(lam)
    BBs = datalib.BB(lam, T_amb)
    x = 0
    for i in range(0, len(w)):
        patm_som = 0
        angular_mod = 1.0 / np.cos(theta[i])
        for j in range(0, len(lam)):
            patm_som = patm_som + (0.5 * EPS_P[i][j] + 0.5 * EPS_S[i][j]) * BBs[j] * np.cos(theta[i]) * (1 - atm_T[j] ** angular_mod) * dlam

        x = x + patm_som * np.sin(theta[i]) * w[i]

    return 2 * np.pi * x


def Psun(theta_sun, lam, n, d):
    n_lam = len(lam)
    n_layer = len(d)
    AM = datalib.AM(lam)
    emissivity_s = 0.0
    emissivity_p = 0.0
    nc = np.zeros(n_layer, dtype=complex)
    P_sun_sum = 0.0
    dl = np.abs(lam[1] - lam[0])
    for i in range(0, n_lam):
        for j in range(0, n_layer):
            nc[j] = n[j][i]

        k0 = np.pi * 2 / lam[i]
        Mp = tmm.tmm(k0, theta_sun, 'p', nc, d)
        Ms = tmm.tmm(k0, theta_sun, 's', nc, d)
        tp = 1.0 / Mp['M11']
        ts = 1.0 / Ms['M11']
        tpi = Mp['theta_i']
        tpL = Mp['theta_L']
        tsi = Ms['theta_i']
        tsL = Ms['theta_L']
        facp = nc[(n_layer - 1)] * np.cos(tpL) / (nc[0] * np.cos(tpi))
        facs = nc[(n_layer - 1)] * np.cos(tsL) / (nc[0] * np.cos(tsi))
        rp = Mp['M21'] / Mp['M11']
        rs = Ms['M21'] / Ms['M11']
        Rp = np.real(rp * np.conj(rp))
        Rs = np.real(rs * np.conj(rs))
        Tp = np.real(tp * np.conj(tp) * facp)
        Ts = np.real(ts * np.conj(ts) * facs)
        emissivity_p = 1 - Rp - Tp
        emissivity_s = 1 - Rs - Ts
        P_sun_sum = P_sun_sum + 0.5 * (emissivity_p + emissivity_s) * AM[i] * dl

    return P_sun_sum


def Pwr_cool(lam):
    Pcool = Prad() - Patm(lam, theta, T) - Psun(lam)
    return Pcool