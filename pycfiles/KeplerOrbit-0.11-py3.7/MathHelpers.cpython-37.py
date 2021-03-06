# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/KeplerOrbit/MathHelpers.py
# Compiled at: 2020-04-10 17:56:35
# Size of source mod 2**32: 2041 bytes
import numpy as np

def cross(x1, y1, z1, x2, y2, z2):
    xc = y1 * z2 - z1 * y2
    yc = z1 * x2 - x1 * z2
    zc = x1 * y2 - y1 * x2
    return (xc, yc, zc)


def dot(x1, y1, z1, x2, y2, z2):
    return x1 * x2 + y1 * y2 + z1 * z2


def nr(M, ecc, epsilon_target=1e-05):
    """
    Newton-Raphson Iteration.
    Computes Eccentric/Hyperbolic Anomaly from Mean Anomaly.
    Cf. Slide 13/26
    http://mmae.iit.edu/~mpeet/Classes/MMAE441/Spacecraft/441Lecture17.pdf
    """
    Ei = M
    ii = 1
    while True:
        if ecc < 1.0:
            Ei1 = Ei - (Ei - ecc * np.sin(Ei) - M) / (1.0 - ecc * np.cos(Ei))
        else:
            if ecc > 1.0:
                Ei1 = Ei + (M - ecc * np.sinh(Ei) + Ei) / (ecc * np.cosh(Ei) - 1.0)
        epsilon = np.abs(Ei1 - Ei)
        Ei = Ei1
        if epsilon < epsilon_target:
            break
        if ii > 100:
            raise Exception('NR Iteration Failed To Converge.')
        ii += 1

    return Ei1


def PQW(Omega, omega, inc):
    """
    Rotation Matrix Components (Orbit Frame => Inertial Frame)
    http://biomathman.com/pair/KeplerElements.pdf (End)
    http://astro.geo.tu-dresden.de/~klioner/celmech.pdf (Eqn. 2.30)
    NB: Shapiro Notation Tricky; Multiplies x = R.T * X, Dresden x = R * X
    """
    Px = np.cos(omega) * np.cos(Omega) - np.sin(omega) * np.cos(inc) * np.sin(Omega)
    Py = np.cos(omega) * np.sin(Omega) + np.sin(omega) * np.cos(inc) * np.cos(Omega)
    Pz = np.sin(omega) * np.sin(inc)
    Qx = -np.sin(omega) * np.cos(Omega) - np.cos(omega) * np.cos(inc) * np.sin(Omega)
    Qy = -np.sin(omega) * np.sin(Omega) + np.cos(omega) * np.cos(inc) * np.cos(Omega)
    Qz = np.sin(inc) * np.cos(omega)
    return (
     Px, Py, Pz, Qx, Qy, Qz)