# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/pytransit/utils/physics.py
# Compiled at: 2020-01-13 18:32:58
# Size of source mod 2**32: 1477 bytes
from numpy import exp
from scipy.constants import c, k, h
from numba import jit

@jit
def planck(T, wl):
    """Radiance as a function or black-body temperature and wavelength.

    Parameters
    ----------

      T   : Temperature  [K]
      wl  : Wavelength   [m]

    Returns
    -------

      B   : Radiance
    """
    return 2 * h * c ** 2 / wl ** 5 / (exp(h * c / (wl * k * T)) - 1.0)


@jit
def planck_ratio(T1, T2, wl):
    """Ratio of the two black-body object radiances

    Parameters
    ----------

      T1  : Temperature  [K]
      T2  : Temperature  [K]
      wl  : Wavelength   [m]

    Returns
    -------

      rB   : Radiance ratio
    """
    return (exp(h * c / (wl * k * T2)) - 1.0) / (exp(h * c / (wl * k * T1)) - 1.0)