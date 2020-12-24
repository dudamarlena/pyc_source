# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\drgpom\methods\current_models.py
# Compiled at: 2020-03-31 10:24:15
# Size of source mod 2**32: 12959 bytes
"""
current_models - library of ionic current models implemented in Python

Created on Mon Apr 10 16:30:04 2017

@author: Oliver Britton
"""
import os, sys, pandas as pd, numpy as np
from matplotlib import pyplot as plt
import seaborn as sns

def nav17vw(Y, t, voltage_clamp_func, voltage_clamp_params):
    """ Human Nav 1.7 from Vasylyev Waxman """
    v = voltage_clamp_func(t, voltage_clamp_params)
    m = Y[0]
    h = Y[1]
    alpha_m = 10.22 - 10.22 / (1 + np.exp((v + 7.19) / 15.43))
    beta_m = 23.76 / (1 + np.exp((v + 70.37) / 14.53))
    minf = alpha_m / (alpha_m + beta_m)
    mtau = 1 / (alpha_m + beta_m)
    alpha_h = 0.0744 / (1 + np.exp((v + 99.76) / 11.07))
    beta_h = 2.54 - 2.54 / (1 + np.exp((v + 7.8) / 10.68))
    hinf = alpha_h / (alpha_h + beta_h)
    htau = 1 / (alpha_h + beta_h)
    dm = (minf - m) / mtau
    dh = (hinf - h) / htau
    return [dm, dh]


def nav17cw(Y, t, voltage_clamp_func, voltage_clamp_params):
    """ Rat? Nav 1.7 from Choi Waxman 2011 """
    v = voltage_clamp_func(t, voltage_clamp_params)
    m = Y[0]
    h = Y[1]
    s = Y[2]
    alpha_m = 15.5 / (1 + np.exp(-(v - 5) / 12.08))
    beta_m = 35.2 / (1 + np.exp((v + 72.7) / 16.7))
    minf = alpha_m / (alpha_m + beta_m)
    mtau = 1 / (alpha_m + beta_m)
    alpha_h = 0.38685 / (1 + np.exp((v + 122.35) / 15.29))
    beta_h = -0.00283 + 2.00283 / (1 + np.exp(-(v + 5.5266) / 12.70195))
    hinf = alpha_h / (alpha_h + beta_h)
    htau = 1 / (alpha_h + beta_h)
    alpha_s = 3e-05 + 0.00092 / (1 + np.exp((v + 93.9) / 16.6))
    beta_s = 132.05 - 132.05 / (1 + np.exp((v - 384.9) / 28.5))
    sinf = alpha_s / (alpha_s + beta_s)
    stau = 1 / (alpha_s + beta_s)
    dm = (minf - m) / mtau
    dh = (hinf - h) / htau
    ds = (sinf - s) / stau
    return [
     dm, dh, ds]


def nav18hw(Y, t, voltage_clamp_func, voltage_clamp_params):
    """ Human Nav 1.8 from Huang Waxman 20(14?) """
    v = voltage_clamp_func(t, voltage_clamp_params)
    m = Y[0]
    h = Y[1]
    alpha_m = 7.35 - 7.35 / (1 + np.exp((v + 1.38) / 10.9))
    beta_m = 5.97 / (1 + np.exp((v + 56.43) / 18.26))
    minf = alpha_m / (alpha_m + beta_m)
    mtau = 1 / (alpha_m + beta_m)
    alpha_h = 0.011 + 1.39 / (1 + np.exp((v + 78.04) / 11.32))
    beta_h = 0.56 - 0.56 / (1 + np.exp((v - 21.82) / 20.03))
    hinf = alpha_h / (alpha_h + beta_h)
    htau = 1 / (alpha_h + beta_h)
    dm = (minf - m) / mtau
    dh = (hinf - h) / htau
    return [
     dm, dh]


