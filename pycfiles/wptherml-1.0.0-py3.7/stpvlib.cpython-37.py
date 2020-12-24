# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/wptherml/stpvlib.py
# Compiled at: 2019-08-20 10:23:08
# Size of source mod 2**32: 10318 bytes
import wptherml.numlib as numlib
import wptherml.datalib as datalib
from wptherml import tmm
import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate
q = 1.60217662e-19
c = 299792458
h = 6.626e-34
k = 1.38064852e-23

def SpectralEfficiency(TE, lam, lbg):
    ynum = TE * lam / lbg
    upper = np.amax(lam)
    num = numlib.Integrate(ynum, lam, 1e-09, lbg)
    den = numlib.Integrate(TE, lam, 1e-09, upper)
    SE = num / den
    return SE


def SpectralEfficiency_EA(TE_p, TE_s, lam, lbg, t, w):
    num = 0.0
    den = 0.0
    dl = abs(lam[1] - lam[0])
    for i in range(0, len(w)):
        num_isom = 0.0
        den_isom = 0.0
        for j in range(0, len(lam)):
            den_isom = den_isom + 0.5 * TE_p[i][j] * dl
            den_isom = den_isom + 0.5 * TE_s[i][j] * dl
            if lam[j] <= lbg:
                num_isom = num_isom + 0.5 * lam[j] / lbg * TE_p[i][j] * dl
                num_isom = num_isom + 0.5 * lam[j] / lbg * TE_s[i][j] * dl

        num = num + w[i] * num_isom * np.sin(t[i]) * 2 * np.pi
        den = den + w[i] * den_isom * np.sin(t[i]) * 2 * np.pi

    return num / den


def Pwr_den(TE, lam, lbg):
    PDA = lam / lbg * TE
    PD = numlib.Integrate(PDA, lam, 1e-09, lbg)
    return PD * np.pi


def Pwr_den_EA(TE_p, TE_s, lam, lbg, t, w):
    PD = 0.0
    dl = np.abs(lam[1] - lam[0])
    for i in range(0, len(w)):
        isom = 0.0
        for j in range(0, len(lam)):
            if lam[j] >= lbg:
                break
            isom = isom + 0.5 * lam[j] / lbg * TE_p[i][j] * dl
            isom = isom + 0.5 * lam[j] / lbg * TE_s[i][j] * dl

        PD = PD + w[i] * isom * np.sin(t[i])

    return PD * 2 * np.pi


def p_in(TE, lam):
    integrand = TE * np.pi
    upper = np.amax(lam)
    p = numlib.Integrate(integrand, lam, 1e-09, upper)
    return p


def p_in_ea(TE_p, TE_s, lam, t, w):
    pin = 0.0
    dl = np.abs(lam[1] - lam[0])
    for i in range(0, len(w)):
        isom = 0.0
        for j in range(0, len(lam)):
            isom = isom + 0.5 * TE_p[i][j] * dl
            isom = isom + 0.5 * TE_s[i][j] * dl

        pin = pin + w[i] * isom * np.sin(t[i])

    return pin * 2 * np.pi


def ambient_jsc(eps, lam, lbg):
    upper = np.amax(lam)
    AM = datalib.AM(lam)
    SR = datalib.SR_Si(lam)
    integrand = AM * SR * eps
    jsc = numlib.Integrate(integrand, lam, 1e-09, upper)
    return jsc


def JSC(TE, lam, PV):
    F = 0.84
    if PV == 'InGaAsSb':
        SR = datalib.SR_InGaAsSb(lam)
    else:
        if PV == 'GaSb':
            SR = datalib.SR_GaSb(lam)
        else:
            SR = datalib.SR_InGaAsSb(lam)
    upper = np.amax(lam)
    integrand = TE * SR * F * np.pi
    jshc = numlib.Integrate(integrand, lam, 1e-09, upper)
    return jshc


