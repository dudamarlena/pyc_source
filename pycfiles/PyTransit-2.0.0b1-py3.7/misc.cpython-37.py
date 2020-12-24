# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/pytransit/utils/misc.py
# Compiled at: 2020-01-13 18:32:58
# Size of source mod 2**32: 2641 bytes
import numpy as np
from scipy.constants import c, k, h
from scipy.optimize import fmin

def fold(time, period, origo=0.0, shift=0.0, normalize=True, clip_range=None):
    """Folds the given data over a given period.

    Parameters
    ----------
    
      time        
      period      
      origo       
      shift       
      normalize   
      clip_range  

    Returns
    -------

      phase       
    """
    tf = ((time - origo) / period + shift) % 1.0
    if not normalize:
        tf *= period
    if clip_range is not None:
        mask = np.logical_and(clip_range[0] < tf, tf < clip_range[1])
        tf = (tf[mask], mask)
    return tf


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
    return 2 * h * c ** 2 / wl ** 5 / (np.exp(h * c / (wl * k * T)) - 1)


def contamination_bb(c1, T, wl1, wl2):
    """Contamination from a third object radiating as a black-body given a contamination estimate in a reference wavelength. 

    Parameters
    ----------

      c1   : Contamination in the reference wavelength [-]
      T    : Temperature                               [K]
      wl1  : Reference wavelength                      [m]
      wl2  : Target wavelength                         [m]

    Returns
    -------

      c2  : Contamination in the given wavelength      [-]
    """
    B1 = planck(T, wl1)
    B2 = planck(T, wl2)
    return c1 * (B2 / B1)


def nonlinear_ld_to_general_ld(ldc):

    def nl(mu, ld):
        return 1.0 - np.sum([ld[(i - 1)] * (1.0 - mu ** (0.5 * i)) for i in range(1, 5)], axis=0)

    def gn(mu, ld):
        return 1.0 - np.sum([ld[(i - 1)] * (1.0 - mu ** i) for i in range(1, 5)], axis=0)

    mu = np.linspace(0, 1, 200)
    pvg = fmin(lambda pv: sum((Inl - gn(mu, pv)) ** 2), ld[::2])