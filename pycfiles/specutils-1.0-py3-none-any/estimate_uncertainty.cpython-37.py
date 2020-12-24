# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/nearl/projects/specutils/build/lib/specutils/manipulation/estimate_uncertainty.py
# Compiled at: 2020-01-06 12:55:36
# Size of source mod 2**32: 2593 bytes
import numpy as np
from astropy import units as u
from .. import Spectrum1D, SpectralRegion
from astropy.nddata.nduncertainty import StdDevUncertainty, VarianceUncertainty, InverseVariance
from .extract_spectral_region import extract_region
__all__ = [
 'noise_region_uncertainty']

def noise_region_uncertainty(spectrum, spectral_region, noise_func=np.std):
    """
    Generates a new spectrum with an uncertainty from the noise in a particular
    region of the spectrum.

    Parameters
    ----------

    spectrum : `~specutils.Spectrum1D`
        The spectrum to which we want to set the uncertainty.

    spectral_region : `~specutils.SpectralRegion`
        The region to use to calculate the standard deviation.

    noise_func : callable
        A function which takes the (1D) flux in the ``spectral_region`` and
        yields a *single* value for the noise to use in the result spectrum.

    Returns
    -------
    spectrum_uncertainty : `~specutils.Spectrum1D`
        The ``spectrum``, but with a constant uncertainty set by the result of
        the noise region calculation
    """
    sub_spectra = extract_region(spectrum, spectral_region)
    if not isinstance(sub_spectra, list):
        sub_spectra = [
         sub_spectra]
    else:
        sub_flux = u.Quantity(np.concatenate([s.flux.value for s in sub_spectra]), spectrum.flux.unit)
        noise = noise_func(sub_flux)
        if noise.unit == spectrum.flux.unit:
            uncertainty = StdDevUncertainty(noise * np.ones(spectrum.flux.shape))
        else:
            if noise.unit == spectrum.flux.unit ** 2:
                uncertainty = VarianceUncertainty(noise * np.ones(spectrum.flux.shape))
            else:
                if noise.unit == 1 / spectrum.flux.unit ** 2:
                    uncertainty = InverseVariance(noise * np.ones(spectrum.flux.shape))
                else:
                    raise ValueError('Can not determine correct NDData Uncertainty based on units {} relative to the flux units {}'.format(noise.unit, spectrum.flux.unit))
    return Spectrum1D(flux=(spectrum.flux), spectral_axis=(spectrum.spectral_axis), uncertainty=uncertainty,
      wcs=(spectrum.wcs),
      velocity_convention=(spectrum.velocity_convention),
      rest_value=(spectrum.rest_value))