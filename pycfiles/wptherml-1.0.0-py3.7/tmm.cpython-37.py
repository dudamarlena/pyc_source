# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/wptherml/tmm.py
# Compiled at: 2019-08-20 10:27:39
# Size of source mod 2**32: 13437 bytes
"""
Created on Fri Sep 14 14:05:59 2018
@author: varnerj
"""
import numpy as np
from matplotlib import pyplot as plt
from numpy.linalg import inv

def BuildP(phil):
    P = np.zeros((2, 2), dtype=complex)
    ci = complex(0.0, 1.0)
    a = -1 * ci * phil
    b = ci * phil
    P[0][1] = complex(0.0, 0.0)
    P[1][0] = complex(0.0, 0.0)
    P[0][0] = np.exp(a)
    P[1][1] = np.exp(b)
    return P


def BuildD(nl, ctheta, pol):
    D = np.zeros((2, 2), dtype=complex)
    if pol == 's' or pol == 'S':
        D[0][0] = complex(1.0, 0.0)
        D[0][1] = complex(1.0, 0.0)
        D[1][0] = nl * ctheta
        D[1][1] = -1 * nl * ctheta
    else:
        if pol == 'p' or pol == 'P':
            D[0][0] = ctheta + complex(0.0, 0.0)
            D[0][1] = ctheta + complex(0.0, 0.0)
            D[1][0] = nl
            D[1][1] = -1 * nl
        else:
            print('Polarization not chosen... defaulting to p-polarization')
            D[0][0] = ctheta + complex(0.0, 0.0)
            D[0][1] = ctheta + complex(0.0, 0.0)
            D[1][0] = nl
            D[1][1] = -1 * nl
    return D


def tmm(k0, theta0, pol, nA, tA):
    t1 = np.zeros((2, 2), dtype=complex)
    t2 = np.zeros((2, 2), dtype=complex)
    Dl = np.zeros((2, 2), dtype=complex)
    Dli = np.zeros((2, 2), dtype=complex)
    Pl = np.zeros((2, 2), dtype=complex)
    M = np.zeros((2, 2), dtype=complex)
    D1 = BuildD(nA[0], np.cos(theta0), pol)
    tmp = D1[(0, 0)] * D1[(1, 1)] - D1[(0, 1)] * D1[(1, 0)]
    det = 1 / tmp
    M[(0, 0)] = det * D1[(1, 1)]
    M[(0, 1)] = -det * D1[(0, 1)]
    M[(1, 0)] = -det * D1[(1, 0)]
    M[(1, 1)] = det * D1[(0, 0)]
    L = len(nA)
    kz = np.zeros(L, dtype=complex)
    phil = np.zeros(L, dtype=complex)
    ctheta = np.zeros(L, dtype=complex)
    theta = np.zeros(L, dtype=complex)
    kx = nA[0] * k0 * np.sin(theta0)
    kz[0] = np.sqrt((nA[0] * k0) ** 2 - kx ** 2)
    kz[L - 1] = np.sqrt((nA[(L - 1)] * k0) ** 2 - kx ** 2)
    if np.real(kz[0]) < 0:
        kz[0] = -1 * kz[0]
    if np.imag(kz[(L - 1)]) < 0:
        kz[L - 1] = -1 * kz[(L - 1)]
    for i in range(1, L - 1):
        kz[i] = np.sqrt((nA[i] * k0) ** 2 - kx ** 2)
        if np.imag(kz[i]) < 0:
            kz[i] = -1 * kz[i]
        ctheta[i] = kz[i] / (nA[i] * k0)
        theta[i] = np.arccos(ctheta[i])
        phil[i] = kz[i] * tA[i]
        Dl = BuildD(nA[i], ctheta[i], pol)
        tmp = Dl[(0, 0)] * Dl[(1, 1)] - Dl[(0, 1)] * Dl[(1, 0)]
        det = 1 / tmp
        Dli[(0, 0)] = det * Dl[(1, 1)]
        Dli[(0, 1)] = -det * Dl[(0, 1)]
        Dli[(1, 0)] = -det * Dl[(1, 0)]
        Dli[(1, 1)] = det * Dl[(0, 0)]
        Pl = BuildP(phil[i])
        t1 = np.matmul(M, Dl)
        t2 = np.matmul(t1, Pl)
        M = np.matmul(t2, Dli)

    kz[L - 1] = np.sqrt((nA[(L - 1)] * k0) ** 2 - kx ** 2)
    ctheta[L - 1] = kz[(L - 1)] / (nA[(L - 1)] * k0)
    DL = BuildD(nA[(L - 1)], ctheta[(L - 1)], pol)
    t1 = np.matmul(M, DL)
    theta[0] = theta0
    theta[L - 1] = np.arccos(ctheta[(L - 1)])
    ctheta[0] = np.cos(theta0)
    M = {'M11':t1[(0, 0)],  'M12':t1[(0, 1)], 
     'M21':t1[(1, 0)], 
     'M22':t1[(1, 1)], 
     'theta_i':theta0, 
     'theta_L':np.real(np.arccos(ctheta[(L - 1)])), 
     'kz':kz, 
     'phil':phil, 
     'ctheta':ctheta, 
     'theta':theta}
    return M