def nav18tf(Y, t, voltage_clamp_func, voltage_clamp_params):
    """ Rat? Nav 1.8 used in Tigerholm model """
    v = voltage_clamp_func(t, voltage_clamp_params)
    m = Y[0]
    h = Y[1]
    s = Y[2]
    u = Y[3]
    alpha_m = 2.85 - 2.839 / (1 + np.exp((v - 1.159) / 13.95))
    beta_m = 7.6205 / (1 + np.exp((v + 46.463) / 8.8289))
    minf = alpha_m / (alpha_m + beta_m)
    mtau = 1 / (alpha_m + beta_m)
    hinf = 1 / (1 + np.exp((v + 32.2) / 4))
    htau = 1.218 + 42.043 * np.exp(-(v + 38.1) ** 2 / 461.4722)
    alpha_s = 0.0054203 / (1 + np.exp((v + 79.816) / 16.269))
    beta_s = 0.005075700000000001 / (1 + np.exp(-(v + 15.968) / 11.542))
    sinf = 1 / (1 + np.exp((v + 45.0) / 8))
    stau = 1 / (alpha_s + beta_s)
    alpha_u = 0.004086800000000001 / (1 + np.exp((v + 67.499) / 19.51))
    beta_u = 0.0039904 / (1 + np.exp(-(v + 30.963) / 14.792))
    uinf = 1 / (1 + np.exp((v + 51.0) / 8))
    utau = 1.0 / (alpha_u + beta_u)
    dm = (minf - m) / mtau
    dh = (hinf - h) / htau
    ds = (sinf - s) / stau
    du = (uinf - u) / utau
    return [
     dm, dh, ds, du]


def nav18cw(Y, t, voltage_clamp_func, voltage_clamp_params):
    """ Nav 1.8 model used in Choi Waxman 2011 """
    v = voltage_clamp_func(t, voltage_clamp_params)
    m = Y[0]
    h = Y[1]
    alpha_m = 2.85 - 2.839 / (1 + np.exp((v - 1.159) / 13.95))
    beta_m = 7.6205 / (1 + np.exp((v + 46.463) / 8.8289))
    minf = alpha_m / (alpha_m + beta_m)
    mtau = 1 / (alpha_m + beta_m)
    hinf = 1 / (1 + np.exp((v + 32.2) / 4))
    htau = 1.218 + 42.043 * np.exp(-(v + 38.1) ** 2 / 461.4722)
    dm = (minf - m) / mtau
    dh = (hinf - h) / htau
    return [
     dm, dh]


def nav19hw(Y, t, voltage_clamp_func, voltage_clamp_params):
    """ Nav 1.9 model from Huang Waxman 2014"""
    m = Y[0]
    h = Y[1]
    s = Y[2]
    v = voltage_clamp_func(t, voltage_clamp_params)
    alpha_m = 0.751 / (1 + np.exp(-(v + 32.26) / 13.71))
    beta_m = 5.68 / (1 + np.exp((v + 123.71) / 13.94))
    minf = alpha_m / (alpha_m + beta_m)
    mtau = 1 / (alpha_m + beta_m)
    alpha_h = 0.082 / (1 + np.exp((v + 113.69) / 17.4))
    beta_h = 0.24 / (1 + np.exp(-(v - 10.1) / 17.2))
    hinf = alpha_h / (alpha_h + beta_h)
    htau = 1 / (alpha_h + beta_h)
    alpha_s = 0.019 / (1 + np.exp((v + 154.51) / 11.46))
    beta_s = 0.000376 / (1 + np.exp(-(v + 60.92) / 15.79))
    sinf = alpha_s / (alpha_s + beta_s)
    stau = 1 / (alpha_s + beta_s)
    dm = (minf - m) / mtau
    dh = (hinf - h) / htau
    ds = (sinf - s) / stau
    return [
     dm, dh, ds]


def nav19md(Y, t, voltage_clamp_func, voltage_clamp_params):
    """ Nav 1.9 model from Maingret 2008"""
    m = Y[0]
    h = Y[1]
    s = Y[2]
    v = voltage_clamp_func(t, voltage_clamp_params)
    return [
     dm, dh, ds]


