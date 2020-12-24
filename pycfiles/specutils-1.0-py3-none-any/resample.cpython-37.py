# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/nearl/projects/specutils/build/lib/specutils/manipulation/resample.py
# Compiled at: 2020-03-19 14:18:03
# Size of source mod 2**32: 15797 bytes
import logging
from abc import ABC, abstractmethod
from warnings import warn
import numpy as np
from astropy.nddata import StdDevUncertainty, VarianceUncertainty, InverseVariance
from astropy.units import Quantity
from scipy.interpolate import CubicSpline
from ..spectra import Spectrum1D
__all__ = [
 'ResamplerBase', 'FluxConservingResampler',
 'LinearInterpolatedResampler', 'SplineInterpolatedResampler']

class ResamplerBase(ABC):
    __doc__ = "\n    Base class for resample classes.  The algorithms and needs for difference\n    resamples will vary quite a bit, so this class is relatively sparse.\n\n    Parameters\n    ----------\n    extrapolation_treatment : str\n        What to do when resampling off the edge of the spectrum.  Can be\n        ``'nan_fill'`` to have points beyond the edges by set to NaN, or\n        ``'zero_fill'`` to be set to zero.\n    "

    def __init__(self, extrapolation_treatment='nan_fill'):
        if extrapolation_treatment not in ('nan_fill', 'zero_fill'):
            raise ValueError('invalid extrapolation_treatment value: ' + str(extrapolation_treatment))
        self.extrapolation_treatment = extrapolation_treatment

    def __call__(self, orig_spectrum, fin_spec_axis):
        """
        Return the resulting `~specutils.Spectrum1D` of the resampling.
        """
        return self.resample1d(orig_spectrum, fin_spec_axis)

    @abstractmethod
    def resample1d(self, orig_spectrum, fin_spec_axis):
        """
        Workhorse method that will return the resampled Spectrum1D
        object.
        """
        return NotImplemented

    @staticmethod
    def _calc_bin_edges(x):
        """
        Calculate the bin edge values of an input spectral axis. Input values
        are assumed to be the center of the bins.

        todo: this should live in the main spectrum object, but we're still
        figuring out the details to that implementation, so leaving here
        for now.

        Parameters
        ----------
        x : ndarray
            The input spectral axis values.

        Returns
        -------
        edges : ndarray
            Calcualated bin edges, including left and right most bin edges.
        """
        inside_edges = (x[1:] + x[:-1]) / 2
        edges = np.insert(inside_edges, 0, 2 * x[0] - inside_edges[0])
        edges = np.append(edges, 2 * x[(-1)] - inside_edges[(-1)])
        return edges