def JSC_EA(TE_p, TE_s, lam, PV, t, w):
    F = 0.84
    if PV == 'InGaAsSb':
        SP = datalib.SR_InGaAsSb(lam)
    else:
        if PV == 'GaSb':
            SP = datalib.SR_GaSb(lam)
        else:
            SP = datalib.SR_InGaAsSb(lam)
    jsch = 0.0
    dl = np.abs(lam[1] - lam[0])
    for i in range(0, len(t)):
        isom = 0.0
        for j in range(0, len(lam)):
            isom = isom + 0.5 * TE_p[i][j] * SP[j] * F * dl
            isom = isom + 0.5 * TE_s[i][j] * SP[j] * F * dl

        jsch = jsch + w[i] * isom * np.sin(t[i])

    return jsch * 2 * np.pi


def Voc(Jsc, T_cell):
    lbg = 2.254e-06
    ebg = h * c / lbg
    J0 = 150000.0 * np.exp(-ebg / (k * T_cell))
    vopc = k * T_cell * np.log(Jsc / J0) / q
    return vopc


def FF(Voc, T_cell):
    red_v = q * Voc / (k * T_cell)
    beta = 0.96
    fillf = beta * (red_v - np.log(red_v + 0.72)) / (red_v + 1)
    return fillf


def Eta_TPV(TE, lam, PV, T_cell):
    jsc = JSC(TE, lam, PV)
    voc = Voc(jsc, T_cell)
    ff = FF(voc, T_cell)
    pin = p_in(TE, lam)
    eta = jsc * voc * ff / pin
    return eta


def Eta_TPV_EA(TE_p, TE_s, lam, PV, T_cell, t, w):
    jsc = JSC_EA(TE_p, TE_s, lam, PV, t, w)
    voc = Voc(jsc, T_cell)
    ff = FF(voc, T_cell)
    pin = p_in_ea(TE_p, TE_s, lam, t, w)
    eta = jsc * voc * ff / pin
    return eta


def integrated_solar_power(lam):
    AM = datalib.AM(lam)
    upper = np.amax(lam)
    p_in = numlib.Integrate(AM, lam, 1e-09, upper)
    return p_in


def absorbed_power_ea(lam, n, d, solarconc):
    """
    Ns     Temp_in_K   (Temp_in_K)
    100    694         (219)
    200    901         (239)   
    300    1048        (252)
    400    1168        (261)
    500    1270        (268)
    600    1359        (274)
    700    1440        (280)
    800    1514        (284)
    900    1582        (288)
    1000   1646        (292)
    
    from the above, 
    """
    AM = datalib.AM(lam) * solarconc
    nc = np.zeros((len(d)), dtype=complex)
    thetaC = np.arcsin(np.sqrt(solarconc * 6.85e-05 / np.pi))
    deg = 7
    a = 0
    b = thetaC
    x, w = np.polynomial.legendre.leggauss(deg)
    t = 0.5 * (x + 1) * (b - a) + a
    w = w * 0.5 * (b - a)
    osom = 0
    dl = abs(lam[1] - lam[0])
    for th, we in zip(t, w):
        isom = 0.0
        for i in range(0, len(lam)):
            k0 = np.pi * 2 / lam[i]
            for j in range(0, len(d)):
                nc[j] = n[j][i]

            As = tmm.Abs(k0, th, 's', nc, d)
            Ap = tmm.Abs(k0, th, 'p', nc, d)
            isom = isom + 0.5 * As * AM[i] * dl + 0.5 * Ap * AM[i] * dl

        osom = osom + we * isom * np.sin(th) * np.cos(th)

    return 2 * np.pi * osom


def Abs_eff(lam, EM, solarconc, T):
    AM = datalib.AM(lam)
    upper = np.amax(lam)
    BBs = datalib.BB(lam, T)
    TE = BBs * EM
    alpha = solarconc * numlib.Integrate(AM * EM, lam, 1e-07, upper)
    beta = np.pi * numlib.Integrate(TE, lam, 1e-07, upper)
    return (alpha - beta) / alpha