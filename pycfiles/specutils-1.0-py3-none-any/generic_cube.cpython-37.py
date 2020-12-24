# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/nearl/projects/specutils/build/lib/specutils/io/default_loaders/generic_cube.py
# Compiled at: 2020-03-17 18:47:05
# Size of source mod 2**32: 2808 bytes
import logging, os, numpy as np
from astropy.io import fits
from astropy.units import Unit
from astropy.wcs import WCS
from ..registers import data_loader
from ...spectra import Spectrum1D

def identify_generic_fits(origin, *args, **kwargs):
    return isinstance(args[0], str) and (fits.connect.is_fits)(origin, *args) and fits.getheader(args[0])['NAXIS'] == 3


def generic_fits(file_name, **kwargs):
    name = os.path.basename(file_name.rstrip(os.sep)).rsplit('.', 1)[0]
    with (fits.open)(file_name, **kwargs) as (hdulist):
        header = hdulist[0].header
        data3 = hdulist[0].data
        wcs = WCS(header)
        shape = data3.shape
        if 'pos' in kwargs:
            ix = kwargs['pos'][0]
            iy = kwargs['pos'][1]
        else:
            ix = int(wcs.wcs.crpix[0])
            iy = int(wcs.wcs.crpix[1])
        if len(shape) == 3:
            data = data3[:, iy, ix]
        else:
            if len(shape) == 4:
                data = data3[:, :, iy, ix].squeeze()
            else:
                logging.error('Unexpected shape %s.', shape)
        meta = {'header': header}
        meta['xpos'] = ix
        meta['ypos'] = iy
        data = data * Unit('Jy')
        sp_axis = 3
        naxis3 = header[('NAXIS%d' % sp_axis)]
        cunit3 = wcs.wcs.cunit[(sp_axis - 1)]
        crval3 = wcs.wcs.crval[(sp_axis - 1)]
        cdelt3 = wcs.wcs.cdelt[(sp_axis - 1)]
        crpix3 = wcs.wcs.crpix[(sp_axis - 1)]
        freqs = np.arange(naxis3) + 1
        freqs = (freqs - crpix3) * cdelt3 + crval3
        freqs = freqs * cunit3
    return Spectrum1D(flux=data, wcs=wcs, meta=meta, spectral_axis=freqs)