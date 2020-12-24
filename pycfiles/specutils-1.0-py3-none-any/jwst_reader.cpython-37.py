# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/nearl/projects/specutils/build/lib/specutils/io/default_loaders/jwst_reader.py
# Compiled at: 2020-03-18 11:09:56
# Size of source mod 2**32: 5021 bytes
import warnings
import astropy.units as u
from astropy.units import Quantity
from astropy.table import Table
from astropy.io import fits
from astropy.nddata import StdDevUncertainty
from astropy.utils.exceptions import AstropyUserWarning
import numpy as np
from ...spectra import Spectrum1D, SpectrumList
from ..registers import data_loader
__all__ = [
 'jwst_x1d_single_loader', 'jwst_x1d_multi_loader']

def identify_jwst_x1d_fits(origin, *args, **kwargs):
    """
    Check whether the given file is a JWST x1d spectral data product.
    """
    is_jwst = _identify_jwst_fits(args[0])
    with fits.open((args[0]), memmap=False) as (hdulist):
        if is_jwst:
            if 'EXTRACT1D' in hdulist:
                if ('EXTRACT1D', 2) not in hdulist:
                    return True
        return False


def identify_jwst_x1d_multi_fits(origin, *args, **kwargs):
    """
    Check whether the given file is a JWST x1d spectral data product.
    """
    is_jwst = _identify_jwst_fits(args[0])
    with fits.open((args[0]), memmap=False) as (hdulist):
        if is_jwst:
            if ('EXTRACT1D', 2) in hdulist:
                return True
        return False


def _identify_jwst_fits(filename):
    """
    Check whether the given file is a JWST spectral data product.
    """
    try:
        with fits.open(filename, memmap=False) as (hdulist):
            if 'ASDF' not in hdulist:
                return False
            else:
                return hdulist[0].header['TELESCOP'] == 'JWST' or False
        return True
    except Exception:
        return False


@data_loader('JWST x1d', identifier=identify_jwst_x1d_fits, dtype=Spectrum1D, extensions=[
 'fits'])
def jwst_x1d_single_loader(filename, **kwargs):
    """
    Loader for JWST x1d 1-D spectral data in FITS format

    Parameters
    ----------
    filename: str
        The path to the FITS file

    Returns
    -------
    Spectrum1D
        The spectrum contained in the file.
    """
    spectrum_list = _jwst_x1d_loader(filename, **kwargs)
    if len(spectrum_list) == 1:
        return spectrum_list[0]
    raise RuntimeError(f"Input data has {len(spectrum_list)} spectra. Use SpectrumList.read() instead.")


@data_loader('JWST x1d multi', identifier=identify_jwst_x1d_multi_fits, dtype=SpectrumList,
  extensions=['fits'])
def jwst_x1d_multi_loader(filename, **kwargs):
    """
    Loader for JWST x1d 1-D spectral data in FITS format

    Parameters
    ----------
    filename: str
        The path to the FITS file

    Returns
    -------
    SpectrumList
        A list of the spectra that are contained in the file.
    """
    return _jwst_x1d_loader(filename, **kwargs)


def _jwst_x1d_loader(filename, **kwargs):
    """Implementation of loader for JWST x1d 1-D spectral data in FITS format

    Parameters
    ----------
    filename: str
        The path to the FITS file

    Returns
    -------
    SpectrumList
        A list of the spectra that are contained in the file.
    """
    spectra = []
    with fits.open(filename, memmap=False) as (hdulist):
        primary_header = hdulist[0].header
        for hdu in hdulist:
            if hdu.name != 'EXTRACT1D':
                continue
            else:
                data = Table.read(hdu)
                wavelength = Quantity(data['WAVELENGTH'])
                try:
                    srctype = hdu.header.get('srctype')
                except KeyError:
                    srctype = hdulist.header.get('srctype')

                if srctype == 'POINT':
                    flux = Quantity(data['FLUX'])
                    uncertainty = StdDevUncertainty(data['ERROR'])
                else:
                    if srctype == 'EXTENDED':
                        flux = Quantity(data['SURF_BRIGHT'])
                        uncertainty = StdDevUncertainty(hdu.data['SB_ERROR'])
                    else:
                        raise RuntimeError(f"Keyword SRCTYPE is {srctype}.  It should be 'POINT' or 'EXTENDED'. Can't decide between `flux` and `surf_bright` columns.")
            if np.min(uncertainty.array) <= 0.0:
                warnings.warn('Standard Deviation has values of 0 or less', AstropyUserWarning)
            slit_header = hdu.header
            header = primary_header.copy()
            header.extend(slit_header, strip=True, update=True)
            meta = {k:v for k, v in header.items()}
            spec = Spectrum1D(flux=flux, spectral_axis=wavelength, uncertainty=uncertainty,
              meta=meta)
            spectra.append(spec)

    return SpectrumList(spectra)