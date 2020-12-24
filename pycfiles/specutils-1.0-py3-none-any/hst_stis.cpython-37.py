# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/nearl/projects/specutils/build/lib/specutils/io/default_loaders/hst_stis.py
# Compiled at: 2020-03-17 18:47:05
# Size of source mod 2**32: 1717 bytes
import os
from astropy.io import fits
from astropy.units import Unit
from astropy.nddata import StdDevUncertainty
from specutils.io.registers import data_loader
from specutils import Spectrum1D
__all__ = [
 'stis_identify', 'stis_spectrum_loader']

def stis_identify(origin, *args, **kwargs):
    """Check whether given file contains HST/STIS spectral data."""
    with fits.open(args[0]) as (hdu):
        if hdu[0].header['TELESCOP'] == 'HST':
            if hdu[0].header['INSTRUME'] == 'STIS':
                return True
    return False


@data_loader(label='HST/STIS', identifier=stis_identify, extensions=['FITS', 'FIT', 'fits', 'fit'])
def stis_spectrum_loader(file_name, **kwargs):
    """
    Load STIS spectral data from the MAST archive into a spectrum object.

    Parameters
    ----------
    file_name: str
        The path to the FITS file

    Returns
    -------
    data: Spectrum1D
        The spectrum that is represented by the data in this table.
    """
    with (fits.open)(file_name, **kwargs) as (hdu):
        header = hdu[0].header
        name = header.get('FILENAME')
        meta = {'header': header}
        unit = Unit('erg/cm**2 Angstrom s')
        disp_unit = Unit('Angstrom')
        data = hdu[1].data['FLUX'].flatten() * unit
        dispersion = hdu[1].data['wavelength'].flatten() * disp_unit
        uncertainty = StdDevUncertainty(hdu[1].data['ERROR'].flatten() * unit)
        sort_idx = dispersion.argsort()
        dispersion = dispersion[sort_idx]
        data = data[sort_idx]
        uncertainty = uncertainty[sort_idx]
    return Spectrum1D(flux=data, spectral_axis=dispersion,
      uncertainty=uncertainty,
      meta=meta)