# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/nearl/projects/specutils/build/lib/specutils/io/default_loaders/sdss.py
# Compiled at: 2020-03-17 18:47:05
# Size of source mod 2**32: 4351 bytes
"""
Loader for SDSS individual spectrum files: spec_ files.

.. _spec: https://data.sdss.org/datamodel/files/BOSS_SPECTRO_REDUX/RUN2D/spectra/PLATE4/spec.html
"""
import os, re
from astropy.io import fits
from astropy.table import Table
from astropy.wcs import WCS
from astropy.units import Unit, def_unit
from astropy.nddata import StdDevUncertainty
import numpy as np
from specutils.io.registers import data_loader, custom_writer
from specutils import Spectrum1D
__all__ = [
 'spec_identify', 'spSpec_identify',
 'spec_loader', 'spSpec_loader']
_spSpec_pattern = re.compile('spSpec-\\d{5}-\\d{4}-\\d{3}\\.fit')
_spec_pattern = re.compile('spec-\\d{4,5}-\\d{5}-\\d{4}\\.fits')

def spec_identify(origin, *args, **kwargs):
    """
    Check whether given file is FITS and has SDSS-III/IV spec type
    BINTABLE in first extension. This is used for Astropy I/O Registry.
    """
    with fits.open(args[0]) as (hdulist):
        return hdulist[0].header['TELESCOP'] == 'SDSS 2.5-M' and len(hdulist) > 1 and isinstance(hdulist[1], fits.BinTableHDU) and hdulist[1].header['TTYPE3'] == 'ivar'


def spSpec_identify(origin, *args, **kwargs):
    """
    Check whether given file is FITS with SDSS-I/II spSpec type data.
    This is used for Astropy I/O Registry.
    """
    with fits.open(args[0]) as (hdulist):
        return hdulist[0].header['TELESCOP'] == 'SDSS 2.5-M' and isinstance(hdulist[0].data, np.ndarray) and hdulist[0].data.shape[0] == 5


@data_loader(label='SDSS-III/IV spec', identifier=spec_identify, extensions=['fits'])
def spec_loader(file_name, **kwargs):
    """
    Loader for SDSS-III/IV optical spectrum "spec" files.

    Parameters
    ----------
    file_name: str
        The path to the FITS file

    Returns
    -------
    data: Spectrum1D
        The spectrum that is represented by the data in this table.
    """
    hdulist = (fits.open)(file_name, **kwargs)
    header = hdulist[0].header
    name = header.get('NAME')
    meta = {'header': header}
    data = hdulist[1].data['flux']
    unit = Unit('1e-17 erg / (Angstrom cm2 s)')
    stdev = np.sqrt(1.0 / hdulist[1].data['ivar'])
    uncertainty = StdDevUncertainty(stdev * unit)
    dispersion = 10 ** hdulist[1].data['loglam']
    dispersion_unit = Unit('Angstrom')
    mask = hdulist[1].data['and_mask'] != 0
    hdulist.close()
    return Spectrum1D(flux=(data * unit), spectral_axis=(dispersion * dispersion_unit),
      uncertainty=uncertainty,
      meta=meta,
      mask=mask)


@data_loader(label='SDSS-I/II spSpec', identifier=spSpec_identify, extensions=['fits'])
def spSpec_loader(file_name, **kwargs):
    """
    Loader for SDSS-I/II spSpec files.

    Parameters
    ----------
    file_name: str
        The path to the FITS file

    Returns
    -------
    data: Spectrum1D
        The spectrum that is represented by the data in this table.
    """
    hdulist = (fits.open)(file_name, **kwargs)
    header = hdulist[0].header
    name = header.get('NAME')
    meta = {'header': header}
    wcs = WCS(hdulist[0].header)
    data = hdulist[0].data[0, :]
    unit = Unit('1e-17 erg / (Angstrom cm2 s)')
    uncertainty = StdDevUncertainty(hdulist[0].data[2, :] * unit)
    dispersion = 10 ** wcs.all_pix2world(np.vstack((np.arange(data.shape[0]),
     np.zeros((data.shape[0],)))).T, 0)[:, 0]
    dispersion_unit = Unit('Angstrom')
    mask = hdulist[0].data[3, :] != 0
    hdulist.close()
    return Spectrum1D(flux=(data * unit), spectral_axis=(dispersion * dispersion_unit),
      uncertainty=uncertainty,
      meta=meta,
      mask=mask)