# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ambhas/radar_sm_models.py
# Compiled at: 2013-05-07 13:19:00
"""
Created on Tue May  7 12:57:49 2013

@author: Sat Kumar Tomer
@email: satkumartomer@gmail.com
@website: www.ambhas.com

"""
import numpy as np, matplotlib.pyplot as plt, warnings
from scipy.interpolate import interp1d, interp2d

def ep2mv(ep):
    """
    this function converts the real part of dielectric constant
    into the volumetric soil moisture
    
    The regression equation is based on the Topp et al. (1980,1985)
    Input:
        ep: real part of the dielectric constant
    Output:
        mv: soil moisture (v/v)
    """
    if np.max(ep) > 70 or np.min(ep) < 2:
        warnings.warn('input ep is less than 2 or greater than 0, replacing with nan!')
        ep[ep > 70] = np.nan
        ep[ep < 2] = np.nan
    mv = (-530 + 292 * ep - 5.5 * ep ** 2 + 0.043 * ep ** 3) * 0.0001
    return mv


def mv2ep(mv):
    """
    this function converts the soil moisture into 
    the real part of dielectric constant

    this uses the function ep2mv and invert it usign the LUT    
    
    Input:
        mv: soil moisture (v/v)
    Output:
        ep: real part of the dielectric constant
    """
    ep_lut = np.linspace(2, 70)
    mv_lut = ep2mv(ep_lut)
    f = interp1d(mv_lut, ep_lut, bounds_error=False, fill_value=np.nan)
    ep = f(mv)
    return ep


def dubois_forward(h, ep, theta, l, dB=True):
    """
    This function performs the forward modelling using the Dubois model
    Input:
        h: rms height (cm)
        ep: real part of the dielectric constant
        theta: incidence angel (degree)
        l: wavelength (cm)
        dB: the type of output
            True --> hh, vv in dB
            False --> hh, vv in linear      
    Output:
        hh: backscatter coefficient in hh pol (in dB if dB=True)
        vv: backscatter coefficient in vv pol (in dB if dB=True)
    """
    theta_rad = theta * np.pi / 180.0
    k = 2 * np.pi / l
    hh = 0.0017782794100389228 * (np.cos(theta_rad) ** 1.5 / np.sin(theta_rad ** 5)) * 10 ** (0.028 * ep * np.tan(theta_rad)) * (k * h * np.sin(theta_rad) ** 1.4) * l ** 0.7
    vv = 0.0044668359215096305 * (np.cos(theta_rad) ** 3.0 / np.sin(theta_rad)) * 10 ** (0.046 * ep * np.tan(theta_rad)) * (k * h * np.sin(theta_rad) ** 3.0) ** 1.1 * l ** 0.7
    if dB:
        hh = 10 * np.log10(hh)
        vv = 10 * np.log10(vv)
    return (hh, vv)


def dubois_inverse(hh, vv, theta, l, dB=True):
    """
    This function performs the forward modelling using the Dubois model
    Input:
        hh: backscatter coefficient in hh pol (in dB if dB=True)
        vv: backscatter coefficient in vv pol (in dB if dB=True)
        theta: incidence angel (degree)
        l: wavelength (cm)
    Output:
        h: rms height (cm)
        ep: real part of the dielectric constant
    """
    h_lut = np.linspace(0, 5)
    ep_lut = np.linspace(2, 70, 100)
    h_LUT, ep_LUT = np.meshgrid(h_lut, ep_lut)
    hh_lut, vv_lut = dubois_forward(h_LUT, ep_LUT, theta, l, dB=dB)
    return (
     hh_lut, vv_lut)