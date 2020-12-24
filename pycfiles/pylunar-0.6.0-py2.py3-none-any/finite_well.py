# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/robochat/Projects/pyLuminous/pyluminous-code/pyLuminous/transfer_matrix_examples/finite_well.py
# Compiled at: 2016-08-15 10:53:48
__doc__ = "Functions for simple modelling of a finite quantum well. It was written to model\na doped GaAs/AlGaAs quantum well in order to find the quantum well's energy levels,\nits Fermi level and its optical absorptions."
import numpy as N, matplotlib.pyplot as P
from scipy.optimize import fsolve
from scipy.integrate import simps, trapz
from scipy.misc import derivative
from itertools import combinations
from functools import partial
cos, sin, tan, sqrt, exp = (
 N.cos, N.sin, N.tan, N.sqrt, N.exp)
print 'libraries imported'
hbar = 1.054571e-34
h = 6.626068e-34
Me = 9.1093826e-31
c = 299792458
eC = 1.602176e-19
pi = N.pi
eps0 = 8.8541878176e-12
kB = 1.3806504e-23
J2meV = 1000.0 / eC
meV2J = 0.001 * eC
dp = 1000000000000000.0

def rhs(E, Mb, Mw, d, V):
    return sqrt(Mw / Mb * (V / E - 1))


def odd_lhs(E, Mb, Mw, d):
    return -1.0 / tan(sqrt(Mw * Me * E / 2.0) * d / hbar)


def odd(E, Mb, Mw, d, V):
    return odd_lhs(E, Mb, Mw, d) - rhs(E, Mb, Mw, d, V)


def even_lhs(E, Mb, Mw, d):
    return tan(sqrt(Mw * Me * E / 2.0) * d / hbar)


def even(E, Mb, Mw, d, V):
    return even_lhs(E, Mb, Mw, d) - rhs(E, Mb, Mw, d, V)


def EnergyLevels(V, Mb, Mw, d):
    """Finds finite quantum well energy levels in meV. Returns 3 arrays:
    array of energy levels, array of even energy levels, array of odd energy levels"""
    intervals = 300.0
    delta = 1e-08
    errsettings = N.seterr()
    N.seterr(invalid='ignore')
    evenlevels = [0.0]
    for E0 in N.linspace(V / intervals, V, intervals, endpoint=False):
        output = fsolve(even, E0, args=(Mb, Mw, d, V), full_output=True)
        level = output[0][0]
        if abs(level - evenlevels[(-1)]) / level > 1e-08 and output[2] == 1:
            evenlevels.append(level)

    evenlevels.pop(0)
    oddlevels = [
     0.0]
    for E0 in N.linspace(V / intervals, V, intervals, endpoint=False):
        output = fsolve(odd, E0, args=(Mb, Mw, d, V), full_output=True)
        level = output[0][0]
        if abs(level - oddlevels[(-1)]) / level > 1e-08 and output[2] == 1:
            oddlevels.append(level)

    oddlevels.pop(0)
    N.seterr(**errsettings)
    levels = N.zeros(len(evenlevels) + len(oddlevels))
    levels[0::2] = evenlevels
    levels[1::2] = oddlevels
    return [ i * 1000.0 / eC for i in [levels, N.array(evenlevels), N.array(oddlevels)] ]


def wavefunctions(level, parity, VmeV, Mb, Mw, d):
    """Returns functions that give normalised wavefunctions"""
    if parity == True:
        f, s = cos, 1
    else:
        f, s = sin, -1
    k = sqrt(2 * Mw * Me * level * 0.001 * eC) / hbar
    kappa = sqrt(2 * Mb * Me * (VmeV - level) * 0.001 * eC) / hbar
    A = 1.0 / sqrt(d / 2.0 + s * sin(k * d) / 2.0 / k + f(k * d / 2.0) ** 2 / kappa)
    B = A * f(k * d / 2.0) * exp(kappa * d / 2)
    C = s * B

    def Psi(z):
        a = d / 2.0
        return (z < -a) * C * exp(kappa * z) + (z >= -a) * (z <= a) * A * f(k * z) + (z > a) * B * exp(-kappa * z)

    return Psi