class FluxConservingResampler(ResamplerBase):
    __doc__ = "\n    This resampling algorithm conserves overall integrated flux (as opposed to\n    flux density).\n    Algorithm based on the equations documented in the following paper:\n    https://ui.adsabs.harvard.edu/abs/2017arXiv170505165C/abstract\n\n    Parameters\n    ----------\n    extrapolation_treatment : str\n        What to do when resampling off the edge of the spectrum.  Can be\n        ``'nan_fill'`` to have points beyond the edges by set to NaN, or\n        ``'zero_fill'`` to be set to zero.\n\n    Examples\n    --------\n\n    To resample an input spectrum to a user specified spectral grid using\n    a flux conserving algorithm:\n\n    >>> import numpy as np\n    >>> import astropy.units as u\n    >>> from specutils import Spectrum1D\n    >>> from specutils.manipulation import FluxConservingResampler\n    >>> input_spectra = Spectrum1D(\n    ...     flux=np.array([1, 3, 7, 6, 20]) * u.mJy,\n    ...     spectral_axis=np.array([2, 4, 12, 16, 20]) * u.nm)\n    >>> resample_grid = [1, 5, 9, 13, 14, 17, 21, 22, 23]  *u.nm\n    >>> fluxc_resample = FluxConservingResampler()\n    >>> output_spectrum1D = fluxc_resample(input_spectra, resample_grid) # doctest: +IGNORE_OUTPUT\n\n    "

    def _resample_matrix(self, orig_spec_axis, fin_spec_axis):
        """
        Create a re-sampling matrix to be used in re-sampling spectra in a way
        that conserves flux. This code was heavily influenced by Nick Earl's
        resample rough draft: nmearl@0ff6ef1.

        Parameters
        ----------
        orig_spec_axis : ndarray
            The original spectral axis array.
        fin_spec_axis : ndarray
            The desired spectral axis array.

        Returns
        -------
        resample_mat : ndarray
            An [[N_{fin_spec_axis}, M_{orig_spec_axis}]] matrix.
        """
        orig_edges = self._calc_bin_edges(orig_spec_axis)
        fin_edges = self._calc_bin_edges(fin_spec_axis)
        orig_low = orig_edges[:-1]
        fin_low = fin_edges[:-1]
        orig_upp = orig_edges[1:]
        fin_upp = fin_edges[1:]
        l_inf = np.where(orig_low > fin_low[:, np.newaxis], orig_low, fin_low[:, np.newaxis])
        l_sup = np.where(orig_upp < fin_upp[:, np.newaxis], orig_upp, fin_upp[:, np.newaxis])
        resamp_mat = (l_sup - l_inf).clip(0)
        resamp_mat *= orig_upp - orig_low
        left_clip = np.where(fin_edges[:-1] - orig_edges[0] < 0, 0, 1)
        right_clip = np.where(orig_edges[(-1)] - fin_edges[1:] < 0, 0, 1)
        keep_overlapping_matrix = left_clip * right_clip
        resamp_mat *= keep_overlapping_matrix[:, np.newaxis]
        return resamp_mat

    def resample1d(self, orig_spectrum, fin_spec_axis):
        """
        Create a re-sampling matrix to be used in re-sampling spectra in a way
        that conserves flux. If an uncertainty is present in the input spectra
        it will be propagated through to the final resampled output spectra
        as an InverseVariance uncertainty.

        Parameters
        ----------
        orig_spectrum : `~specutils.Spectrum1D`
            The original 1D spectrum.
        fin_spec_axis :  Quantity
            The desired spectral axis array.

        Returns
        -------
        resample_spectrum : `~specutils.Spectrum1D`
            An output spectrum containing the resampled `~specutils.Spectrum1D`
        """
        if isinstance(fin_spec_axis, Quantity):
            if orig_spectrum.spectral_axis.unit != fin_spec_axis.unit:
                raise ValueError('Original spectrum spectral axis grid and newspectral axis grid must have the same units.')
        elif orig_spectrum.uncertainty is not None:
            if isinstance(orig_spectrum.uncertainty, StdDevUncertainty):
                pixel_uncer = np.square(orig_spectrum.uncertainty.array)
            elif isinstance(orig_spectrum.uncertainty, VarianceUncertainty):
                pixel_uncer = orig_spectrum.uncertainty.array
            else:
                if isinstance(orig_spectrum.uncertainty, InverseVariance):
                    pixel_uncer = np.reciprocal(orig_spectrum.uncertainty.array)
                else:
                    pixel_uncer = None
                orig_axis_in_fin = orig_spectrum.spectral_axis.to(fin_spec_axis.unit)
                resample_grid = self._resample_matrix(orig_axis_in_fin.value, fin_spec_axis.value)
                new_flux_shape = list(orig_spectrum.flux.shape)
                new_flux_shape.insert(-1, 1)
                in_flux = orig_spectrum.flux.reshape(new_flux_shape)
                ones = [
                 1] * len(orig_spectrum.flux.shape[:-1])
                new_shape_resample_grid = ones + list(resample_grid.shape)
                resample_grid = resample_grid.reshape(new_shape_resample_grid)
                out_flux = np.sum((in_flux * resample_grid), axis=(-1)) / np.sum(resample_grid,
                  axis=(-1))
                if pixel_uncer is not None:
                    pixel_uncer = pixel_uncer.reshape(new_flux_shape)
                    out_variance = np.sum((pixel_uncer * resample_grid ** 2), axis=(-1)) / np.sum((resample_grid ** 2),
                      axis=(-1))
                    out_uncertainty = InverseVariance(np.reciprocal(out_variance))
        else:
            out_uncertainty = None
        if self.extrapolation_treatment == 'zero_fill':
            origedges = self._calc_bin_edges(orig_spectrum.spectral_axis.value) * orig_spectrum.spectral_axis.unit
            off_edges = (fin_spec_axis < origedges[0]) | (origedges[(-1)] < fin_spec_axis)
            out_flux[off_edges] = 0
            if out_uncertainty is not None:
                out_uncertainty.array[off_edges] = 0
        resampled_spectrum = Spectrum1D(flux=out_flux, spectral_axis=(np.array(fin_spec_axis) * orig_spectrum.spectral_axis_unit),
          uncertainty=out_uncertainty)
        return resampled_spectrum


