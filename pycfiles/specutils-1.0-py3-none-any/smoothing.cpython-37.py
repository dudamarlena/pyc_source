# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/nearl/projects/specutils/build/lib/specutils/manipulation/smoothing.py
# Compiled at: 2020-01-06 12:55:36
# Size of source mod 2**32: 8544 bytes
import copy, warnings
from astropy import convolution
from astropy.nddata import StdDevUncertainty, VarianceUncertainty, InverseVariance
import astropy.units as u
from astropy.utils.exceptions import AstropyUserWarning
from scipy.signal import medfilt
import numpy as np
from ..spectra import Spectrum1D
__all__ = [
 'convolution_smooth', 'box_smooth', 'gaussian_smooth',
 'trapezoid_smooth', 'median_smooth']

def convolution_smooth(spectrum, kernel):
    """
    Apply a convolution based smoothing to the spectrum. The kernel must be one
    of the 1D kernels defined in `astropy.convolution`.

    This method can be used along but also is used by other specific methods below.

    If the spectrum uncertainty exists and is StdDevUncertainty, VarianceUncertainty or InverseVariance
    then the errors will be propagated through the convolution using a standard propagation of errors. The
    covariance is not considered, currently.

    Parameters
    ----------
    spectrum : `~specutils.Spectrum1D`
        The `~specutils.Spectrum1D` object to which the smoothing will be applied.
    kernel : `astropy.convolution.Kernel1D` subclass or array.
        The convolution based smoothing kernel - anything that `astropy.convolution.convolve` accepts.

    Returns
    -------
    spectrum : `~specutils.Spectrum1D`
        Output `~specutils.Spectrum1D` which is copy of the one passed in with the updated flux.

    Raises
    ------
    ValueError
       In the case that ``spectrum`` and ``kernel`` are not the correct types.

    """
    if not isinstance(spectrum, Spectrum1D):
        raise ValueError('The spectrum parameter must be a Spectrum1D object')
    else:
        flux = spectrum.flux
        smoothed_flux = convolution.convolve(flux, kernel)
        uncertainty = copy.deepcopy(spectrum.uncertainty)
        if uncertainty is not None:
            if isinstance(uncertainty, StdDevUncertainty):
                values = uncertainty.array
                ivar_values = 1 / values ** 2
                prop_ivar_values = convolution.convolve(ivar_values, kernel)
                uncertainty.array = 1 / np.sqrt(prop_ivar_values)
            else:
                if isinstance(uncertainty, VarianceUncertainty):
                    values = uncertainty.array
                    ivar_values = 1 / values
                    prop_ivar_values = convolution.convolve(ivar_values, kernel)
                    uncertainty.array = 1 / prop_ivar_values
                else:
                    if isinstance(uncertainty, InverseVariance):
                        ivar_values = uncertainty.array
                        prop_ivar_values = convolution.convolve(ivar_values, kernel)
                        uncertainty.array = prop_ivar_values
                    else:
                        uncertainty = None
                        warnings.warn('Uncertainty is {} but convolutional error propagation is not defined for that type. Uncertainty will be dropped in the convolved spectrum.'.format(type(uncertainty)), AstropyUserWarning)
    return Spectrum1D(flux=(u.Quantity(smoothed_flux, spectrum.unit)), spectral_axis=(u.Quantity(spectrum.spectral_axis, spectrum.spectral_axis_unit)),
      wcs=(spectrum.wcs),
      uncertainty=uncertainty,
      velocity_convention=(spectrum.velocity_convention),
      rest_value=(spectrum.rest_value))


