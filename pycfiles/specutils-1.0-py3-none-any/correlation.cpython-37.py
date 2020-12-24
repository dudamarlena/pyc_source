# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/nearl/projects/specutils/build/lib/specutils/analysis/correlation.py
# Compiled at: 2020-03-19 14:18:03
# Size of source mod 2**32: 10153 bytes
import astropy.units as u
import numpy as np
from astropy import constants as const
from astropy.units import Quantity
from scipy.signal.windows import tukey
from ..manipulation import LinearInterpolatedResampler
from .. import Spectrum1D
__all__ = [
 'template_correlate', 'template_logwl_resample']
_KMS = u.Unit('km/s')

def template_correlate(observed_spectrum, template_spectrum, lag_units=_KMS, apodization_window=0.5, resample=True):
    """
    Compute cross-correlation of the observed and template spectra.

    After re-sampling into log-wavelength, both observed and template
    spectra are apodized by a Tukey window in order to minimize edge
    and consequent non-periodicity effects and thus decrease
    high-frequency power in the correlation function. To turn off the
    apodization, use alpha=0.

    Parameters
    ----------
    observed_spectrum : :class:`~specutils.Spectrum1D`
        The observed spectrum.
    template_spectrum : :class:`~specutils.Spectrum1D`
        The template spectrum, which will be correlated with
        the observed spectrum.
    lag_units: `~astropy.units.Unit`
        Must be a unit with velocity physical type for lags in velocity. To
        output the lags in redshift, use ``u.dimensionless_unscaled``.
    apodization_window: float, callable, or None
        If a callable, will be treated as a window function for apodization of
        the cross-correlation (should behave like a `~scipy.signal.windows`
        window function, with ``sym=True``). If a float, will be treated as the
        ``alpha`` parameter for a Tukey window (`~scipy.signal.windows.tukey`),
        in units of pixels. If None, no apodization will be performed
    resample: bool or dict
        If True or a dictionary, resamples the spectrum and template following
        the process in `template_logwl_resample`. If a dictionary, it will be
        used as the keywords for `template_logwl_resample`.  For example,
        ``resample=dict(delta_log_wavelength=.1)`` would be the same as calling
        ``template_logwl_resample(spectrum, template, delta_log_wavelength=.1)``.
        If False, *no* resampling is performed (and the user is responsible for
        a sensible resampling).

    Returns
    -------
    (`~astropy.units.Quantity`, `~astropy.units.Quantity`)
        Arrays with correlation values and lags in km/s
    """
    if resample:
        if resample is True:
            resample_kwargs = dict()
        else:
            resample_kwargs = resample
        log_spectrum, log_template = template_logwl_resample(observed_spectrum, 
         template_spectrum, **resample_kwargs)
    else:
        log_spectrum = observed_spectrum
        log_template = template_spectrum
    observed_log_spectrum, template_log_spectrum = _apodize(log_spectrum, log_template, apodization_window)
    normalization = _normalize(observed_log_spectrum, template_log_spectrum)
    if normalization < 0.0:
        normalization = 1.0
    else:
        corr = np.correlate((observed_log_spectrum.flux.value), (template_log_spectrum.flux.value * normalization),
          mode='full')
        wave_l = observed_log_spectrum.spectral_axis.value
        delta_log_wave = np.log10(wave_l[1]) - np.log10(wave_l[0])
        deltas = (np.array(range(len(corr))) - len(corr) / 2 + 0.5) * delta_log_wave
        lags = np.power(10.0, deltas) - 1.0
        if u.dimensionless_unscaled.is_equivalent(lag_units):
            lags = Quantity(lags, u.dimensionless_unscaled)
        else:
            if _KMS.is_equivalent(lag_units):
                lags = lags * const.c.to(lag_units)
            else:
                raise u.UnitsError('lag_units must be either velocity or dimensionless')
    return (
     corr * u.dimensionless_unscaled, lags)


def _apodize(spectrum, template, apodization_window):
    if apodization_window is None:
        clean_spectrum = spectrum
        clean_template = template
    else:
        if callable(apodization_window):
            window = apodization_window
        else:

            def window(wlen):
                return tukey(wlen, alpha=apodization_window)

        clean_spectrum = spectrum * window(len(spectrum.wavelength))
        clean_template = template * window(len(template.wavelength))
    return (clean_spectrum, clean_template)