def FermiLevel_0K(Ns, levels, Mw):
    Et, Ef = (0.0, 0.0)
    Z = hbar ** 2 * pi / (Mw * Me)
    N2 = Ns * dp
    for i, En in enumerate(levels):
        Et += En
        Efnew = (Z * N2 * J2meV + Et) / (i + 1)
        if Efnew > En:
            Ef = Efnew
        else:
            break
    else:
        print "Have processed all energy levels present and so can't be sure that Ef is below next higher energy level."

    Nlevels = (Ef - N.array(levels)) / (Z * J2meV * dp)
    Nlevels *= Nlevels > 0.0
    return (
     Ef, Nlevels)


def fd2(Ei, Ef, T):
    """integral of Fermi Dirac Equation.
    Ei [meV], Ef [meV], T [K]"""
    return kB * T * N.log(N.exp((Ef - Ei) / (J2meV * kB * T)) + 1)


def FermiLevel(T, Ns, levels, Mw):
    """taking advantage of step like d.o.s. and analytic integral of FD"""
    Z = hbar ** 2 * pi / (Mw * Me)
    N2 = Ns * dp

    def func(Ef, levels, N2, T):
        return N2 - sum([ fd2(En, Ef, T) for En in levels[:-1] ]) / Z

    Ef_0K, Nlevels_0K = FermiLevel_0K(Ns, levels, Mw)
    Ef = fsolve(func, Ef_0K, args=(levels, N2, T))[0]
    Nlevels = [ fd2(En, Ef, T) / Z / dp for En in levels ]
    return (
     Ef, Nlevels)


def transition_generator(seq):
    """returns the possible pairs in the input sequence. Each pair is
    only returned once and the ordering found in the input is maintained"""
    return combinations(seq, 2)


def _wavefunctions2(level, parity, VmeV, Mb, Mw, d):
    """Returns functions that give normalised wavefunctions"""
    if parity == True:
        f, s = cos, 1
    else:
        f, s = sin, -1
    k = sqrt(2 * Mw * Me * level * 0.001 * eC) / hbar
    kappa = sqrt(2 * Mb * Me * (VmeV - level) * 0.001 * eC) / hbar
    A = 1.0 / sqrt(d / 2.0 + s * sin(k * d) / 2.0 / k + f(k * d / 2.0) ** 2 / kappa)
    return (
     k, kappa, A)


def Dipole_matrix(i, f, levels, VmeV, Mb, Mw, d):
    """analytical calculation of dipole matrix element. Returns value in metres 
    (electron charge is not included in calculation)"""
    ieven = i % 2 == 0
    feven = f % 2 == 0
    if ieven == feven:
        return 0.0
    if ieven == True:
        dpar = -1
    else:
        dpar = 1
    ki, kappai, Ai = _wavefunctions2(levels[i], ieven, VmeV, Mb, Mw, d)
    kf, kappaf, Af = _wavefunctions2(levels[f], feven, VmeV, Mb, Mw, d)
    a = d / 2.0
    ktot = ki + kf
    sin1 = sin(ktot * a)
    cos1 = cos(ktot * a)
    dk = ki - kf
    sin2 = sin(dk * a)
    cos2 = cos(dk * a)
    ikappatot = 1.0 / (kappai + kappaf)
    well = sin1 / ktot ** 2 - cos1 * a / ktot + dpar * (sin2 / dk ** 2 - cos2 * a / dk)
    barrier = (sin1 + dpar * sin2) * (a + ikappatot) * ikappatot
    dipole = Ai * Af * (well + barrier)
    return dipole


def Dipole_matrix_numeric(z, Psi1, Psi2):
    """Calculates dipole matrix element numerically. Returns values in metres
    (electron charge is not included in calculation)"""
    return simps(z * Psi1(z) * Psi2(z), z)


def OscStr(mu_if, w_if, Mw):
    """Calculates oscillator strength. w_if - frequency of transition (meV),
    Mw - relative effective electron mass in well layer, mu_if - dipole matrix element
    for position operator (m)."""
    return 2 * Mw * Me * (w_if * 0.001 * eC) * mu_if ** 2 / hbar ** 2


