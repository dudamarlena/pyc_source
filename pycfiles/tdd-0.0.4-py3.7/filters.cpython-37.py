# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/tdd/filters.py
# Compiled at: 2019-03-27 17:17:54
# Size of source mod 2**32: 2164 bytes
"""
Module executed an install and setup to register both LSST and MEGACAM filters
as SNCosmo bands.

This allows SNCosmo to automatically use the 
    LSST bandpass objects through the string 'lsst_b' where b is one of 'ugrizy'
    Megacam bandpass objects through the string 'megab' where b is one of 'ugrizy'

Note : The megacam bands added are the 'average' megacam bands using in ugriz.
1. Post 2007 (June), the i band has been changed to i2. This is important for
    SNLS5, but SNLS3 was taken prior to that. 
2. For the precise analysis of MEGACAM SN, one needs to take into account the
    dependence of the radial position of the SN. This is not done here.
"""
from __future__ import absolute_import
import os, numpy as np
from astropy.units import Unit
import sncosmo
lsstbandPassList = [
 'u', 'g', 'r', 'i', 'z', 'y']
lsstbanddir = os.path.join(os.getenv('THROUGHPUTS_DIR'), 'baseline')
megacamPassList = 'ugriz'
megacambanddir = os.path.join(os.getenv('THROUGHPUTS_DIR'), 'megacam')
for band in lsstbandPassList:
    bandfname = lsstbanddir + '/total_' + band + '.dat'
    numpyband = np.loadtxt(bandfname)
    sncosmoband = sncosmo.Bandpass(wave=(numpyband[:, 0]), trans=(numpyband[:, 1]),
      wave_unit=(Unit('nm')),
      name=('lsst' + band))
    sncosmo.registry.register(sncosmoband, force=True)

for band in megacamPassList:
    bandfname = os.path.join(megacambanddir, band + 'Mega.fil.txt')
    numpyband = np.loadtxt(bandfname)
    sncosmoband = sncosmo.Bandpass(wave=(numpyband[:, 0]), trans=(numpyband[:, 1]),
      wave_unit=(Unit('nm')),
      name=('megacam' + band))
    sncosmo.registry.register(sncosmoband, force=True)