def nav16zm(Y, t, voltage_clamp_func, voltage_clamp_params):
    """ Nav 1.6 model from Zach Mainen 1994 """
    m = Y[0]
    h = Y[1]
    v = voltage_clamp_func(t, voltage_clamp_params)
    vhalf = -43.0
    a_m = 0.182 * (v - vhalf) / (1 - np.exp((vhalf - v) / 6.0))
    b_m = 0.124 * (-v + vhalf) / (1 - np.exp((-vhalf + v) / 6.0))
    m_inf = a_m / (a_m + b_m)
    m_tau = 1.0 / (a_m + b_m)
    vhalf_ha = -50.0
    vhalf_hb = -75.0
    q_h = 5.0
    vhalf_inf = -72.0
    qinf = 6.2
    rate_ha = 0.0091
    rate_hb = 0.024
    a_h = rate_ha * (v - vhalf_ha) / (1 - np.exp((vhalf_ha - v) / q_h))
    b_h = rate_hb * (-v + vhalf_hb) / (1 - np.exp((-vhalf_hb + v) / q_h))
    h_inf = 1.0 / (1.0 + np.exp((v - vhalf_inf) / qinf))
    h_tau = 1.0 / (a_h + b_h)
    dm = (m_inf - m) / m_tau
    dh = (h_inf - h) / h_tau
    return [
     dm, dh]


def kdr_tf(Y, t, voltage_clamp_func, voltage_clamp_params):
    """ Tigerholm version of the Sheets et al. IKdr model """
    v = voltage_clamp_func(t, voltage_clamp_params)
    n = Y[0]
    q10 = 1.0
    if v > -31.0:
        tau = 0.16 + 0.8 * np.exp(-0.0267 * (v + 11))
    else:
        tau = 1000 * (0.000688 + 1 / (np.exp((v + 75.2) / 6.5) + np.exp(-(v - 131.5) / 34.8)))
    ninf = 1 / (1 + np.exp(-(v + 45) / 15.4))
    ntau = tau / q10
    dn = (ninf - n) / ntau
    return [dn]


def km_tf(Y, t, voltage_clamp_func, voltage_clamp_params):
    """ Tigerholm version of the IM current. Current is from multiple sources:
    The voltage dependence of steady-state activation forthe KM current is from
    Maingret et al. (2008), which was derived from Passmore 2003. The KM channel activation has a fast and a slow 
    time constant as described by Passmore et al. (2003). To account for the 
    two time constants, weimplemented one fast (nf) and one slow (ns) gate, 
    combined as follows.
    """
    v = voltage_clamp_func(t, voltage_clamp_params)
    ns = Y[0]
    nf = Y[1]
    q10 = 1.0
    if v < -60.0:
        nstau = 219.0 * q10
    else:
        nstau = 13.0 * v + 1000.0 * q10
    nftau_alpha = 0.00395 * np.exp((v + 30.0) / 40.0)
    nftau_beta = 0.00395 * np.exp(-(v + 30.0) / 20.0) * q10
    nftau = 1.0 / (nftau_alpha + nftau_beta)
    ninf = 1.0 / (1.0 + np.exp(-(v + 30.0) / 6.0))
    dns = (ninf - ns) / nstau
    dnf = (ninf - nf) / nftau
    return [
     dns, dnf]


def ka_tf(Y, t, voltage_clamp_func, voltage_clamp_params):
    """ Tigerholm version of IA.
    """
    v = voltage_clamp_func(t, voltage_clamp_params)
    n = Y[0]
    h = Y[1]
    q10 = 1.0
    ninf = (1.0 / (1.0 + np.exp(-(v + 5.4 + 15) / 16.4))) ** 4
    ntau = 0.25 + 10.04 * np.exp(-(v + 24.67) ** 2 / 2422.0799999999995) * q10
    hinf = 1.0 / (1.0 + np.exp((v + 49.9 + 15.0) / 4.6))
    htau = 20.0 + 50.0 * np.exp(-(v + 40.0) ** 2 / 3200.0) * q10
    if htau < 5.0:
        htau = 5.0
    dn = (ninf - n) / ntau
    dh = (hinf - h) / htau
    return [
     dn, dh]