def S(i, j, levels, VmeV, Mb, Mw, d):
    """Returns S_ij"""
    ieven = i % 2 == 0
    jeven = j % 2 == 0
    if ieven == True:
        fi, si = cos, 1
    else:
        fi, si = sin, -1
    ki = sqrt(2 * Mw * Me * levels[i] * 0.001 * eC) / hbar
    kappai = sqrt(2 * Mb * Me * (VmeV - levels[i]) * 0.001 * eC) / hbar
    Ai = 1.0 / sqrt(d / 2.0 + si * sin(ki * d) / 2.0 / ki + fi(ki * d / 2.0) ** 2 / kappai)
    Bi = Ai * fi(ki * d / 2.0) * exp(kappai * d / 2)
    if jeven == True:
        fj, sj = cos, 1
    else:
        fj, sj = sin, -1
    kj = sqrt(2 * Mw * Me * levels[j] * 0.001 * eC) / hbar
    kappaj = sqrt(2 * Mb * Me * (VmeV - levels[j]) * 0.001 * eC) / hbar
    Aj = 1.0 / sqrt(d / 2.0 + sj * sin(kj * d) / 2.0 / kj + fj(kj * d / 2.0) ** 2 / kappaj)
    Bj = Aj * fj(ki * d / 2.0) * exp(kappaj * d / 2)
    ksum = ki + kj
    kdif = kj - ki
    t = si * sj
    I2 = kdif ** 2 / 2.0 * (d - t * sin(ksum * d) / ksum) + ksum ** 2 / 2.0 * (d - t * sin(kdif * d) / kdif) + -sj * kdif * ksum * (sin(kj * d) / kj - t * sin(ki * d) / ki)
    I2 *= (Ai * Aj / 2.0) ** 2
    kappasum = kappaj + kappai
    kappadif = kappaj - kappai
    I13 = (Bj * Bi * kappadif) ** 2 / kappasum * exp(-kappasum * d)
    S = (hbar ** 2 / (2 * Me * (levels[j] - levels[i]) * meV2J)) ** 2 * (I2 / Mw ** 2 + I13 / Mw ** 2)
    return S


def S_num(z, Psi1, Psi2, w_if, Mw):
    """Calculates S, a quantity used to calculate the effective thickness of an
    intersubband transition of a quantum well. w_if is the transitions frequency
    in meV, Mw -relative effective electron mass in well layer"""
    dz = (z[1] - z[0]) * 0.1
    integral = simps((derivative(Psi2, z, dx=dz, n=1) * Psi1(z) - Psi2(z) * derivative(Psi1, z, dx=dz, n=1)) ** 2, z)
    return (hbar ** 2 / (2 * Mw * Me * w_if * meV2J)) ** 2 * integral


def L_eff(w_if, S, Mw):
    """Calculates the effective thickness of an intersubband transition of a quantum
    well. w_if is the transitions frequency in meV, Mw is the relative effective 
    electron mass in well layer, S is a dimensionless quantity calculated via an
    integral. Returns a value in metres"""
    return hbar ** 2 / (2 * S * Mw * Me * w_if * meV2J)


import pyFresnelInit
from pyLuminous.transfer_matrix import LayerUniaxial_eps