def whichLayer(t, d):
    dc = cumulativeD(d)
    l = len(d) - 1
    for i in range(0, len(dc)):
        if dc[i] >= t:
            l = i
            break

    return l


def cumulativeD(d):
    dc = []
    som = 0
    for i in range(0, len(d)):
        som = som + d[i]
        dc.append(som)

    return dc


def Ex(z, k0, theta0, pol, n, d):
    Ex = np.zeros((len(z)), dtype=complex)
    ci = complex(0.0, 1.0)
    M = tmm(k0, theta0, 'p', n, d)
    t = 1.0 / M['M11']
    r = M['M21'] / M['M11']
    kz = M['kz']
    phil = M['phil']
    ctheta = M['ctheta']
    Ef = np.zeros(2, dtype=complex)
    Ei = np.zeros(2, dtype=complex)
    Ep = np.zeros((len(n)), dtype=complex)
    Em = np.zeros((len(n)), dtype=complex)
    T1 = np.zeros(2, dtype=complex)
    T2 = np.zeros(2, dtype=complex)
    D = np.zeros((2, 2), dtype=complex)
    Di = np.zeros((2, 2), dtype=complex)
    P = np.zeros((2, 2), dtype=complex)
    Ef[0] = t
    Ef[1] = 0
    Ei[0] = 1
    Ei[1] = r
    Ep[0] = 1
    Em[0] = r
    lm1 = len(n) - 1
    Ep[lm1] = t
    Em[lm1] = 0
    T2 = Ef
    D = BuildD(n[lm1], ctheta[lm1], 'p')
    for i in range(1, lm1):
        l = lm1 - i
        T1 = np.dot(D, T2)
        D = BuildD(n[l], ctheta[l], 'p')
        Di = inv(D)
        T2 = np.dot(Di, T1)
        P = BuildP(phil[l])
        T1 = np.dot(P, T2)
        Ep[l] = T1[0]
        Em[l] = T1[1]
        T2 = T1

    l = 0
    doff = 0
    dc = cumulativeD(d)
    for i in range(0, len(z)):
        l = whichLayer(z[i], d)
        if l == 0:
            doff = 0
        else:
            doff = dc[(l - 1)]
        Ex[i] = Ep[l] * np.exp(ci * kz[l] * (z[i] - doff)) + Em[l] * np.exp(-ci * kz[l] * (z[i] - doff))

    return {'Ex':Ex,  'v_list':Ep,  'w_list':-1 * Em}


def AbsAlongz(z, k0, theta0, pol, n, d):
    alpha = np.zeros((len(z)), dtype=complex)
    M = tmm(k0, theta0, 'p', n, d)
    Ef = Ex(z, k0, theta0, pol, n, d)
    v = Ef['v_list']
    w = Ef['w_list']
    kz = M['kz']
    print('v is ', v)
    print('w is ', w)
    ctheta = M['ctheta']
    theta = M['theta']
    ci = complex(0.0, 1.0)
    for i in range(0, len(z)):
        temp = complex(0.0, 0.0)
        l = whichLayer(z[i], d)
        if l > 0:
            Ef = v[l] * np.exp(complex(0.0, 1.0) * kz[l] * z[i])
            Eb = w[l] * np.exp(complex(-0.0, -1.0) * kz[l] * z[i])
            thc = np.conj(theta[l])
            cth = np.cos(thc)
            cth0 = ctheta[0]
            imkz = np.imag(kz[l])
            rekz = np.real(kz[l])
            ni = n[l]
            n0 = n[0]
            num = ni * np.conj(cth) * (kz[l] * abs(Ef - Eb) ** 2 - np.conj(kz[l]) * abs(Ef + Eb) ** 2)
            denom = n0 * np.conj(cth0)
            alpha[i] = np.imag(num) / np.real(denom)

    return alpha


