# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/nearl/projects/specutils/build/lib/specutils/analysis/uncertainty.py
# Compiled at: 2020-01-06 12:55:36
# Size of source mod 2**32: 5542 bytes
"""
A module for analysis tools dealing with uncertainties or error analysis in
spectra.
"""
import numpy as np
from ..spectra import SpectralRegion
from ..manipulation import extract_region
__all__ = [
 'snr', 'snr_derived']

def snr(spectrum, region=None):
    """
    Calculate the mean S/N of the spectrum based on the flux and uncertainty
    in the spectrum. This will be calculated over the regions, if they
    are specified.

    Parameters
    ----------
    spectrum : `~specutils.spectra.spectrum1d.Spectrum1D`
        The spectrum object overwhich the equivalent width will be calculated.

    region: `~specutils.utils.SpectralRegion` or list of `~specutils.utils.SpectralRegion`
        Region within the spectrum to calculate the SNR.

    Returns
    -------
    snr : `~astropy.units.Quantity` or list (based on region input)
        Signal to noise ratio of the spectrum or within the regions

    Notes
    -----
    The spectrum will need to have the uncertainty defined in order for the SNR
    to be calculated. If the goal is instead signal to noise *per pixel*, this
    should be computed directly as ``spectrum.flux / spectrum.uncertainty``.

    """
    if not hasattr(spectrum, 'uncertainty') or spectrum.uncertainty is None:
        raise Exception('Spectrum1D currently requires the uncertainty be defined.')
    if region is None:
        return _snr_single_region(spectrum)
    if isinstance(region, SpectralRegion):
        return _snr_single_region(spectrum, region=region)
    if isinstance(region, list):
        return [_snr_single_region(spectrum, region=reg) for reg in region]


def _snr_single_region(spectrum, region=None):
    """
    Calculate the mean S/N of the spectrum based on the flux and uncertainty
    in the spectrum.

    Parameters
    ----------
    spectrum : `~specutils.spectra.spectrum1d.Spectrum1D`
        The spectrum object overwhich the equivalent width will be calculated.

    region: `~specutils.utils.SpectralRegion`
        Region within the spectrum to calculate the SNR.

    Returns
    -------
    snr : `~astropy.units.Quantity` or list (based on region input)
        Signal to noise ratio of the spectrum or within the regions

    Notes
    -----
    This is a helper function for the above `snr()` method.

    """
    if region is not None:
        calc_spectrum = extract_region(spectrum, region)
    else:
        calc_spectrum = spectrum
    flux = calc_spectrum.flux
    uncertainty = calc_spectrum.uncertainty.array * spectrum.uncertainty.unit
    return np.mean((flux / uncertainty), axis=(-1))


def snr_derived(spectrum, region=None):
    """
    This function computes the signal to noise ratio DER_SNR following the
    definition set forth by the Spectral Container Working Group of ST-ECF,
    MAST and CADC.

    Parameters
    ----------
    spectrum : `~specutils.spectra.spectrum1d.Spectrum1D`
        The spectrum object overwhich the equivalent width will be calculated.

    region: `~specutils.utils.SpectralRegion`
        Region within the spectrum to calculate the SNR.

    Returns
    -------
    snr : `~astropy.units.Quantity` or list (based on region input)
        Signal to noise ratio of the spectrum or within the regions

    Notes
    -----
    The DER_SNR algorithm is an unbiased estimator describing the spectrum
    as a whole as long as the noise is uncorrelated in wavelength bins spaced
    two pixels apart, the noise is Normal distributed, for large wavelength
    regions, the signal over the scale of 5 or more pixels can be approximated
    by a straight line.

    Code and some docs copied from
    ``http://www.stecf.org/software/ASTROsoft/DER_SNR/der_snr.py``
    """
    if region is None:
        return _snr_derived(spectrum)
    if isinstance(region, SpectralRegion):
        return _snr_derived(spectrum, region=region)
    if isinstance(region, list):
        return [_snr_derived(spectrum, region=reg) for reg in region]


def _snr_derived(spectrum, region=None):
    """
    This function computes the signal to noise ratio DER_SNR following the
    definition set forth by the Spectral Container Working Group of ST-ECF,
    MAST and CADC

    Parameters
    ----------
    spectrum : `~specutils.spectra.spectrum1d.Spectrum1D`
        The spectrum object overwhich the equivalent width will be calculated.

    region: `~specutils.utils.SpectralRegion`
        Region within the spectrum to calculate the SNR.

    Returns
    -------
    snr : `~astropy.units.Quantity` or list (based on region input)
        Signal to noise ratio of the spectrum or within the regions

    Notes
    -----
    This is a helper function for the above `snr_derived()` method.

    """
    if region is not None:
        calc_spectrum = extract_region(spectrum, region)
    else:
        calc_spectrum = spectrum
    flux = calc_spectrum.flux
    n = len(flux)
    if n > 4:
        signal = np.median(flux)
        noise = 0.6052697 * np.median(np.abs(2.0 * flux[2:n - 2] - flux[0:n - 4] - flux[4:n]))
        return signal / noise
    return 0.0