def QW_GUI(VmeV, Mb, Mw, d, Ns, T, b=2e-07, eps_b=1.0, gammaf=0.1, mag=1.0, figures=False):
    """VmeV -barrier height (meV)
    Mw -effective mass in well (relative to Me)
    Mb -effective mass in barrier (relative to Me)
    d -width of well (m)
    Ns -doping (1E11cm-2)
    T -Temperature (K)
    b -width of barrier (m)
    eps_b -background dielectric constant
    gammaf -broadening factor for absorption plot, broadeningij=gammaf*wij
    mag -scaling factor between wavefunctions and potential well
    """
    ISBT = LayerUniaxial_eps(eps_b, eps_b, d + b)
    ISBT.VmeV = VmeV
    ISBT.Mw = Mw
    ISBT.Mb = Mb
    ISBT.Ns = Ns
    ISBT.T = T
    ISBT.well_width = d
    ISBT.barrier_width = b
    ISBT.eps_b = eps_b
    V = VmeV * eC * 0.001
    levels, evenlevels, oddlevels = EnergyLevels(V, Mb, Mw, d)
    ISBT.levels = levels
    Nsteps = 900.0
    z = N.linspace(-3 * d / 2, 3 * d / 2, Nsteps)
    if figures:
        f1 = P.figure(5)
        ax1 = f1.add_subplot(211)
        ax1.set_ylabel('Even Solutions (at crossings)')
        ax1.set_xlabel('Energy (meV)')
        ax2 = f1.add_subplot(212)
        ax2.set_ylabel('Odd Solutions (at crossings)')
        ax2.set_xlabel('Energy (meV)')
        Eaxis_meV = N.arange(1, VmeV, 0.1)
        Eaxis_J = Eaxis_meV * 0.001 * eC
        ax1.plot(Eaxis_meV, even_lhs(Eaxis_J, Mb, Mw, d))
        ax1.plot(Eaxis_meV, rhs(Eaxis_J, Mb, Mw, d, V))
        [ ax1.axvline(el) for el in evenlevels ]
        ax2.plot(Eaxis_meV, odd_lhs(Eaxis_J, Mb, Mw, d))
        ax2.plot(Eaxis_meV, rhs(Eaxis_J, Mb, Mw, d, V))
        [ ax2.axvline(ol) for ol in oddlevels ]
        ax1.set_ylim(-20, 20)
        ax2.set_ylim(-20, 20)
        mag *= VmeV / len(levels) / 20000.0
        f2 = P.figure(6)
        ax3 = f2.add_subplot(111)
        ax3.set_ylabel('Energy (meV)')
        ax3.vlines([-d / 2.0, d / 2.0], 0.0, VmeV)
        ax3.hlines(0.0, -d / 2.0, d / 2.0)
        ax3.hlines(VmeV, -d / 2 - d, -d / 2)
        ax3.hlines(VmeV, d / 2, d / 2 + d)
        ISBT.Psi = []
        for i, level in enumerate(levels):
            parity = i % 2 == 0
            Psi = wavefunctions(level, parity, VmeV, Mb, Mw, d)
            ISBT.Psi.append(Psi)
            ax3.hlines(level, -d, d, color='r')
            ax3.plot(z, mag * Psi(z) + level, 'b')

        ax3.set_xlabel('Distance (nm)')
        ticks = ax3.get_xticks() * 1000000000.0
        ax3.set_xticklabels(ticks)
    print 'the barrier is ', VmeV, 'meV high'
    print 'the well is ', d, 'm wide'
    print 'the electron mass in the well is ', Mw, 'm_e'
    print 'the electron mass in the barrier is ', Mb, 'm_e'
    print
    print 'the energy levels are (meV):'
    for level in levels:
        print '\t', level

    print
    print 'the energy levels gaps are (meV) (THz) (um) (wavno):'
    gaps = levels[1:] - levels[:-1]
    for gap, freq, wav, wavno in zip(gaps, gaps * 0.001 * eC / h / 1000000000000.0, 1000000.0 * h * c / (gaps * 0.001 * eC), gaps * 0.001 * eC / h / c * 0.01):
        print '\t', gap, '\t', freq, '\t', wav, '\t', wavno

    print
    print 'Doping'
    EF_0K, Nlevels_0K = FermiLevel_0K(Ns, levels, Mw)
    print 'At 0K, the Fermi level is ', EF_0K, 'meV'
    print '                          ', EF_0K - levels[0], 'meV above E0'
    print 'The level populations are (1E11cm-2):'
    for Nn in Nlevels_0K:
        print '\t', Nn

    print
    EF, Nlevels = FermiLevel(T, Ns, levels, Mw)
    print 'At ', T, 'K, kBT is ', kB * T / eC * 1000.0, ' meV'
    print 'and the Fermi-Level is ', EF, 'meV'
    print '                       ', EF - levels[0], 'meV above E0'
    if figures:
        ax3.hlines(EF, -d, +d, color='green')
    print 'The level populations are (1E11cm-2):'
    for Nn in Nlevels:
        print '\t', Nn

    ISBT.Nlevels = Nlevels
    print
    print 'Summary of Intersubband Transitions'
    hdr = ['ilevel', 'flevel', 'dE', 'freq', 'lambda', 'wavno', 'dN @%gK' % T, 'z', 'z_num', 'f', 'Leff', 'S_if_num', 'S_if', 'wp']
    units = ['', '', 'meV', 'THz', 'um', 'cm-1', '1e11cm-2', 'nm', 'nm', '', 'nm', 'nm', 'nm', 'THz']
    table = [hdr, units]

    def transition(i, j):
        meV = levels[j] - levels[i]
        THz = meV * 0.001 * eC / h / 1000000000000.0
        um = 1000000.0 * h * c / (meV * 0.001 * eC)
        wavno = meV * 0.001 * eC / h / c * 0.01
        dN = Nlevels[i] - Nlevels[j]
        mu = Dipole_matrix(i, j, levels, VmeV, Mb, Mw, d)
        Psi1 = wavefunctions(levels[i], i % 2 == 0, VmeV, Mb, Mw, d)
        Psi2 = wavefunctions(levels[j], j % 2 == 0, VmeV, Mb, Mw, d)
        mu_num = Dipole_matrix_numeric(z, Psi1, Psi2)
        f = OscStr(mu, meV, Mw)
        Sij_num = S_num(z, Psi1, Psi2, meV, Mw)
        Sij = S(i, j, levels, VmeV, Mb, Mw, d)
        Lij = L_eff(meV, Sij_num, Mw)
        wp = sqrt(dN * 1000000000000000.0 * eC ** 2 / (Mw * Me * eps_b * eps0 * Lij)) / (2 * pi)

        def invepsij(w):
            """wp, w and THz are all real frequencies in this function"""
            return Lij / (d + b) * wp ** 2 * f / ((THz * 1000000000000.0) ** 2 + wp ** 2 - w ** 2 - complex(0.0, 2.0) * (THz * 1000000000000.0) * gammaf * w)

        col = (
         i, j, meV, THz, um, wavno, dN, mu * 1000000000.0, mu_num * 1000000000.0, f, Lij * 1000000000.0, Sij_num * 1000000000.0, Sij * 1000000000.0, wp * 1e-12)
        return (
         col, invepsij)

    inveps = []
    for i, j in transition_generator(N.arange(len(levels))):
        col, invepsij = transition(i, j)
        inveps.append(invepsij)
        table.append(col)

    wids = [8, 9] + [11] * (len(table[0]) - 2)
    for row in zip(*table):
        print ('').join([row[0].rjust(wids[0]), row[1].rjust(wids[1])] + [ ('%.3g' % item).rjust(wid) for wid, item in zip(wids[2:], row[2:]) ])

    ISBT.transitions = table

    def epszz(w):
        """Calculates the zz dielectric constant for a quantum well. w - should be
        an array of frequency values (natural)."""
        epszz = eps_b / (1.0 - sum([ transition(w / 2 / pi) for transition in inveps ]))
        return epszz

    ISBT.epszz = epszz

    def absorption(w, theta):
        """Calculates the (approximate) absorption of a quantum well. 
        w - array of frequency values (real frequency) 
        theta - angle of incidence (rad)"""
        return sum([ transition(w) for transition in inveps ]).imag * sqrt(eps_b) * w / c * sin(theta) ** 2 / cos(theta) * (d + b)

    ISBT.absorption = absorption
    if figures:
        f3 = P.figure(7)
        ax4 = f3.add_subplot(111)
        wmin = min([ line[3] for line in table[2:] ]) * 1000000000000.0 * 0.5
        wmax = max([ line[3] for line in table[2:] ]) * 1000000000000.0 * 2.0
        w = N.linspace(wmin, wmax, 500)
        ax4.plot(w * 1e-12, absorption(w, pi / 4))
        ax4.set_xlabel('Frequency (THz)')
        ax4.set_ylabel('Absorption')
        P.show()
    return ISBT


if __name__ == '__main__':
    x = 0.15
    VmeV = 835.5 * x
    Mw = 0.067
    Mb = 0.067 + 0.083 * x
    d = 1e-08
    Ns = 18.0
    T = 30
    eps_b = 10
    N.set_printoptions(precision=3)
    ISBT = QW_GUI(VmeV, Mb, Mw, d, Ns, T, eps_b=eps_b, figures=True)