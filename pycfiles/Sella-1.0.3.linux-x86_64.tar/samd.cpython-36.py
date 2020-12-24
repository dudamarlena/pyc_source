# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/sella/samd.py
# Compiled at: 2019-10-04 13:28:30
# Size of source mod 2**32: 2457 bytes
from __future__ import division
import numpy as np
from ase.units import kB

def T_linear(i, T0, Tf, n):
    return T0 + i * (Tf - T0) / (n - 1)


def T_exp(i, T0, Tf, n):
    return T0 * (Tf / T0) ** (i / n)


def bdp(func, x0, ngen, T0, Tf, dt, tau, *args, schedule=T_linear, v0=None, **kwargs):
    d = len(x0)
    x = x0.copy()
    f, g = func(x, *args, **kwargs)
    if v0 is None:
        v = np.random.normal(scale=(np.sqrt(2 * T0)), size=d)
    else:
        v = v0.copy()
    edttau = np.exp(-dt / tau)
    edttau2 = np.exp(-dt / (2 * tau))
    for i in range(ngen):
        old_f = f
        old_g = g.copy()
        x += dt * v - 0.5 * dt ** 2 * g
        f, g = func(x, *args, **kwargs)
        v -= 0.5 * dt * (g + old_g)
        T = schedule(i, T0, Tf, ngen)
        K_target = d * T / 2.0
        K = np.sum(v ** 2) / 2.0
        R = np.random.normal(size=d)
        alpha2 = edttau + K * (1 - edttau) * np.sum(R ** 2) / (d * K) + 2 * edttau2 * np.sqrt(K_target * (1 - edttau) / (d * K)) * R[0]
        v *= np.sqrt(alpha2)
        print(np.average(v ** 2) / kB, T / kB)

    return x


def velocity_rescaling(func, x0, ngen, T0, Tf, dt, *args, schedule=T_linear, v0=None, **kwargs):
    d = len(x0)
    x = x0.copy()
    f, g = func(x, *args, **kwargs)
    if v0 is None:
        v = np.random.normal(scale=(np.sqrt(2 * T0)), size=d)
    else:
        v = v0.copy()
    for i in range(ngen):
        old_f = f
        old_g = g.copy()
        x += dt * v - 0.5 * dt ** 2 * g
        f, g = func(x, *args, **kwargs)
        v -= 0.5 * dt * (g + old_g)
        T = schedule(i, T0, Tf, ngen)
        K_target = d * T / 2.0
        K = np.sum(v ** 2) / 2.0
        v *= np.sqrt(K_target / K)
        print(np.average(v ** 2) / kB, T / kB)

    return x


def csvr(func, x0, ngen, T0, Tf, dt, *args, schedule=T_linear, v0=None, **kwargs):
    d = len(x0)
    x = x0.copy()
    f, g = func(x, *args, **kwargs)
    if v0 is None:
        v = np.random.normal(scale=(np.sqrt(2 * T0)), size=d)
    else:
        v = v0.copy()
    for i in range(ngen):
        old_f = f
        old_g = g.copy()
        x += dt * v - 0.5 * dt ** 2 * g
        f, g = func(x, *args, **kwargs)
        v -= 0.5 * dt * (g + old_g)
        T = schedule(i, T0, Tf, ngen)
        K_target = np.random.gamma(d / 2, T)
        K = np.sum(v ** 2) / 2.0
        v *= np.sqrt(K_target / K)
        print(np.average(v ** 2) / kB, T / kB)

    return x