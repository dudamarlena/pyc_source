# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/mx/Dropbox (MIT)/Science/Code/allesfitter/allesfitter/exoworlds_rdx/lightcurves/conversions.py
# Compiled at: 2018-11-09 10:58:00
# Size of source mod 2**32: 1796 bytes
__doc__ = '\nCreated on Thu Nov  8 17:49:54 2018\n\n@author:\nMaximilian N. Günther\nMIT Kavli Institute for Astrophysics and Space Research, \nMassachusetts Institute of Technology,\n77 Massachusetts Avenue,\nCambridge, MA 02109, \nUSA\nEmail: maxgue@mit.edu\nWeb: www.mnguenther.com\n'
from __future__ import print_function, division, absolute_import
import seaborn as sns
sns.set(context='paper', style='ticks', palette='deep', font='sans-serif', font_scale=1.5, color_codes=True)
sns.set_style({'xtick.direction':'in',  'ytick.direction':'in'})
sns.set_context(rc={'lines.markeredgewidth': 1})
import numpy as np
import matplotlib.pyplot as plt

def get_normalized_flux_from_normalized_mag(normalized_mag, normalized_mag_err=None):
    """
    Inputs:
    -------
    
    normalized_mag : float or array of float
        the normalized magnitude (i.e. centered around 0)
        
    normalized_mag_err : float or array of float (optional; default is None)
        the error on the normalized magnitude
        if not given, only the normalized_flux is returned
        if given, both the normalized_flux and the normalized_flux_err are returned
        
    
    Returns:
    --------
    
    normalized_flux : float or array of float
        the normalized_flux
        
    normalized_flux_err: float or array of float
        the error on the normalized_flux
    """
    if normalized_mag_err is None:
        normalized_flux = 10.0 ** (-normalized_mag / 2.5)
        return normalized_flux
    normalized_flux = 10.0 ** (-normalized_mag / 2.5)
    conv = 2.5 / np.log(10)
    normalized_flux_err = normalized_mag_err / conv * normalized_flux
    return (
     normalized_flux, normalized_flux_err)