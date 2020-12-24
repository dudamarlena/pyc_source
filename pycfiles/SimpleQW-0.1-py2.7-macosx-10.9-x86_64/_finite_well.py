# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/simpleqw/_finite_well.py
# Compiled at: 2014-12-26 00:18:10
import numpy
from numpy import sqrt, tan, cos, pi, arcsin

def infinite_well_ground_state_energy(thickness, meff):
    """
    thickness : float
        thickness of the well in units of meters
    meff : float
        effective mass in the well as a fraction of the electron mass

    Returns the ground state energy in units of eV.
    """
    return 3.7603e-19 / (thickness ** 2 * meff)


def _finite_well_states(P):
    """
    Returns the number of bound states in a finite-potential quantum well
    with the given well-strength parameter, `P`.
    """
    return int(P / (pi / 2.0)) + 1


def _finite_well_energy(P, n=1, atol=1e-06):
    """
    Returns the nth bound-state energy for a finite-potential quantum well
    with the given well-strength parameter, `P`.
    """
    assert n > 0 and n <= _finite_well_states(P)
    pi_2 = pi / 2.0
    r = 1 / (P + pi_2) * (n * pi_2)
    eta = n * pi_2 - arcsin(r) - r * P
    w = 1
    while True:
        assert r <= 1
        if abs(eta) < atol:
            break
        r2 = r ** 2.0
        sqrt_1mr2 = sqrt(1.0 - r2)
        denom = 1.0 + P * sqrt_1mr2
        t1 = P * sqrt_1mr2 / denom * eta
        while True:
            next_r = (1 - w) * r + w * (r + t1)
            next_eta = n * pi_2 - arcsin(next_r) - next_r * P
            if abs(next_eta / eta) < 1:
                r = next_r
                eta = next_eta
                break
            else:
                w *= 0.5

    alpha = P * r
    E = 2 * alpha ** 2
    return E


prefactor = 2561584000.0

def finite_well_energy(a, m, U, n=1):
    """
    a : float
        thickness of the well in units of meters
    m : float
        effective mass in the well as a fraction of the electron mass
    U : float
        the potential in eV
    n : int
        the quantum number of the desired state

    If U <= 0, returns 0. Otherwise, returns the confinement energy in
    units of eV.

    Reference:
    D.L. Aronstein and C.R. Stroud, Jr., Am. J. Phys. 68, 943 (2000).
    """
    if U <= 0.0:
        return 0
    P = prefactor * a * sqrt(m * U)
    print P, _finite_well_energy(P, n)
    return _finite_well_energy(P, n) * 7.61996e-20 / m / a ** 2.0


def plot_time():
    import time, matplotlib.pyplot as plt
    repeats = 20
    Pi = numpy.linspace(0.01, 6, 100)
    ti = numpy.empty_like(Pi)
    Eij = numpy.empty((100, repeats), dtype=float)
    for i in xrange(Pi.size):
        t0 = time.time()
        for j in xrange(repeats):
            Eij[i][j] = _finite_well_energy(Pi[i], n=1)

        t1 = time.time()
        ti[i] = float(t1 - t0) / repeats

    plt.semilogy(Pi, ti)
    plt.ylim(1e-05, 0.1)
    plt.show()


def plot_E1():
    import matplotlib.pyplot as plt
    Pi = numpy.linspace(0, 6, 100)
    Ni = numpy.empty_like(Pi, dtype=int)
    for i, P in enumerate(Pi):
        Ni[i] = _finite_well_states(P)

    plt.plot(Pi, Ni)
    plt.show()
    plt.cla()
    Eij = numpy.empty((Pi.size, 10), dtype=float)
    for i, P in enumerate(Pi):
        for j in xrange(10):
            if j + 1 <= _finite_well_states(P):
                Eij[(i, j)] = _finite_well_energy(P, n=j + 1)
            else:
                Eij[(i, j)] = numpy.nan

    for j in xrange(10):
        plt.plot(Pi, Eij[:, j])

    plt.show()


if __name__ == '__main__':
    print finite_well_energy(1.0000000000000002e-12, 1, 1, n=1)