class LinearInterpolatedResampler(ResamplerBase):
    __doc__ = "\n    Resample a spectrum onto a new ``spectral_axis`` using linear interpolation.\n\n    Parameters\n    ----------\n    extrapolation_treatment : str\n        What to do when resampling off the edge of the spectrum.  Can be\n        ``'nan_fill'`` to have points beyond the edges by set to NaN, or\n        ``'zero_fill'`` to be set to zero.\n\n    Examples\n    --------\n\n    To resample an input spectrum to a user specified dispersion grid using\n    linear interpolation:\n\n    >>> import numpy as np\n    >>> import astropy.units as u\n    >>> from specutils import Spectrum1D\n    >>> from specutils.manipulation import LinearInterpolatedResampler\n    >>> input_spectra = Spectrum1D(\n    ...     flux=np.array([1, 3, 7, 6, 20]) * u.mJy,\n    ...     spectral_axis=np.array([2, 4, 12, 16, 20]) * u.nm)\n    >>> resample_grid = [1, 5, 9, 13, 14, 17, 21, 22, 23] * u.nm\n    >>> fluxc_resample = LinearInterpolatedResampler()\n    >>> output_spectrum1D = fluxc_resample(input_spectra, resample_grid) # doctest: +IGNORE_OUTPUT\n    "

    def __init__(self, extrapolation_treatment='nan_fill'):
        super().__init__(extrapolation_treatment)

    def resample1d(self, orig_spectrum, fin_spec_axis):
        """
        Call interpolation, repackage new spectra

        Parameters
        ----------
        orig_spectrum : `~specutils.Spectrum1D`
            The original 1D spectrum.
        fin_spec_axis : ndarray
            The desired spectral axis array.

        Returns
        -------
        resample_spectrum : `~specutils.Spectrum1D`
            An output spectrum containing the resampled `~specutils.Spectrum1D`
        """
        fill_val = np.nan
        if self.extrapolation_treatment == 'zero_fill':
            fill_val = 0
        orig_axis_in_fin = orig_spectrum.spectral_axis.to(fin_spec_axis.unit)
        out_flux = np.interp(fin_spec_axis, orig_axis_in_fin, (orig_spectrum.flux),
          left=fill_val, right=fill_val)
        new_unc = None
        if orig_spectrum.uncertainty is not None:
            out_unc_arr = np.interp(fin_spec_axis, orig_axis_in_fin, (orig_spectrum.uncertainty.array),
              left=fill_val,
              right=fill_val)
            new_unc = orig_spectrum.uncertainty.__class__(array=out_unc_arr, unit=(orig_spectrum.unit))
        return Spectrum1D(spectral_axis=fin_spec_axis, flux=out_flux,
          uncertainty=new_unc)


class SplineInterpolatedResampler(ResamplerBase):
    __doc__ = "\n    This resample algorithim uses a cubic spline interpolator. Any uncertainty\n    is also interpolated using an identical spline.\n\n\n    Parameters\n    ----------\n    extrapolation_treatment : str\n        What to do when resampling off the edge of the spectrum.  Can be\n        ``'nan_fill'`` to have points beyond the edges by set to NaN, or\n        ``'zero_fill'`` to be set to zero.\n\n    Examples\n    --------\n\n    To resample an input spectrum to a user specified spectral axis grid using\n    a cubic spline interpolator:\n\n    >>> import numpy as np\n    >>> import astropy.units as u\n    >>> from specutils import Spectrum1D\n    >>> from specutils.manipulation import SplineInterpolatedResampler\n    >>> input_spectra = Spectrum1D(\n    ...     flux=np.array([1, 3, 7, 6, 20]) * u.mJy,\n    ...     spectral_axis=np.array([2, 4, 12, 16, 20]) * u.nm)\n    >>> resample_grid = [1, 5, 9, 13, 14, 17, 21, 22, 23] * u.nm\n    >>> fluxc_resample = SplineInterpolatedResampler()\n    >>> output_spectrum1D = fluxc_resample(input_spectra, resample_grid) # doctest: +IGNORE_OUTPUT\n\n    "

    def __init__(self, bin_edges='nan_fill'):
        super().__init__(bin_edges)

    def resample1d(self, orig_spectrum, fin_spec_axis):
        """
        Call interpolation, repackage new spectra

        Parameters
        ----------
        orig_spectrum : `~specutils.Spectrum1D`
            The original 1D spectrum.
        fin_spec_axis : Quantity
            The desired spectral axis array.

        Returns
        -------
        resample_spectrum : `~specutils.Spectrum1D`
            An output spectrum containing the resampled `~specutils.Spectrum1D`
        """
        orig_axis_in_new = orig_spectrum.spectral_axis.to(fin_spec_axis.unit)
        flux_spline = CubicSpline((orig_axis_in_new.value), (orig_spectrum.flux.value), extrapolate=(self.extrapolation_treatment != 'nan_fill'))
        out_flux_val = flux_spline(fin_spec_axis.value)
        new_unc = None
        if orig_spectrum.uncertainty is not None:
            unc_spline = CubicSpline((orig_axis_in_new.value), (orig_spectrum.uncertainty.array), extrapolate=(self.extrapolation_treatment != 'nan_fill'))
            out_unc_val = unc_spline(fin_spec_axis.value)
            new_unc = orig_spectrum.uncertainty.__class__(array=out_unc_val, unit=(orig_spectrum.unit))
        if self.extrapolation_treatment == 'zero_fill':
            origedges = self._calc_bin_edges(orig_spectrum.spectral_axis.value) * orig_spectrum.spectral_axis.unit
            off_edges = (fin_spec_axis < origedges[0]) | (origedges[(-1)] < fin_spec_axis)
            out_flux_val[off_edges] = 0
            if new_unc is not None:
                new_unc.array[off_edges] = 0
        return Spectrum1D(spectral_axis=fin_spec_axis, flux=(out_flux_val * orig_spectrum.flux.unit),
          uncertainty=new_unc)