def cal_ja(Y, t, voltage_clamp_func, voltage_clamp_params):
    """
    Jaffe et al. 1994 ICaL model. 
    """
    v = voltage_clamp_func(t, voltage_clamp_params)
    m = Y[0]
    tfa = 1.0
    ki = 0.001
    cao = 2.5
    cai = 0.0001
    celsius = 37.0

    def alpha(v):
        return 15.69 * (81.5 - v) / (np.exp((-1.0 * v + 81.5) / 10.0) - 1.0)

    def beta(v):
        return 0.29 * np.exp(-v / 10.86)

    def KTF(celsius):
        return 0.08528057308545114 * (celsius + 273.15)

    def efun(z):
        return np.array([1 - i / 2 if i < 0.0001 else i / (np.exp(i) - 1) for i in z])

    def calc_ghk(v, cai, cao):
        f = KTF(celsius) / 2
        nu = v / f
        return -f * (1.0 - cai / cao * np.exp(nu)) * efun(nu)

    a = alpha(v)
    b = beta(v)
    tau = 1.0 / (tfa * (a + b))
    minf = a / (a + b)
    dm = (minf - m) / tau
    return [
     dm]


def can_mi():
    """
    Model of N-type Ca current from Migliore 95
    """
    pass


def hcn_kn(Y, t, voltage_clamp_func, voltage_clamp_params):
    """ 
    Kouranova Ih model with non-specific current (reversal potential should be set at -30 mV 
    """
    v = voltage_clamp_func(t, voltage_clamp_params)
    n_s = Y[0]
    n_f = Y[1]
    ninf_s = 1 / (1 + np.exp((v + 87.2) / 9.7))
    ninf_f = ninf_s
    if v > -70.0:
        tau_ns = 300.0 + 542.0 * np.exp((v + 25.0) / 20.0)
        tau_nf = 140.0 + 50.0 * np.exp(-(v + 25.0) / 20.0)
    else:
        tau_ns = 2500.0 + 100.0 * np.exp((v + 240.0) / 50.0)
        tau_nf = 250.0 + 12.0 * np.exp((v + 240.0) / 50.0)
    dns = (ninf_s - n_s) / tau_ns
    dnf = (ninf_f - n_f) / tau_nf
    return [
     dns, dnf]


def hcn_tf(Y, t, voltage_clamp_func, voltage_clamp_params):
    """
    Tigerholm version of the Kouranova Ih model which is identical except
    that when you calculate the current you don't use a nonspecific reversal potential and instead split the current between Na+ and K+, 50/50.    
    """
    v = voltage_clamp_func(t, voltage_clamp_params)
    n_s = Y[0]
    n_f = Y[1]
    ninf_s = 1 / (1 + np.exp((v + 87.2) / 9.7))
    ninf_f = ninf_s
    if v > -70.0:
        tau_ns = 300.0 + 542.0 * np.exp((v + 25.0) / 20.0)
        tau_nf = 140.0 + 50.0 * np.exp(-(v + 25.0) / 20.0)
    else:
        tau_ns = 2500.0 + 100.0 * np.exp((v + 240.0) / 50.0)
        tau_nf = 250.0 + 12.0 * np.exp((v + 240.0) / 50.0)
    dns = (ninf_s - n_s) / tau_ns
    dnf = (ninf_f - n_f) / tau_nf
    return [
     dns, dnf]


def nav17test(Y, t, voltage_clamp_func, voltage_clamp_params):
    """ Human Nav 1.7 from Vasylyev Waxman """
    v = voltage_clamp_func(t, voltage_clamp_params)
    m = Y[0]
    h = Y[1]
    alpha_m = 10.22 - 10.22 / (1 + np.exp((v + 7.19) / 15.43))
    beta_m = 23.76 / (1 + np.exp((v + 70.37) / 14.53))
    minf = alpha_m / (alpha_m + beta_m)
    mtau = 1 / (alpha_m + beta_m)
    alpha_h = 0.0744 / (1 + np.exp((v + 99.76) / 11.07))
    beta_h = 2.54 - 2.54 / (1 + np.exp((v + 7.8) / 10.68))
    hinf = alpha_h / (alpha_h + beta_h)
    htau = 1 / (alpha_h + beta_h)
    dm = (minf - m) / mtau
    dh = (hinf - h) / htau
    return [dm, dh]