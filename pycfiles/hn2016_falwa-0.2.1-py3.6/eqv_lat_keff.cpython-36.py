# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/hn2016_falwa/eqv_lat_keff.py
# Compiled at: 2017-09-26 18:03:40
# Size of source mod 2**32: 5430 bytes
""" eqv_lat contains 2 modules that compute equivalent-latitude relationship Q(y)
(See Nakamura 1996, Allen and Nakamura 2003, etc) with a global domain (EqvLat)
or hemispheric domain (EqvLat_hemispheric) as in Huang and Nakamura (2016).

The computation of Q(y) with hemispheric domain is preferrable when studying
a QGPV field, in which the meridional gradient of QGPV near equator is vanishing.

The use of hemispheric domain is necessary to compute the surface wave activity
(B in Nakamura and Solomon (2010) equation (15)) from potential temperature field
because there is a reversal of meridional gradient at the equator.

Please make inquiries and report issues via Github: https://github.com/csyhuang/hn2016_falwa/issues
"""
from math import pi
import numpy as np

def eqvlat(ylat, vort, area, n_points, planet_radius=6378000.0, vgrad=None):
    """
    Input variables:
        ylat: 1-d numpy array of latitude (in degree) with equal spacing in
              ascending order; dimension = nlat
        vort: 2-d numpy array of vorticity values; dimension = [nlat_s x nlon]
        area: 2-d numpy array specifying differential areal element of each
              grid point; dimension = [nlat_s x nlon]
        n_points: analysis resolution to calculate equivalent latitude.
        planet_radius: scalar; radius of spherical planet of interest consistent
        with input 'area'
        vgrad: (optional) 2-d numpy array of laplacian (or higher-order laplacian)
        values; dimension = [nlat_s x nlon]

    Output variables:
        q_part: 1-d numpy array of value Q(y) where latitude y is given by ylat.
        brac: (output if vgrad is not None) averaged vgrad in the square bracket
    """
    vort_min = np.min([vort.min(), vort.min()])
    vort_max = np.max([vort.max(), vort.max()])
    q_part_u = np.linspace(vort_min, vort_max, n_points, endpoint=True)
    aa = np.zeros(q_part_u.size)
    vort_flat = vort.flatten()
    area_flat = area.flatten()
    if vgrad is not None:
        dp = np.zeros_like(aa)
        vgrad_flat = vgrad.flatten()
    inds = np.digitize(vort_flat, q_part_u)
    for i in np.arange(0, aa.size):
        aa[i] = np.sum(area_flat[np.where(inds == i)])
        if vgrad is not None:
            dp[i] = np.sum(area_flat[np.where(inds == i)] * vgrad_flat[np.where(inds == i)]) / aa[i]

    aq = np.cumsum(aa)
    if vgrad is not None:
        brac = np.zeros_like(aa)
        brac[1:-1] = 0.5 * (dp[:-2] + dp[2:])
    y_part = aq / (2 * pi * planet_radius ** 2) - 1.0
    lat_part = np.arcsin(y_part) * 180 / pi
    q_part = np.interp(ylat, lat_part, q_part_u)
    if vgrad is not None:
        brac_return = np.interp(ylat, lat_part, brac)
        return (
         q_part, brac_return)
    else:
        return q_part


def eqvlat_hemispheric(ylat, vort, area, nlat_s=61, planet_radius=6378000.0, vgrad=None):
    """
    Input variables:
        ylat: 1-d numpy array of latitude (in degree) with equal spacing in
              ascending order; dimension = nlat
        vort: 2-d numpy array of vorticity values; dimension = [nlat_s x nlon]
        area: 2-d numpy array specifying differential areal element of each
              grid point; dimension = [nlat_s x nlon]
        nlat_s: the index of grid point that defines the extent of hemispheric
                domain from the pole. The default is 61 for ERA-Interim data of
                latitudinal resolution of 1.5 deg.
        planet_radius: scalar; radius of spherical planet of interest consistent
                       with input 'area'
        vgrad: (optional) 2-d numpy array of laplacian (or higher-order laplacian)
        values; dimension = [nlat_s x nlon]

    Output variables:
        q_part: 1-d numpy array of value Q(y) where latitude y is given by ylat.
        brac: (output if vgrad is not None) averaged vgrad in the square bracket
    """
    nlat = vort.shape[0]
    qref = np.zeros(nlat)
    brac = np.zeros(nlat)
    if vgrad is not None:
        qref1, brac1 = eqvlat((ylat[:nlat_s]), (vort[:nlat_s, :]), (area[:nlat_s, :]), nlat_s,
          planet_radius=planet_radius, vgrad=vgrad)
    else:
        qref1 = eqvlat((ylat[:nlat_s]), (vort[:nlat_s, :]), (area[:nlat_s, :]), nlat_s,
          planet_radius=planet_radius)
    qref[:nlat_s] = qref1
    vort2 = -vort[::-1, :]
    if vgrad is not None:
        qref2, brac2 = eqvlat((ylat[:nlat_s]), (vort2[:nlat_s, :]), (area[:nlat_s, :]), nlat_s,
          planet_radius=planet_radius, vgrad=vgrad)
    else:
        qref2 = eqvlat((ylat[:nlat_s]), (vort2[:nlat_s, :]), (area[:nlat_s, :]), nlat_s,
          planet_radius=planet_radius)
    qref[-nlat_s:] = qref2[::-1]
    if vgrad is not None:
        brac[:nlat_s] = brac1
        brac[-nlat_s:] = brac2[::-1]
    return (qref, brac)