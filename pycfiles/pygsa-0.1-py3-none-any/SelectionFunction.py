# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.5-x86_64/egg/PyGS/SelectionFunction.py
# Compiled at: 2013-11-06 06:43:11
__doc__ = '\nCreated on Dec 3, 2012\n\n@author: Steven\n'
import sys
try:
    import matplotlib.pyplot as plt
except:
    sys.exit('Please install Matplotlib')

try:
    import numpy as np
except:
    sys.exit('Please install Numpy')

from scipy.optimize import curve_fit
import scipy.special as sp
from scipy.interpolate import InterpolatedUnivariateSpline as spline
import scipy.integrate as integ, utils

def fit_selection_simple(cdist, bins=None, verbose=True):
    """
    Fits the simple selection function to the N-d relation
    
    Fits for A,g,t
    """
    if not bins:
        bins = utils.FD_bins(cdist)
    hist, edges = np.histogram(cdist, normed=True, bins=bins)
    centres = edges[:-1] + (edges[1] - edges[0]) / 2.0
    popt, pcov = curve_fit(selection_simple, xdata=centres, ydata=hist, p0=(0.95, 2.0,
                                                                            340.0))
    if verbose:
        print 'PARAMETERS OF THE FIT AND THEIR STANDARD DEVIATION'
        print 'A: ', popt[0]
        print 'g: ', popt[1]
        print 't: ', popt[2]
    return (
     popt[0], popt[1], popt[2])


def fit_selection_simple_z(redshifts, bins=None, verbose=True):
    """
    Fits the simple selection function to the N-d relation
    
    Fits for A,g,t
    """
    if not bins:
        bins = utils.FD_bins(redshifts)
    hist, edges = np.histogram(redshifts, normed=True, bins=bins)
    centres = edges[:-1] + (edges[1] - edges[0]) / 2.0
    popt, pcov = curve_fit(selection_simple, xdata=centres, ydata=hist, p0=(0.95, 2.0,
                                                                            0.1))
    if verbose:
        print 'PARAMETERS OF THE FIT AND THEIR STANDARD DEVIATION'
        print 'A: ', popt[0]
        print 'g: ', popt[1]
        print 't: ', popt[2]
    return (
     popt[0], popt[1], popt[2])


def selection_simple(z, A, g, t):
    """
    Definition of the simple selection function (thesis eq.2.10)
    
    Original from Baugh, C., & Efstathiou, G. 1993, MNRAS, 265, 145
    Also in Percival, W. et. al. 2007 APJ, 657, 645
    """
    return A * z ** 2 * np.exp(-(z / t) ** g)


def get_sel_from_nd(A, g, t):
    norm = selection_simple(0.001, A, g, t) / 1e-06
    return lambda d: selection_simple(d, A, g, t) / (norm * d ** 2)


def selection_simple_integral(x, A, g, t):
    """
    Defines the integral of the simple selection function from 0 to x
    """
    return A * (1 / t) ** (-1 - g) * (sp.gamma(1 / g) - g * sp.gamma(1 + 1 / g) * sp.gammaincc(1 + 1 / g, (x / t) ** g)) / g ** 2


def simple_inv_cdf(z_max, A, g, t):
    """
    Interpolates the integral of the simple selection function as an inverse.
    """
    grid = np.linspace(0, z_max, 1000)
    print selection_simple_integral(grid, A, g, t)[:50]
    print selection_simple_integral(z_max, A, g, t)
    icdf = spline(selection_simple_integral(grid, A, g, t) / selection_simple_integral(z_max, A, g, t), grid)
    return icdf


def create_radial_selection_simple(A, g, t, z_min, z_max, N):
    """
    Creates a random catalogue of particles based on a defined selection function. Only radial co-ords.
    """
    padded_N = 2 * N
    X = np.random.random(padded_N)
    icdf = simple_inv_cdf(z_max, A, g, t)
    radii = icdf(X)
    radii = radii[((radii > z_min) & (radii < z_max))]
    if len(radii) > N:
        radii = radii[1:N]
        return radii
    while len(radii) < N:
        print 'in while loop'
        X = np.random.random(N)
        print len(X)
        new_radii = icdf(X)
        print len(new_radii)
        new_radii = new_radii[np.logical_and(radii > z_min, radii < z_max)]
        print len(new_radii)
        radii = np.append(radii, new_radii)
        print len(radii)

    radii = radii[1:N]
    return radii


def create_mock(s_of_z, zmin, zmax, N):
    maxval = np.max(np.exp(s_of_z(np.linspace(zmin, zmax, 1000))))
    x = np.random.rand(N) * (zmax - zmin) + zmin
    y = np.random.rand(N) * (maxval * 1.01)
    z = np.exp(s_of_z(x))
    redshifts = x[(y < z)]
    gens = 1.3 * np.ceil(float(N) / len(redshifts)) * N
    x = np.random.rand(gens) * (zmax - zmin) + zmin
    y = np.random.rand(gens) * (maxval * 1.01)
    z = np.exp(s_of_z(x))
    redshifts = np.concatenate((redshifts, x[(y < z)]))
    redshifts = redshifts[:N]
    return redshifts


def selection_of_galaxies(phi, Mbins, apmag, absmag):
    """Generates a selection function value for each galaxy"""
    cum_int = np.zeros_like(phi)
    for i in range(len(phi))[1:]:
        cum_int[i] = integ.simps(phi[:i], dx=Mbins[1] - Mbins[0])

    denom = cum_int[(-1)]
    M_max = apmag.max() - apmag + absmag
    M_min = apmag.min() - apmag + absmag
    mask_valid = np.logical_and(absmag < Mbins[(-1)], absmag > Mbins[0])
    sel_upper = np.zeros(len(M_max))
    sel_lower = np.zeros(len(M_max))
    sel_upper[M_max >= Mbins[(-1)]] = denom
    fit = spline(Mbins, cum_int, k=2)
    sel_upper[np.logical_and(M_max < Mbins[(-1)], mask_valid)] = fit(M_max[np.logical_and(M_max < Mbins[(-1)], mask_valid)])
    sel_lower[np.logical_and(M_min > Mbins[0], mask_valid)] = fit(M_min[np.logical_and(M_min > Mbins[0], mask_valid)])
    total = (sel_upper - sel_lower) / denom
    total[np.logical_not(mask_valid)] = np.nan
    return total


def selection_of_z(sel_bins, phi, Mbins, apmag, absmag, redshift):
    """
    Get selection function of redshift only
    
    Returns a function of z which gives the log of the selection function.
    """
    cum_int = np.zeros_like(phi)
    for i in range(len(phi))[1:]:
        cum_int[i] = integ.simps(phi[:i], dx=Mbins[1] - Mbins[0])

    fit = spline(Mbins, cum_int, k=2)
    denom = cum_int[(-1)]
    M_max = apmag.max() - apmag + absmag
    M_min = apmag.min() - apmag + absmag
    dz = (redshift.max() - redshift.min()) / sel_bins
    sel = np.zeros(sel_bins)
    centres = np.zeros(sel_bins)
    for i in range(sel_bins):
        mask = np.logical_and(redshift > redshift.min() + i * dz, redshift < redshift.max() + (i + 1) * dz)
        centres[i] = redshift.min() + (i + 0.5) * dz
        mmax = np.mean(M_max[mask])
        mmin = np.mean(M_min[mask])
        sel[i] = (fit(mmax) - fit(mmin)) / denom

    selfunc = spline(centres, np.log(sel), k=2)
    return selfunc