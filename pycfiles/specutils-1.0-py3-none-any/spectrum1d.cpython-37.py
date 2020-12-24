# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/nearl/projects/specutils/build/lib/specutils/spectra/spectrum1d.py
# Compiled at: 2020-03-19 15:08:28
# Size of source mod 2**32: 16344 bytes
import logging
from copy import deepcopy
import numpy as np
from astropy import units as u
from astropy import constants as cnst
from astropy.nddata import NDDataRef
from astropy.utils.decorators import lazyproperty
from .spectrum_mixin import OneDSpectrumMixin
from .spectral_coordinate import SpectralCoord
from utils.wcs_utils import gwcs_from_array
__all__ = [
 'Spectrum1D']
__doctest_skip__ = [
 'Spectrum1D.spectral_resolution']
u.set_enabled_equivalencies(u.spectral())

class Spectrum1D(OneDSpectrumMixin, NDDataRef):
    __doc__ = '\n    Spectrum container for 1D spectral data.\n\n    Parameters\n    ----------\n    flux : `astropy.units.Quantity` or astropy.nddata.NDData`-like\n        The flux data for this spectrum.\n    spectral_axis : `astropy.units.Quantity` or `specutils.SpectralCoord`\n        Dispersion information with the same shape as the last (or only)\n        dimension of flux.\n    wcs : `astropy.wcs.WCS` or `gwcs.wcs.WCS`\n        WCS information object.\n    velocity_convention : {"doppler_relativistic", "doppler_optical", "doppler_radio"}\n        Convention used for velocity conversions.\n    rest_value : `~astropy.units.Quantity`\n        Any quantity supported by the standard spectral equivalencies\n        (wavelength, energy, frequency, wave number). Describes the rest value\n        of the spectral axis for use with velocity conversions.\n    redshift\n        See `redshift` for more information.\n    radial_velocity\n        See `radial_velocity` for more information.\n    uncertainty : `~astropy.nddata.NDUncertainty`\n        Contains uncertainty information along with propagation rules for\n        spectrum arithmetic. Can take a unit, but if none is given, will use\n        the unit defined in the flux.\n    meta : dict\n        Arbitrary container for any user-specific information to be carried\n        around with the spectrum container object.\n    '

    def __init__(self, flux=None, spectral_axis=None, wcs=None, velocity_convention=None, rest_value=None, redshift=None, radial_velocity=None, **kwargs):
        unknown_kwargs = set(kwargs).difference({
         'data', 'unit', 'uncertainty', 'meta', 'mask', 'copy'})
        if len(unknown_kwargs) > 0:
            raise ValueError('Initializer contains unknown arguments(s): {}.'.format(', '.join(map(str, unknown_kwargs))))
        if isinstance(flux, NDDataRef):
            super(Spectrum1D, self).__init__(flux)
            return
        if flux is not None and not isinstance(flux, u.Quantity):
            raise ValueError('Flux must be a `Quantity` object.')
        else:
            if flux.isscalar:
                flux = u.Quantity([flux])
            elif redshift is not None and radial_velocity is not None:
                raise ValueError('Cannot set both radial_velocity and redshift at the same time.')
            if flux is None:
                if 'data' in kwargs:
                    flux = kwargs.pop('data')
            kwargs.setdefault('unit', flux.unit if isinstance(flux, u.Quantity) else kwargs.get('unit'))
        if isinstance(flux, u.Quantity):
            if isinstance(flux, float) or isinstance(flux, int):
                if np.ndim(flux) == 0:
                    (super(Spectrum1D, self).__init__)(data=flux, wcs=wcs, **kwargs)
                    return
            if rest_value is None:
                if hasattr(wcs, 'rest_frequency') and wcs.rest_frequency != 0:
                    rest_value = wcs.rest_frequency * u.Hz
            elif hasattr(wcs, 'rest_wavelength') and wcs.rest_wavelength != 0:
                rest_value = wcs.rest_wavelength * u.AA
            else:
                rest_value = 0 * u.AA
        else:
            pass
        if not isinstance(rest_value, u.Quantity):
            logging.info("No unit information provided with rest value. Assuming units of spectral axis ('%s').", spectral_axis.unit)
            rest_value = u.Quantity(rest_value, spectral_axis.unit)
        else:
            if not rest_value.unit.is_equivalent(u.AA):
                if not rest_value.unit.is_equivalent(u.Hz):
                    raise u.UnitsError('Rest value must be energy/wavelength/frequency equivalent.')
                elif spectral_axis is not None:
                    if not isinstance(spectral_axis, u.Quantity):
                        raise ValueError('Spectral axis must be a `Quantity` or `SpectralCoord` object.')
                    self._spectral_axis = isinstance(spectral_axis, SpectralCoord) or SpectralCoord(spectral_axis,
                      redshift=redshift, radial_velocity=radial_velocity,
                      doppler_rest=rest_value,
                      doppler_convention=velocity_convention)
                else:
                    for a in [radial_velocity, redshift]:
                        if a is not None:
                            raise ValueError('Cannot separately set redshift or radial_velocity if a SpectralCoord object is input to spectral_axis')

                    self._spectral_axis = spectral_axis
                wcs = gwcs_from_array(spectral_axis)
            else:
                if wcs is None:
                    size = len(flux) if not flux.isscalar else 1
                    wcs = gwcs_from_array(np.arange(size) * u.Unit(''))
                elif flux is not None and spectral_axis is not None:
                    if not spectral_axis.shape[0] == flux.shape[(-1)]:
                        raise ValueError('Spectral axis ({}) and the last flux axis ({}) lengths must be the same.'.format(spectral_axis.shape[0], flux.shape[(-1)]))
                else:
                    (super(Spectrum1D, self).__init__)(data=flux.value if isinstance(flux, u.Quantity) else flux, 
                     wcs=wcs, **kwargs)
                    if spectral_axis is None:
                        spec_axis = self.wcs.pixel_to_world(np.arange(self.flux.shape[(-1)]))
                        self._spectral_axis = SpectralCoord(spec_axis,
                          redshift=redshift,
                          radial_velocity=radial_velocity,
                          doppler_rest=rest_value,
                          doppler_convention=velocity_convention)
                    if hasattr(self, 'uncertainty'):
                        if self.uncertainty is not None and not flux.shape == self.uncertainty.array.shape:
                            raise ValueError('Flux axis ({}) and uncertainty ({}) shapes must be the same.'.format(flux.shape, self.uncertainty.array.shape))

    def __getitem__(self, item):
        if len(self.flux.shape) > 1:
            return self._copy(flux=(self.flux[item]),
              uncertainty=(self.uncertainty[item] if self.uncertainty is not None else None))
        if not isinstance(item, slice):
            item = slice(item, item + 1, None)
        tmp_spec = super().__getitem__(item)
        return tmp_spec._copy(spectral_axis=(self.spectral_axis[item]))

    def _copy(self, **kwargs):
        """
        Peform deep copy operations on each attribute of the ``Spectrum1D``
        object.
        """
        alt_kwargs = dict(flux=(deepcopy(self.flux)),
          spectral_axis=(deepcopy(self.spectral_axis)),
          uncertainty=(deepcopy(self.uncertainty)),
          wcs=(deepcopy(self.wcs)),
          mask=(deepcopy(self.mask)),
          meta=(deepcopy(self.meta)),
          unit=(deepcopy(self.unit)),
          velocity_convention=(deepcopy(self.velocity_convention)),
          rest_value=(deepcopy(self.rest_value)))
        alt_kwargs.update(kwargs)
        return (self.__class__)(**alt_kwargs)

    @property
    def frequency(self):
        """
        The frequency as a `~astropy.units.Quantity` in units of GHz
        """
        return self.spectral_axis.to(u.GHz, u.spectral())

    @property
    def wavelength(self):
        """
        The wavelength as a `~astropy.units.Quantity` in units of Angstroms
        """
        return self.spectral_axis.to(u.AA, u.spectral())

    @property
    def energy(self):
        """
        The energy of the spectral axis as a `~astropy.units.Quantity` in units
        of eV.
        """
        return self.spectral_axis.to(u.eV, u.spectral())

    @property
    def photon_flux(self):
        """
        The flux density of photons as a `~astropy.units.Quantity`, in units of
        photons per cm^2 per second per spectral_axis unit
        """
        flux_in_spectral_axis_units = self.flux.to(u.W * u.cm ** (-2) * self.spectral_axis.unit ** (-1), u.spectral_density(self.spectral_axis))
        photon_flux_density = flux_in_spectral_axis_units / (self.energy / u.photon)
        return photon_flux_density.to(u.photon * u.cm ** (-2) * u.s ** (-1) * self.spectral_axis.unit ** (-1))

    @lazyproperty
    def bin_edges(self):
        return self.wcs.bin_edges()

    @property
    def shape(self):
        return self.flux.shape

    @property
    def redshift(self):
        """
        The redshift(s) of the objects represented by this spectrum.  May be
        scalar (if this spectrum's ``flux`` is 1D) or vector.  Note that
        the concept of "redshift of a spectrum" can be ambiguous, so the
        interpretation is set to some extent by either the user, or operations
        (like template fitting) that set this attribute when they are run on
        a spectrum.
        """
        return self.spectral_axis.redshift

    @redshift.setter
    def redshift(self, val):
        new_spec_coord = self.spectral_axis.with_redshift(val)
        self._spectral_axis = new_spec_coord

    @property
    def radial_velocity(self):
        """
        The radial velocity(s) of the objects represented by this spectrum.  May
        be scalar (if this spectrum's ``flux`` is 1D) or vector.  Note that
        the concept of "RV of a spectrum" can be ambiguous, so the
        interpretation is set to some extent by either the user, or operations
        (like template fitting) that set this attribute when they are run on
        a spectrum.
        """
        return self.spectral_axis.radial_velocity

    @radial_velocity.setter
    def radial_velocity(self, val):
        if val is not None:
            if not val.unit.is_equivalent(u.km / u.s):
                raise u.UnitsError('Radial velocity must be a velocity.')
        new_spectral_axis = self.spectral_axis.with_radial_velocity(val)
        self._spectral_axis = new_spectral_axis

    def __add__(self, other):
        if not isinstance(other, NDDataRef):
            other = u.Quantity(other, unit=(self.unit))
        return self.add(other)

    def __sub__(self, other):
        if not isinstance(other, NDDataRef):
            other = u.Quantity(other, unit=(self.unit))
        return self.subtract(other)

    def __mul__(self, other):
        if not isinstance(other, NDDataRef):
            other = u.Quantity(other)
        return self.multiply(other)

    def __div__(self, other):
        if not isinstance(other, NDDataRef):
            other = u.Quantity(other)
        return self.divide(other)

    def __truediv__(self, other):
        if not isinstance(other, NDDataRef):
            other = u.Quantity(other)
        return self.divide(other)

    def _format_array_summary(self, label, array):
        if len(array) == 1:
            mean = np.mean(array)
            s = '{:17} [ {:.5} ],  mean={:.5}'
            return s.format(label + ':', array[0], array[(-1)], mean)
        if len(array) > 1:
            mean = np.mean(array)
            s = '{:17} [ {:.5}, ..., {:.5} ],  mean={:.5}'
            return s.format(label + ':', array[0], array[(-1)], mean)
        return '{:17} [ ],  mean= n/a'.format(label + ':')

    def __str__(self):
        result = 'Spectrum1D '
        if self.flux.ndim == 0:
            result += '(length=1)\n'
            return result + 'flux:   {}'.format(self.flux)
            result += '(length={})\n'.format(len(self.spectral_axis))
            if self.flux.ndim > 1:
                for i, flux in enumerate(self.flux):
                    label = 'flux{:2}'.format(i)
                    result += self._format_array_summary(label, flux) + '\n'

        else:
            result += self._format_array_summary('flux', self.flux) + '\n'
        result += self._format_array_summary('spectral axis', self.spectral_axis)
        if self.uncertainty:
            result += '\nuncertainty:      [ {}, ..., {} ]'.format(self.uncertainty[0], self.uncertainty[(-1)])
        return result

    def __repr__(self):
        inner_str = 'flux={}, spectral_axis={}'.format(repr(self.flux), repr(self.spectral_axis))
        if self.uncertainty is not None:
            inner_str += ', uncertainty={}'.format(repr(self.uncertainty))
        result = '<Spectrum1D({})>'.format(inner_str)
        return result