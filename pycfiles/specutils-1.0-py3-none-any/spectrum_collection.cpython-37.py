# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/nearl/projects/specutils/build/lib/specutils/spectra/spectrum_collection.py
# Compiled at: 2020-03-17 18:47:05
# Size of source mod 2**32: 9471 bytes
import logging
import astropy.units as u
import numpy as np
from astropy.nddata import NDUncertainty, StdDevUncertainty
from .spectrum1d import Spectrum1D
__all__ = [
 'SpectrumCollection']

class SpectrumCollection:
    __doc__ = '\n    A class to represent a heterogeneous set of spectra that are the same length\n    but have different spectral axes. Spectra that meet this requirement can be\n    stored as multidimensional arrays, and thus can have operations performed\n    on them faster than if they are treated as individual\n    :class:`~specutils.Spectrum1D` objects.\n\n    The attributes on this class uses the same names and conventions as\n    :class:`~specutils.Spectrum1D`, allowing some operations to work the same.\n    Where this does not work, the user can use standard indexing notation to\n    access individual :class:`~specutils.Spectrum1D` objects.\n\n    Parameters\n    ----------\n    flux : :class:`astropy.units.Quantity`\n        The flux data. The trailing dimension should be the spectral dimension.\n    spectral_axis : :class:`astropy.units.Quantity`\n        The spectral axes of the spectra (e.g., wavelength).  Must match the\n        dimensionality of ``flux``.\n    wcs : wcs object or None\n        A wcs object (if available) for the collection of spectra.  The object\n        must follow standard indexing rules to get a sub-wcs if it is provided.\n    uncertainty : :class:`astropy.nddata.NDUncertainty` or ndarray\n        The uncertainties associated with each spectrum of the collection. In\n        the case that only an n-dimensional quantity or ndaray is provided,\n        the uncertainties are assumed to be standard deviations. Must match the\n        dimensionality of ``flux``.\n    mask : ndarray or None\n        The n-dimensional mask information associated with each spectrum. If\n        present, must match the dimensionality of ``flux``.\n    meta : list\n        The list of dictionaries containing meta data to be associated with\n        each spectrum in the collection.\n    '

    def __init__(self, flux, spectral_axis=None, wcs=None, uncertainty=None, mask=None, meta=None):
        if not isinstance(flux, u.Quantity):
            raise u.UnitsError('Flux must be a `Quantity`.')
        else:
            if spectral_axis is not None:
                if not isinstance(spectral_axis, u.Quantity):
                    raise u.UnitsError('Spectral axis must be a `Quantity`.')
                if not flux.shape == spectral_axis.shape:
                    raise ValueError('Shape of all data elements must be the same.')
            else:
                if uncertainty is not None:
                    if uncertainty.array.shape != flux.shape:
                        raise ValueError('Uncertainty must be the same shape as flux and spectral axis.')
                if mask is not None and mask.shape != flux.shape:
                    raise ValueError('Mask must be the same shape as flux and spectral axis.')
            if uncertainty is not None and not isinstance(uncertainty, NDUncertainty):
                if not isinstance(uncertainty, u.Quantity):
                    logging.warning("No unit associated with uncertainty, assumingflux units of '{}'.".format(flux.unit))
                    uncertainty = u.Quantity(uncertainty, unit=(flux.unit))
                uncertainty = StdDevUncertainty(uncertainty)
        self._flux = flux
        self._spectral_axis = spectral_axis
        self._wcs = wcs
        self._uncertainty = uncertainty
        self._mask = mask
        self._meta = meta

    def __getitem__(self, key):
        flux = self.flux[key]
        if flux.ndim != 1:
            raise ValueError('Currently only 1D data structures may be returned from slice operations.')
        spectral_axis = self.spectral_axis[key]
        uncertainty = None if self.uncertainty is None else self.uncertainty[key]
        wcs = None if self.wcs is None else self.wcs[key]
        mask = None if self.mask is None else self.mask[key]
        if self.meta is None:
            meta = None
        else:
            try:
                meta = self.meta[key]
            except KeyError:
                meta = self.meta

            return Spectrum1D(flux=flux, spectral_axis=spectral_axis, uncertainty=uncertainty,
              wcs=wcs,
              mask=mask,
              meta=meta)

    @classmethod
    def from_spectra(cls, spectra):
        """
        Create a spectrum collection from a set of individual
        :class:`specutils.Spectrum1D` objects.

        Parameters
        ----------
        spectra : list, ndarray
            A list of :class:`~specutils.Spectrum1D` objects to be held in the
            collection.
        """
        if not all((x.shape == spectra[0].shape for x in spectra)):
            raise ValueError('Shape of all elements must be the same.')
        else:
            flux = u.Quantity([spec.flux for spec in spectra])
            spectral_axis = u.Quantity([spec.spectral_axis for spec in spectra])
            if not all((x.uncertainty is None for x in spectra)):
                if any((x.uncertainty is not None for x in spectra)) and all((x.uncertainty.uncertainty_type == spectra[0].uncertainty.uncertainty_type for x in spectra)):
                    quncs = u.Quantity([spec.uncertainty.quantity for spec in spectra])
                    uncertainty = spectra[0].uncertainty.__class__(quncs)
                else:
                    uncertainty = None
                    logging.warning('Not all spectra have associated uncertainties of the same type, skipping uncertainties.')
                if not all((x.mask is None for x in spectra)):
                    if any((x.mask is not None for x in spectra)):
                        mask = np.array([spec.mask for spec in spectra])
            else:
                mask = None
                logging.warning('Not all spectra have associated masks, skipping masks.')
        wcs = [spec.wcs for spec in spectra]
        meta = [spec.meta for spec in spectra]
        return cls(flux=flux, spectral_axis=spectral_axis, uncertainty=uncertainty,
          wcs=wcs,
          mask=mask,
          meta=meta)

    @property
    def flux(self):
        """The flux in the spectrum as a `~astropy.units.Quantity`."""
        return self._flux

    @property
    def spectral_axis(self):
        """The spectral axes as a `~astropy.units.Quantity`."""
        return self._spectral_axis

    @property
    def frequency(self):
        """
        The spectral axis as a frequency `~astropy.units.Quantity` (in GHz).
        """
        return self.spectral_axis.to(u.GHz, u.spectral())

    @property
    def wavelength(self):
        """
        The spectral axis as a wavelength `~astropy.units.Quantity` (in
        Angstroms).
        """
        return self.spectral_axis.to(u.AA, u.spectral())

    @property
    def energy(self):
        """
        The spectral axis as an energy `~astropy.units.Quantity` (in eV).
        """
        return self.spectral_axis.to(u.eV, u.spectral())

    @property
    def wcs(self):
        """The WCS's as an object array"""
        return self._wcs

    @property
    def uncertainty(self):
        """The uncertainty in the spectrum as a `~astropy.units.Quantity`."""
        return self._uncertainty

    @property
    def mask(self):
        """The mask array for the spectrum."""
        return self._mask

    @property
    def meta(self):
        """A dictionary of metadata for theis spectrum collection, or `None`."""
        return self._meta

    @property
    def shape(self):
        """
        The shape of the collection. This is *not* the same as
        the shape of the flux et al., because the trailing (spectral)
        dimension is not included here.
        """
        return self.flux.shape[:-1]

    def __len__(self):
        return self.shape[0]

    @property
    def ndim(self):
        """
        The dimensionality of the collection. This is *not* the same as
        the dimensionality of the flux et al., because the trailing (spectral)
        dimension is not included here.
        """
        return self.flux.ndim - 1

    @property
    def nspectral(self):
        """
        The length of the spectral dimension.
        """
        return self.flux.shape[(-1)]

    def __repr__(self):
        return 'SpectrumCollection(ndim={}, shape={})\n    Flux units:          {}\n    Spectral axis units: {}\n    Uncertainty type:    {}'.format(self.ndim, self.shape, self.flux.unit, self.spectral_axis.unit, self.uncertainty.uncertainty_type if self.uncertainty is not None else None)