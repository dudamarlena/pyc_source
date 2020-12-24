# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-9.6.0-i386/egg/astrogrid/examples/siapsearch.py
# Compiled at: 2008-03-28 09:33:16
"""
Given a list of RA and Dec positions perform a SIAP search saving the 
resultant VOTables and images to MySpace.
"""
import os
from time import sleep
from astrogrid import acr
from astrogrid import SiapSearch
acr.login()
ra = [
 180.0, 181.0]
dec = [0.0, 0.1]
siap = SiapSearch('ivo://nasa.heasarc/skyview/sdss')
for i in range(len(ra)):
    odir = '#siap/sdss/obj%02d' % (i + 1)
    (out, th) = siap.execute(ra[i], dec[i], 30.0 / 3600.0, saveAs=odir + '/sdss.vot', saveDatasets=odir, clobber=True)
    while th.isAlive():
        sleep(10)