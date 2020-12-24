# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/obpds/ifdint.py
# Compiled at: 2015-04-23 21:09:33
"""
Fermi-Dirac integrals
    
[1] T. Fukushima, "Precise and fast computation of Fermi-Dirac integral
    of integer and half integer order by piecewise minimax rational
    approximation," Applied Mathematics and Computation, vol. 259,
    pp. 708-729, May 2015.
"""
import numpy
from numpy import exp, sqrt, log
from scipy.optimize import newton
from fdint import fdk, dfdk
__all__ = [
 'ifd1h']

def _ifd1h(nu):
    """
    Inverse Fermi-Dirac integral of order 1/2.

    Parameters
    ----------
    nu : float
        normalized carrier concentration, n/Nc.
    
    Returns
    -------
    eta : float
        normalized Fermi energy, (phi_n-Ec)/Vt
    """
    f = lambda eta: fdk(0.5, eta) - nu
    fprime = lambda eta: dfdk(0.5, eta)
    if nu < 10:
        guess = log(nu)
    else:
        guess = nu ** 1.5
    return newton(f, guess, fprime=fprime)


ifd1h = numpy.vectorize(_ifd1h)
if __name__ == '__main__':
    import matplotlib.pyplot as plt
    _, ax = plt.subplots()
    nu = numpy.logspace(-10, 3, 10000)
    ax.semilogx(nu, ifd1h(nu))
    plt.show()