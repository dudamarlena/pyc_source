# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/nearl/projects/specutils/build/lib/specutils/spectra/spectrum_list.py
# Compiled at: 2020-01-06 10:58:55
# Size of source mod 2**32: 335 bytes
from astropy.nddata import NDIOMixin
__all__ = [
 'SpectrumList']

class SpectrumList(list, NDIOMixin):
    __doc__ = '\n    A list that is used to hold a list of Spectrum1D objects\n\n    The primary purpose of this class is to allow loaders to return a list of\n    heterogenous spectra that do have a spectral axis of the same length.\n    '