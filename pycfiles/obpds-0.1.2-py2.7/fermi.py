# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/obpds/fermi.py
# Compiled at: 2015-04-23 21:09:33
import numpy
from numpy import exp, log, sqrt, pi
from fdint import fdk, dfdk
from ifdint import ifd1h
__all__ = [
 'boltz_p', 'boltz_n', 'iboltz_p', 'iboltz_n',
 'dboltz_p', 'dboltz_n',
 'fermi_p', 'fermi_n', 'ifermi_p', 'ifermi_n',
 'dfermi_p', 'dfermi_n',
 'npfermi', 'npfermi_n', 'dnpfermi_n']

def boltz_p(phi_p, Ev, Nv, Vt):
    phi = (Ev - phi_p) / Vt
    return exp(phi) * Nv


def boltz_n(phi_n, Ec, Nc, Vt):
    phi = (phi_n - Ec) / Vt
    return exp(phi) * Nc


def iboltz_p(p, Ev, Nv, Vt):
    return Ev - log(p / Nv) * Vt


def iboltz_n(n, Ec, Nc, Vt):
    return Ec + log(n / Nc) * Vt


def dboltz_p(phi_p, Ev, Nv, Vt):
    phi = (Ev - phi_p) / Vt
    return -exp(phi) * Nv / Vt


def dboltz_n(phi_n, Ec, Nc, Vt):
    phi = (phi_n - Ec) / Vt
    return exp(phi) * Nc / Vt


assert 2 / sqrt(pi) == 1.1283791670955126

def fermi_p(phi_p, Ev, Nv, Vt):
    phi = (Ev - phi_p) / Vt
    return fdk(0.5, phi) * (Nv * 1.1283791670955126)


def fermi_n(phi_n, Ec, Nc, Vt):
    phi = (phi_n - Ec) / Vt
    return fdk(0.5, phi) * (Nc * 1.1283791670955126)


def ifermi_p(p, Ev, Nv, Vt):
    return Ev - ifd1h(p / (Nv * 1.1283791670955126)) * Vt


def ifermi_n(n, Ec, Nc, Vt):
    return Ec + ifd1h(n / (Nc * 1.1283791670955126)) * Vt


def dfermi_p(phi_p, Ev, Nv, Vt):
    phi = (Ev - phi_p) / Vt
    return -0.5 * fdk(-0.5, phi) * (Nv * 1.1283791670955126) / Vt


def dfermi_n(phi_n, Ec, Nc, Vt):
    phi = (phi_n - Ec) / Vt
    return 0.5 * fdk(-0.5, phi) * (Nc * 1.1283791670955126) / Vt


def _npfermi(phi, alpha):
    """
    Approximation of the Fermi-Dirac integral for a bulk semiconductor with
    a non-parabolic band. This approximation degrades significantly for
    alpha > 0.07, particularly at phi ~= 15.
    """
    if phi < 20:
        return fdk(0.5, phi) + alpha * (2.5 * fdk(1.5, phi) + alpha * (0.875 * fdk(2.5, phi) + alpha * (-0.1875 * fdk(3.5, phi) + alpha * (0.0859375 * fdk(4.5, phi) + alpha * (-0.05078125 * fdk(5.5, phi) + alpha * (0.0341796875 * fdk(6.5, phi) + alpha * (-0.02490234375 * fdk(7.5, phi) + alpha * (0.019134521484375 * fdk(8.5, phi) + alpha * (-0.0152740478515625 * fdk(9.5, phi) + alpha * (0.012546539306640625 * fdk(10.5, phi)))))))))))
    else:
        return 0.6666666666666666 * (phi * (1.0 + alpha * phi)) ** 1.5


npfermi = numpy.vectorize(_npfermi)

def _dnpfermi(phi, alpha):
    """
    Approximation of the derivative of the Fermi-Dirac integral for a bulk
    semiconductor with a non-parabolic band. This approximation degrades
    significantly for alpha > 0.07, particularly at phi ~= 15.
    """
    if phi < 20:
        return dfdk(0.5, phi) + alpha * (2.5 * dfdk(1.5, phi) + alpha * (0.875 * dfdk(2.5, phi) + alpha * (-0.1875 * dfdk(3.5, phi) + alpha * (0.0859375 * dfdk(4.5, phi) + alpha * (-0.05078125 * dfdk(5.5, phi) + alpha * (0.0341796875 * dfdk(6.5, phi) + alpha * (-0.02490234375 * dfdk(7.5, phi) + alpha * (0.019134521484375 * dfdk(8.5, phi) + alpha * (-0.0152740478515625 * dfdk(9.5, phi) + alpha * (0.012546539306640625 * dfdk(10.5, phi)))))))))))
    else:
        return 2.0 * (phi * (alpha * phi + 1)) ** 1.5 * (1.0 * alpha * phi + 0.5) / (phi * (alpha * phi + 1))


dnpfermi = numpy.vectorize(_dnpfermi)

def npfermi_n(phi_n, Ec, Nc, alpha, Vt):
    """
    Non-parabolic Fermi-Dirac integral.
    """
    phi = (phi_n - Ec) / Vt
    return npfermi(phi, alpha) * (Nc * 1.1283791670955126)


def dnpfermi_n(phi_n, Ec, Nc, alpha, Vt):
    """
    Derivative of the non-parabolic Fermi-Dirac integral.
    """
    phi = (phi_n - Ec) / Vt
    return dnpfermi(phi, alpha) * (Nc * 1.1283791670955126) / Vt


if __name__ == '__main__':
    from scipy.integrate import quad

    def _num_fermi(phi, alpha):
        result = quad(lambda x: sqrt(x) / (1.0 + exp(x - phi)), 0.0, numpy.inf)[0]
        return result


    num_fermi = numpy.vectorize(_num_fermi)

    def _num_npfermi(phi, alpha):
        result = quad(lambda x: sqrt(x * (1.0 + alpha * x)) * (1.0 + 2.0 * alpha * x) / (1.0 + exp(x - phi)), 0.0, numpy.inf)[0]
        return result


    num_npfermi = numpy.vectorize(_num_npfermi)
    import numpy, matplotlib.pyplot as plt
    _, ax = plt.subplots()
    phi = numpy.linspace(-30, 10, 10000)
    ax.semilogy(phi, exp(phi) / 1.1283791670955126, 'b')
    phi = numpy.linspace(-30, 100, 1000)
    ax.semilogy(phi, fdk(0.5, phi), 'r')
    from scipy.integrate import quad

    def _num_fd1h(phi):
        result = quad(lambda x: sqrt(x) / (1.0 + exp(x - phi)), 0.0, 100.0)[0]
        return result


    num_fd1h = numpy.vectorize(_num_fd1h)
    ax.semilogy(phi, num_fd1h(phi), 'r--', lw=2)
    phi = numpy.linspace(-30, 100, 1000)
    alpha = 0.07
    ax.semilogy(phi, npfermi(phi, alpha), 'g')
    ax.semilogy(phi, dnpfermi(phi, alpha), 'g:')
    ax.semilogy(phi, num_npfermi(phi, alpha), 'g--', lw=2)
    phi = -5
    print fdk(0.5, phi) / _num_fermi(phi, alpha)
    print _npfermi(phi, alpha) / _num_npfermi(phi, alpha)
    phi = 5
    print fdk(0.5, phi) / _num_fermi(phi, alpha)
    print _npfermi(phi, alpha) / _num_npfermi(phi, alpha)
    phi = 30
    print fdk(0.5, phi) / _num_fermi(phi, alpha)
    print _npfermi(phi, alpha) / _num_npfermi(phi, alpha)
    plt.show()