def template_logwl_resample(spectrum, template, wblue=None, wred=None, delta_log_wavelength=None, resampler=LinearInterpolatedResampler()):
    """
    Resample a spectrum and template onto a common log-spaced spectral grid.

    If wavelength limits are not provided, the function will use
    the limits of the merged (observed+template) wavelength scale
    for building the log-wavelength scale.

    For the wavelength step, the function uses either the smallest wavelength
    interval found in the *observed* spectrum, or takes it from the
    ``delta_log_wavelength`` parameter.

    Parameters
    ----------
    observed_spectrum : :class:`~specutils.Spectrum1D`
        The observed spectrum.
    template_spectrum : :class:`~specutils.Spectrum1D`
        The template spectrum.
    wblue, wred: float
        Wavelength limits to include in the correlation.
    delta_log_wavelength: float
        Log-wavelength step to use to build the log-wavelength
        scale. If None, use limits defined as explained above.
    resampler
        A specutils resampler to use to actually do the resampling.  Defaults to
        using a `~specutils.manipulation.LinearInterpolatedResampler`.

    Returns
    -------
    resampled_observed : :class:`~specutils.Spectrum1D`
        The observed spectrum resampled to a common spectral_axis.
    resampled_template: :class:`~specutils.Spectrum1D`
        The template spectrum resampled to a common spectral_axis.
    """
    if wblue:
        w0 = np.log10(wblue)
    else:
        ws0 = np.log10(spectrum.spectral_axis[0].value)
        wt0 = np.log10(template.spectral_axis[0].value)
        w0 = min(ws0, wt0)
    if wred:
        w1 = np.log10(wred)
    else:
        ws1 = np.log10(spectrum.spectral_axis[(-1)].value)
        wt1 = np.log10(template.spectral_axis[(-1)].value)
        w1 = max(ws1, wt1)
    if delta_log_wavelength is None:
        ds = np.log10(spectrum.spectral_axis.value[1:]) - np.log10(spectrum.spectral_axis.value[:-1])
        dw = ds[np.argmin(ds)]
    else:
        dw = delta_log_wavelength
    nsamples = int((w1 - w0) / dw)
    log_wave_array = np.ones(nsamples) * w0
    for i in range(nsamples):
        log_wave_array[i] += dw * i

    wave_array = np.power(10.0, log_wave_array) * spectrum.spectral_axis.unit
    resampled_spectrum = resampler(spectrum, wave_array)
    resampled_template = resampler(template, wave_array)
    clean_spectrum_flux = np.nan_to_num(resampled_spectrum.flux.value) * resampled_spectrum.flux.unit
    clean_template_flux = np.nan_to_num(resampled_template.flux.value) * resampled_template.flux.unit
    clean_spectrum = Spectrum1D(spectral_axis=(resampled_spectrum.spectral_axis), flux=clean_spectrum_flux,
      uncertainty=(resampled_spectrum.uncertainty),
      velocity_convention='optical',
      rest_value=(spectrum.rest_value))
    clean_template = Spectrum1D(spectral_axis=(resampled_template.spectral_axis), flux=clean_template_flux,
      uncertainty=(resampled_template.uncertainty),
      velocity_convention='optical',
      rest_value=(template.rest_value))
    return (
     clean_spectrum, clean_template)


def _normalize(observed_spectrum, template_spectrum):
    """
    Calculate a scale factor to be applied to the template spectrum so the
    total flux in both spectra will be the same.

    Parameters
    ----------
    observed_spectrum : :class:`~specutils.Spectrum1D`
        The observed spectrum.
    template_spectrum : :class:`~specutils.Spectrum1D`
        The template spectrum, which needs to be normalized in order to be
        compared with the observed spectrum.

    Returns
    -------
    `float`
        A float which will normalize the template spectrum's flux so that it
        can be compared to the observed spectrum.
    """
    num = np.nansum(observed_spectrum.flux * template_spectrum.flux / observed_spectrum.uncertainty.array ** 2)
    denom = np.nansum((template_spectrum.flux / observed_spectrum.uncertainty.array) ** 2)
    return num / denom