def box_smooth(spectrum, width):
    """
    Smooth a `~specutils.Spectrum1D` instance based on a `astropy.convolution.Box1DKernel` kernel.

    Parameters
    ----------
    spectrum : `~specutils.Spectrum1D`
        The spectrum object to which the smoothing will be applied.
    width : number
        The width of the kernel, in pixels, as defined in `astropy.convolution.Box1DKernel`

    Returns
    -------
    spectrum : `~specutils.Spectrum1D`
        Output `~specutils.Spectrum1D` which a copy of the one passed in with the updated flux.

    Raises
    ------
    ValueError
       In the case that ``width`` is not the correct type or value.

    """
    if not isinstance(width, (int, float)) or width <= 0:
        raise ValueError('The width parameter, {}, must be a number greater than 0'.format(width))
    box1d_kernel = convolution.Box1DKernel(width)
    return convolution_smooth(spectrum, box1d_kernel)


def gaussian_smooth(spectrum, stddev):
    """
    Smooth a `~specutils.Spectrum1D` instance based on a `astropy.convolution.Gaussian1DKernel`.

    Parameters
    ----------
    spectrum : `~specutils.Spectrum1D`
        The spectrum object to which the smoothing will be applied.
    stddev : number
        The stddev of the kernel, in pixels, as defined in `astropy.convolution.Gaussian1DKernel`

    Returns
    -------
    spectrum : `~specutils.Spectrum1D`
        Output `~specutils.Spectrum1D` which is copy of the one passed in with the updated flux.

    Raises
    ------
    ValueError
       In the case that ``stddev`` is not the correct type or value.

    """
    if not isinstance(stddev, (int, float)) or stddev <= 0:
        raise ValueError('The stddev parameter, {}, must be a number greater than 0'.format(stddev))
    gaussian_kernel = convolution.Gaussian1DKernel(stddev)
    return convolution_smooth(spectrum, gaussian_kernel)


def trapezoid_smooth(spectrum, width):
    """
    Smoothing based on a `astropy.convolution.Trapezoid1DKernel` kernel.

    Parameters
    ----------
    spectrum : `~specutils.Spectrum1D`
        The `~specutils.Spectrum1D` object to which the smoothing will be applied.
    width : number
        The width of the kernel, in pixels, as defined in `astropy.convolution.Trapezoid1DKernel`

    Returns
    -------
    spectrum : `~specutils.Spectrum1D`
        Output `~specutils.Spectrum1D` which is copy of the one passed in with the updated flux.

    Raises
    ------
    ValueError
       In the case that ``width`` is not the correct type or value.

    """
    if not isinstance(width, (int, float)) or width <= 0:
        raise ValueError('The stddev parameter, {}, must be a number greater than 0'.format(width))
    trapezoid_kernel = convolution.Trapezoid1DKernel(width)
    return convolution_smooth(spectrum, trapezoid_kernel)


def median_smooth(spectrum, width):
    """
    Smoothing based on a median filter. The median filter smoothing
    is implemented using the `scipy.signal.medfilt` function.

    Parameters
    ----------
    spectrum : `~specutils.Spectrum1D`
        The `~specutils.Spectrum1D` object to which the smoothing will be applied.
    width : number
        The width of the median filter in pixels.

    Returns
    -------
    spectrum : `~specutils.Spectrum1D`
        Output `~specutils.Spectrum1D` which is copy of the one passed in with the updated flux.

    Raises
    ------
    ValueError
       In the case that ``spectrum`` or ``width`` are not the correct type or value.

    """
    if not isinstance(spectrum, Spectrum1D):
        raise ValueError('The spectrum parameter must be a Spectrum1D object')
    if not isinstance(width, (int, float)) or width <= 0:
        raise ValueError('The stddev parameter, {}, must be a number greater than 0'.format(width))
    flux = spectrum.flux
    smoothed_flux = medfilt(flux, width)
    return Spectrum1D(flux=(u.Quantity(smoothed_flux, spectrum.unit)), spectral_axis=(u.Quantity(spectrum.spectral_axis, spectrum.spectral_axis_unit)),
      wcs=(spectrum.wcs),
      velocity_convention=(spectrum.velocity_convention),
      rest_value=(spectrum.rest_value))