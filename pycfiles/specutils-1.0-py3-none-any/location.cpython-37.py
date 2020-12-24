# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/nearl/projects/specutils/build/lib/specutils/analysis/location.py
# Compiled at: 2020-03-19 14:18:03
# Size of source mod 2**32: 2568 bytes
"""
A module for analysis tools focused on determining the location of
spectral features.
"""
import numpy as np
from ..spectra import SpectralRegion
from ..manipulation import extract_region
__all__ = [
 'centroid']

def centroid(spectrum, region):
    """
    Calculate the centroid of a region, or regions, of the spectrum.

    Parameters
    ----------
    spectrum : `~specutils.spectra.spectrum1d.Spectrum1D`
        The spectrum object overwhich the centroid will be calculated.

    region: `~specutils.utils.SpectralRegion` or list of `~specutils.utils.SpectralRegion`
        Region within the spectrum to calculate the centroid.

    Returns
    -------
    centroid : float or list (based on region input)
        Centroid of the spectrum or within the regions

    Notes
    -----
    The spectrum will need to be continuum subtracted before calling
    this method. See the
    `analysis documentation <https://specutils.readthedocs.io/en/latest/basic_analysis.html>`_ for more information.

    """
    if region is None:
        return _centroid_single_region(spectrum)
    if isinstance(region, SpectralRegion):
        return _centroid_single_region(spectrum, region=region)
    if isinstance(region, list):
        return [_centroid_single_region(spectrum, region=reg) for reg in region]


def _centroid_single_region(spectrum, region=None):
    """
    Calculate the centroid of the spectrum based on the flux and uncertainty
    in the spectrum.

    Parameters
    ----------
    spectrum : `~specutils.spectra.spectrum1d.Spectrum1D`
        The spectrum object overwhich the centroid will be calculated.

    region: `~specutils.utils.SpectralRegion`
        Region within the spectrum to calculate the centroid.

    Returns
    -------
    centroid : float or list (based on region input)
        Centroid of the spectrum or within the regions

    Notes
    -----
    This is a helper function for the above `centroid()` method.

    """
    if region is not None:
        calc_spectrum = extract_region(spectrum, region)
    else:
        calc_spectrum = spectrum
    flux = calc_spectrum.flux
    dispersion = calc_spectrum.spectral_axis.quantity
    if len(flux.shape) > 1:
        dispersion = np.tile(dispersion, [flux.shape[0], 1])
    return np.sum((flux * dispersion), axis=(-1)) / np.sum(flux, axis=(-1))