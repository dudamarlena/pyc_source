# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/nearl/projects/specutils/build/lib/specutils/io/default_loaders/subaru_pfs_spec.py
# Compiled at: 2020-03-17 18:47:05
# Size of source mod 2**32: 2502 bytes
"""
Loader for PFS spectrum files.

https://github.com/Subaru-PFS/datamodel/blob/master/datamodel.txt
"""
import os, re
from astropy.io import fits
from astropy.units import Unit
from astropy.nddata import StdDevUncertainty
import numpy as np
from specutils.io.registers import data_loader
from specutils import Spectrum1D
__all__ = [
 'spec_identify', 'spec_loader']
_spec_pattern = re.compile('pfsObject-(?P<tract>\\d{5})-(?P<patch>.{3})-(?P<catId>\\d{3})-(?P<objId>\\d{8})-(?P<nVisit>\\d{2})-(?P<pfsVisitHash>0x\\w{8})\\.fits')

def spec_identify(origin, *args, **kwargs):
    """
    Check whether given filename is FITS. This is used for Astropy I/O
    Registry.
    """
    return isinstance(args[0], str) and _spec_pattern.match(args[0]) is not None and (fits.connect.is_fits)(origin, *args)


@data_loader(label='Subaru-pfsObject', identifier=spec_identify, extensions=[
 'fits'])
def spec_loader(file_name, **kwargs):
    """
    Loader for PFS combined spectrum files.

    Parameters
    ----------
    file_name: str
        The path to the FITS file

    Returns
    -------
    data: Spectrum1D
        The spectrum that is represented by the data in this table.
    """
    m = _spec_pattern.match(os.path.basename(file_name))
    with (fits.open)(file_name, **kwargs) as (hdulist):
        header = hdulist[0].header
        meta = {'header':header,  'tract':m['tract'], 
         'patch':m['patch'], 
         'catId':m['catId'], 
         'objId':m['objId'], 
         'nVisit':m['nVisit'], 
         'pfsVisitHash':m['pfsVisitHash']}
        data = hdulist[2].data['flux']
        unit = Unit('nJy')
        error = hdulist[2].data['fluxVariance']
        uncertainty = StdDevUncertainty(np.sqrt(error))
        wave = hdulist[2].data['lambda']
        wave_unit = Unit('nm')
        mask = hdulist[2].data['mask'] != 0
    return Spectrum1D(flux=(data * unit), spectral_axis=(wave * wave_unit),
      uncertainty=uncertainty,
      meta=meta,
      mask=mask)