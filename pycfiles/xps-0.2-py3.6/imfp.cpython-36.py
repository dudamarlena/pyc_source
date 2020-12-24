# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.openbsd-6.5-amd64/egg/xps/scatter/imfp.py
# Compiled at: 2019-06-04 15:28:04
# Size of source mod 2**32: 2111 bytes
"""
imfp.py

Equations relating to the Inelastic Mean Free Path (IMFP) of electrons

References
----------
IMFP TPP-2M (TPP-2 modified eqution)
    S. Tanuma, C. J. Powell, D. R. Penn: Surf. Interf. Anal.,Vol. 21, 165 (1994)
"""
from numpy import log as _log
from numpy import sqrt as _sqrt

def imfp_TPP2M(Ek, rho, M, Nv, Eg, units='Angstroms'):
    """The TPP-2M is the modified TPP-2 equation for estimating inelastic
    mean free paths (IMFP)

    S. Tanuma, C. J. Powell, D. R. Penn: Surf. Interf. Anal.,Vol. 21, 165 (1994)

    Ek    : Kinetic energy [eV]
    rho   : Density (g/cm**3)
    M     : Atomic or molar mass
    Nv    : Valence electrons
    Eg    : Bandgap energy [eV]
    units : 'Angstroms' or 'SI' [default: AA, or 1E-10 m]

    returns IMFP in Angstroms or meters [default: AA, or 1E-10 m]
    """
    U = Nv * rho / M
    C = 1.97 - 0.91 * U
    D = 53.4 - 20.8 * U
    Eplasmon = _sqrt(829.4 * U)
    gamma = 0.191 * rho ** (-0.5)
    betaM = -0.1 + 0.944 / _sqrt(Eplasmon ** 2 + Eg ** 2) + 0.069 * rho ** 0.1
    imfp = Ek / (Eplasmon ** 2 * (betaM * _log(gamma * Ek) - C / Ek + D / Ek ** 2))
    if units.upper() == 'SI':
        return imfp * 1e-10
    else:
        return imfp


if __name__ == '__main__':
    pass