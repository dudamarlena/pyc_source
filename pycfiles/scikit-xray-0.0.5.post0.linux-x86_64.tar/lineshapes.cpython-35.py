# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/edill/mc/lib/python3.5/site-packages/skxray/core/fitting/lineshapes.py
# Compiled at: 2016-03-04 05:19:32
# Size of source mod 2**32: 12769 bytes
from __future__ import absolute_import, division, print_function
import numpy as np, scipy.special, six
log2 = np.log(2)
s2pi = np.sqrt(2 * np.pi)
spi = np.sqrt(np.pi)
s2 = np.sqrt(2.0)

def gaussian(x, area, center, sigma):
    """1 dimensional gaussian:
    gaussian(x, amplitude, center, sigma)

    Parameters
    ----------
    x : array
        independent variable
    area : float
        Area of the normally distributed peak
    center : float
        center position
    sigma : float
        standard deviation
    """
    return area / (s2pi * sigma) * np.exp(-(1.0 * x - center) ** 2 / (2 * sigma ** 2))


def lorentzian(x, area, center, sigma):
    """1 dimensional lorentzian
    lorentzian(x, amplitude, center, sigma)

    Parameters
    ----------
    x : array
        independent variable
    area : float
        area of lorentzian peak,
        If area is set as 1, the integral is unity.
    center : float
        center position
    sigma : float
        standard deviation
    """
    return area / (1 + ((1.0 * x - center) / sigma) ** 2) / (np.pi * sigma)


def lorentzian2(x, area, center, sigma):
    """
    1-d lorentzian squared profile

    Parameters
    ----------
    x : array
        independent variable
    area : float
        area of lorentzian squared peak,
        If area is set as 1, the integral is unity.
    center : float
        center position
    sigma : float
        standard deviation
    """
    return area / (1 + ((x - center) / sigma) ** 2) ** 2 / (np.pi * sigma)


def voigt(x, area, center, sigma, gamma=None):
    """1 dimensional voigt function.
    see http://en.wikipedia.org/wiki/Voigt_profile
    1 dimensional voigt function, the convolution between gaussian and
    lorentzian curve.

    Parameters
    ----------
    x : array
        independent variable
    area : float
        area of voigt peak
    center : float
        center position
    sigma : float
        standard deviation
    gamma : float, optional
        half width at half maximum of lorentzian.
        If optional, `gamma` gets set to `sigma`
    """
    if gamma is None:
        gamma = sigma
    z = (x - center + complex(0.0, 1.0) * gamma) / (sigma * s2)
    return area * scipy.special.wofz(z).real / (sigma * s2pi)


def pvoigt(x, area, center, sigma, fraction):
    """1 dimensional pseudo-voigt:
    pvoigt(x, area, center, sigma, fraction)
       = amplitude*(1-fraction)*gaussion(x, center,sigma) +
         amplitude*fraction*lorentzian(x, center, sigma)

    1 dimensional pseudo-voigt, linear combination of gaussian and lorentzian
    curve.

    Parameters
    ----------
    x : array
        independent variable
    area : float
        area of pvoigt peak
    center : float
        center position
    sigma : float
        standard deviation
    fraction : float
        weight for lorentzian peak in the linear combination, and (1-fraction)
        is the weight
        for gaussian peak.
    """
    return (1 - fraction) * gaussian(x, area, center, sigma) + fraction * lorentzian(x, area, center, sigma)


def gausssian_step(x, area, center, sigma, peak_e):
    """
    Gauss step function is an important component in modeling compton peak.
    Use scipy erfc function. Please note erfc = 1-erf.

    Parameters
    ----------
    x : array
        data in x coordinate
    area : float
        area of gauss step function
    center : float
        center position
    sigma : float
        standard deviation
    peak_e : float
        emission energy

    Returns
    -------
    counts : array
        gaussian step peak

    References
    ----------
    .. [1] Rene Van Grieken, "Handbook of X-Ray Spectrometry, Second Edition,
           (Practical Spectroscopy)", CRC Press, 2 edition, pp. 182, 2007.
    """
    return area * scipy.special.erfc((x - center) / (np.sqrt(2) * sigma)) / (2.0 * peak_e)


def gaussian_tail(x, area, center, sigma, gamma):
    """
    Use a gaussian tail function to simulate compton peak
    
    Parameters
    ----------
    x : array
        data in x coordinate
    area : float
        area of gauss tail function
        If area is set as 1, the integral is unity.
    center : float
        center position
    sigma : float
        control peak width
    gamma : float
        normalization factor
    
    Returns
    -------
    counts : array
        gaussian tail peak

    References
    ----------
    .. [1] Rene Van Grieken, "Handbook of X-Ray Spectrometry, Second Edition,
           (Practical Spectroscopy)", CRC Press, 2 edition, pp. 182, 2007.
    """
    dx_neg = np.array(x) - center
    dx_neg[dx_neg > 0] = 0
    temp_a = np.exp(dx_neg / (gamma * sigma))
    counts = area / (2 * gamma * sigma * np.exp(-0.5 / gamma ** 2)) * temp_a * scipy.special.erfc((x - center) / (np.sqrt(2) * sigma) + 1 / (gamma * np.sqrt(2)))
    return counts


