# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/nearl/projects/specutils/build/lib/specutils/io/default_loaders/muscles_sed.py
# Compiled at: 2020-03-17 18:47:05
# Size of source mod 2**32: 1988 bytes
import logging, os
from astropy.io import fits
from astropy.nddata import StdDevUncertainty
from astropy.table import Table
from astropy.units import Unit
from astropy.wcs import WCS
from ...spectra import Spectrum1D
from ..registers import data_loader

def identify_muscles_sed(origin, *args, **kwargs):
    return isinstance(args[0], str) and args[0].split('.')[0].endswith('sed') and (fits.connect.is_fits)(origin, *args) and len(fits.open(args[0])) > 1 and isinstance(fits.open(args[0])[1], fits.BinTableHDU) and fits.open(args[0])[0].header['PROPOSID'] == 13650


@data_loader('muscles-sed', identifier=identify_muscles_sed, dtype=Spectrum1D,
  extensions=['fits'])
def muscles_sed(file_name, **kwargs):
    """
    Load spectrum from a MUSCLES SED FITS file.

    Parameters
    ----------
    file_name: str
        The path to the FITS file.

    Returns
    -------
    data: Spectrum1D
        The spectrum that is represented by the data in this table.
    """
    with (fits.open)(file_name, **kwargs) as (hdulist):
        header = hdulist[0].header
        tab = Table.read(hdulist)
        meta = {'header': header}
        uncertainty = StdDevUncertainty(tab['ERROR'])
        data = tab['FLUX']
        wavelength = tab['WAVELENGTH']
    return Spectrum1D(flux=data, spectral_axis=wavelength, uncertainty=uncertainty,
      meta=meta,
      unit=(data.unit),
      spectral_axis_unit=(wavelength.unit))