def Trans(k0, theta0, pol, nA, tA):
    L = len(nA)
    nL = nA[(L - 1)]
    ni = nA[0]
    M = tmm(k0, theta0, pol, nA, tA)
    t = 1 / M['M11']
    ti = M['theta_i']
    tL = M['theta_L']
    fac = nL * np.cos(tL) / (ni * np.cos(ti))
    T = np.real(t * np.conj(t) * fac)
    return T


def Reflect(k0, theta0, pol, nA, tA):
    M = tmm(k0, theta0, pol, nA, tA)
    r = M['M21'] / M['M11']
    R = np.real(r * np.conj(r))
    return R


def Abs(k0, theta0, pol, nA, tA):
    L = len(nA)
    nL = nA[(L - 1)]
    ni = nA[0]
    M = tmm(k0, theta0, pol, nA, tA)
    r = M['M21'] / M['M11']
    t = 1 / M['M11']
    ti = M['theta_i']
    tL = M['theta_L']
    fac = nL * np.cos(tL) / (ni * np.cos(ti))
    R = np.real(r * np.conj(r))
    T = np.real(t * np.conj(t) * fac)
    A = 1 - R - T
    return A


def tmm_ab(k0, kx, pol, nA, tA):
    t1 = np.zeros((2, 2), dtype=complex)
    t2 = np.zeros((2, 2), dtype=complex)
    Dl = np.zeros((2, 2), dtype=complex)
    Dli = np.zeros((2, 2), dtype=complex)
    Pl = np.zeros((2, 2), dtype=complex)
    M = np.zeros((2, 2), dtype=complex)
    L = len(nA)
    kz = np.zeros(L, dtype=complex)
    phil = np.zeros(L, dtype=complex)
    ctheta = np.zeros(L, dtype=complex)
    theta = np.zeros(L, dtype=complex)
    kz[0] = np.sqrt((nA[0] * k0) ** 2 - kx ** 2)
    if np.real(kz[0]) < 0:
        kz[0] = -1 * kz[0]
    ctheta[0] = kz[0] / (nA[0] * k0)
    for i in range(1, L):
        kz[i] = np.sqrt((nA[i] * k0) ** 2 - kx ** 2)
        if np.imag(kz[i]) < 0:
            kz[i] = -1 * kz[i]
        ctheta[i] = kz[i] / (nA[i] * k0)

    D1 = BuildD(nA[0], ctheta[0], pol)
    tmp = D1[(0, 0)] * D1[(1, 1)] - D1[(0, 1)] * D1[(1, 0)]
    det = 1 / tmp
    M[(0, 0)] = det * D1[(1, 1)]
    M[(0, 1)] = -det * D1[(0, 1)]
    M[(1, 0)] = -det * D1[(1, 0)]
    M[(1, 1)] = det * D1[(0, 0)]
    for i in range(1, L - 1):
        theta[i] = np.arccos(ctheta[i])
        phil[i] = kz[i] * tA[i]
        Dl = BuildD(nA[i], ctheta[i], pol)
        tmp = Dl[(0, 0)] * Dl[(1, 1)] - Dl[(0, 1)] * Dl[(1, 0)]
        det = 1 / tmp
        Dli[(0, 0)] = det * Dl[(1, 1)]
        Dli[(0, 1)] = -det * Dl[(0, 1)]
        Dli[(1, 0)] = -det * Dl[(1, 0)]
        Dli[(1, 1)] = det * Dl[(0, 0)]
        Pl = BuildP(phil[i])
        t1 = np.matmul(M, Dl)
        t2 = np.matmul(t1, Pl)
        M = np.matmul(t2, Dli)

    DL = BuildD(nA[(L - 1)], ctheta[(L - 1)], pol)
    t1 = np.matmul(M, DL)
    r = t1[(1, 0)] / t1[(0, 0)]
    return np.real(np.conj(r) * r)