def elastic(x, coherent_sct_amplitude, coherent_sct_energy, fwhm_offset, fwhm_fanoprime, e_offset, e_linear, e_quadratic, epsilon=2.96):
    """
    Use gaussian function to model elastic peak
    
    Parameters
    ----------
    x : array
        energy value
    coherent_sct_amplitude : float
        area of elastic peak
    coherent_sct_energy : float
        incident energy
    fwhm_offset : float
        global fitting parameter for peak width
    fwhm_fanoprime : float
        global fitting parameter for peak width
    e_offset : float
        offset of energy calibration
    e_linear : float
        linear coefficient in energy calibration
    e_quadratic : float
        quadratic coefficient in energy calibration
    epsilon : float
        energy to create a hole-electron pair
        for Ge 2.96, for Si 3.61 at 300K
        needs to double check this value
    
    Returns
    -------
    value : array
        elastic peak
    """
    x = e_offset + x * e_linear + x ** 2 * e_quadratic
    temp_val = 2 * np.sqrt(2 * np.log(2))
    sigma = np.sqrt((fwhm_offset / temp_val) ** 2 + coherent_sct_energy * epsilon * fwhm_fanoprime)
    return gaussian(x, coherent_sct_amplitude, coherent_sct_energy, sigma)


def compton(x, compton_amplitude, coherent_sct_energy, fwhm_offset, fwhm_fanoprime, e_offset, e_linear, e_quadratic, compton_angle, compton_fwhm_corr, compton_f_step, compton_f_tail, compton_gamma, compton_hi_f_tail, compton_hi_gamma, epsilon=2.96):
    """
    Model compton peak, which is generated as an inelastic peak and always
    stays to the left of elastic peak on the spectrum.
    
    Parameters
    ----------
    x : array
        energy value
    compton_amplitude : float
        area for gaussian peak, gaussian step and gaussian tail functions
    coherent_sct_energy : float
        incident energy                         
    fwhm_offset : float
        global fitting parameter for peak width
    fwhm_fanoprime : float
        global fitting parameter for peak width
    e_offset : float
        offset of energy calibration
    e_linear : float
        linear coefficient in energy calibration
    e_quadratic : float
        quadratic coefficient in energy calibration
    compton_angle : float
        compton angle in degree
    compton_fwhm_corr : float 
        correction factor on peak width
    compton_f_step : float
        weight factor of the gaussian step function
    compton_f_tail : float
        weight factor of gaussian tail on lower side
    compton_gamma : float
        normalization factor of gaussian tail on lower side
    compton_hi_f_tail : float
        weight factor of gaussian tail on higher side
    compton_hi_gamma : float
        normalization factor of gaussian tail on higher side
    epsilon : float
        energy to create a hole-electron pair
        for Ge 2.96, for Si 3.61 at 300K
        needs to double check this value
    
    Returns
    -------
    counts : array
        compton peak

     References
    -----------
    .. [1] M. Van Gysel etc, "Description of Compton peaks in
           energy-dispersive x-ray fluorescence spectra",
           X-Ray Spectrometry, vol. 32, pp. 139-147, 2003.
    """
    x = e_offset + x * e_linear + x ** 2 * e_quadratic
    mc2 = 511
    comp_denom = 1 + coherent_sct_energy / mc2 * (1 - np.cos(np.deg2rad(compton_angle)))
    compton_e = coherent_sct_energy / comp_denom
    temp_val = 2 * np.sqrt(2 * np.log(2))
    sigma = np.sqrt((fwhm_offset / temp_val) ** 2 + compton_e * epsilon * fwhm_fanoprime)
    counts = np.zeros_like(x)
    factor = 1 / (1 + compton_f_step + compton_f_tail + compton_hi_f_tail)
    value = factor * gaussian(x, compton_amplitude, compton_e, sigma * compton_fwhm_corr)
    counts += value
    if compton_f_step > 0.0:
        value = factor * compton_f_step
        value *= gausssian_step(x, compton_amplitude, compton_e, sigma, compton_e)
        counts += value
    value = factor * compton_f_tail
    value *= gaussian_tail(x, compton_amplitude, compton_e, sigma, compton_gamma)
    counts += value
    value = factor * compton_hi_f_tail
    value *= gaussian_tail(-1 * x, compton_amplitude, -1 * compton_e, sigma, compton_hi_gamma)
    counts += value
    return counts