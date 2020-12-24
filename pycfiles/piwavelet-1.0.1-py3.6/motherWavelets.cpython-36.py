# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/piwavelet/motherWavelets.py
# Compiled at: 2020-03-19 11:26:12
# Size of source mod 2**32: 6280 bytes
from __future__ import division
__authors__ = 'Eduardo dos Santos Pereira'
__data__ = '17/01/2015'
__email__ = 'pereira.somoza@gmail.com'
from numpy import pi, exp, sqrt, prod
from scipy.special import gamma
from scipy.special.orthogonal import hermitenorm
from numpy.lib.polynomial import polyval

class Morlet:
    __doc__ = 'Implements the Morlet wavelet class.\n\n    Note that the input parameters f and f0 are angular frequencies.\n    f0 should be more than 0.8 for this function to be correct, its\n    default value is f0=6.\n\n    '
    name = 'Morlet'

    def __init__(self, f0=6.0):
        self._set_f0(f0)

    def psi_ft(self, f):
        """Fourier transform of the approximate Morlet wavelet."""
        return pi ** (-0.25) * exp(-0.5 * (f - self.f0) ** 2.0)

    def psi(self, t):
        """Morlet wavelet as described in Torrence and Compo (1998)"""
        return pi ** (-0.25) * exp(complex(0.0, 1.0) * self.f0 * t - t ** 2.0 / 2.0)

    def flambda(self):
        """Fourier wavelength as of Torrence and Compo (1998)"""
        return 4 * pi / (self.f0 + sqrt(2 + self.f0 ** 2))

    def coi(self):
        """e-Folding Time as of Torrence and Compo (1998)"""
        return 1.0 / sqrt(2.0)

    def sup(self):
        """Wavelet support defined by the e-Folding time"""
        return 1.0 / self.coi()

    def _set_f0(self, f0):
        self.f0 = f0
        self.dofmin = 2
        if self.f0 == 6.0:
            self.cdelta = 0.776
            self.gamma = 2.32
            self.deltaj0 = 0.6
        else:
            self.cdelta = -1
            self.gamma = -1
            self.deltaj0 = -1


class Paul:
    __doc__ = 'Implements the Paul wavelet class.\n\n    Note that the input parameter f is the angular frequency and that\n    the default order for this wavelet is m=4.\n\n    '
    name = 'Paul'

    def __init__(self, m=4):
        self._set_m(m)

    def psi_ft(self, f):
        """Fourier transform of the Paul wavelet."""
        return 2 ** self.m / sqrt(self.m * prod(range(2, 2 * self.m))) * f ** self.m * exp(-f) * (f > 0)

    def psi(self, t):
        """Paul wavelet as described in Torrence and Compo (1998)"""
        return 2 ** self.m * complex(0.0, 1.0) ** self.m * prod(range(2, self.m - 1)) / sqrt(pi * prod(range(2, 2 * self.m + 1))) * (1 - complex(0.0, 1.0) * t) ** (-(self.m + 1))

    def flambda(self):
        """Fourier wavelength as of Torrence and Compo (1998)"""
        return 4 * pi / (2 * self.m + 1)

    def coi(self):
        """e-Folding Time as of Torrence and Compo (1998)"""
        return sqrt(2.0)

    def sup(self):
        """Wavelet support defined by the e-Folding time"""
        return 1.0 / self.coi()

    def _set_m(self, m):
        self.m = m
        self.dofmin = 2
        if self.m == 4:
            self.cdelta = 1.132
            self.gamma = 1.17
            self.deltaj0 = 1.5
        else:
            self.cdelta = -1
            self.gamma = -1
            self.deltaj0 = -1


class DOG:
    __doc__ = 'Implements the derivative of a Guassian wavelet class.\n\n    Note that the input parameter f is the angular frequency and that\n    for m=2 the DOG becomes the Mexican hat wavelet, which is then\n    default.\n\n    '
    name = 'DOG'

    def __init__(self, m=2):
        self._set_m(m)

    def psi_ft(self, f):
        """Fourier transform of the DOG wavelet."""
        return -complex(0.0, 1.0) ** self.m / sqrt(gamma(self.m + 0.5)) * f ** self.m * exp(-0.5 * f ** 2)

    def psi(self, t):
        """DOG wavelet as described in Torrence and Compo (1998)

        The derivative of a Gaussian of order n can be determined using
        the probabilistic Hermite polynomials. They are explicitly
        written as:
            Hn(x) = 2 ** (-n / s) * n! * sum ((-1) ** m) * (2 ** 0.5 *
                x) ** (n - 2 * m) / (m! * (n - 2*m)!)
        or in the recursive form:
            Hn(x) = x * Hn(x) - nHn-1(x)

        Source: http://www.ask.com/wiki/Hermite_polynomials

        """
        p = hermitenorm(self.m)
        return (-1) ** (self.m + 1) * polyval(p, t) * exp(-t ** 2 / 2) / sqrt(gamma(self.m + 0.5))

    def flambda(self):
        """Fourier wavelength as of Torrence and Compo (1998)"""
        return 2 * pi / sqrt(self.m + 0.5)

    def coi(self):
        """e-Folding Time as of Torrence and Compo (1998)"""
        return 1.0 / sqrt(2.0)

    def sup(self):
        """Wavelet support defined by the e-Folding time"""
        return 1.0 / self.coi()

    def _set_m(self, m):
        self.m = m
        self.dofmin = 1
        if self.m == 2:
            self.cdelta = 3.541
            self.gamma = 1.43
            self.deltaj0 = 1.4
        else:
            if self.m == 6:
                self.cdelta = 1.966
                self.gamma = 1.37
                self.deltaj0 = 0.97
            else:
                self.cdelta = -1
                self.gamma = -1
                self.deltaj0 = -1


class Mexican_hat(DOG):
    __doc__ = 'Implements the Mexican hat wavelet class.\n\n    This class inherits the DOG class using m=2.\n\n    '
    name = 'Mexican hat'

    def __init__(self):
        self._set_m(2)