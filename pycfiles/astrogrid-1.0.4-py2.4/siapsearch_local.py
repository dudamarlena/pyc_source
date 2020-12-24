# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-9.6.0-i386/egg/astrogrid/examples/siapsearch_local.py
# Compiled at: 2008-11-18 03:33:26
"""
Given a list of RA and Dec positions perform a SIAP search saving the 
resultant VOTables and images to MySpace.
"""
import os, re, urllib
from time import sleep
from astrogrid import acr
from astrogrid import SiapSearch
ra = [
 180.0, 181.0]
dec = [0.0, 0.1]
siap = SiapSearch('ivo://nasa.heasarc/skyview/sdss')
if not os.access('sdss', os.R_OK):
    os.mkdir('sdss')
for i in range(len(ra)):
    odir = 'sdss/obj%02d' % (i + 1)
    if not os.access(odir, os.R_OK):
        os.mkdir(odir)
    res = siap.execute(ra[i], dec[i], 30.0 / 3600.0)
    open(os.path.join(odir, 'sdss.vot'), 'w').write(res)
    j = 0
    for img in re.compile('http://.\\S+FITS').findall(res):
        print img
        j = j + 1
        urllib.urlretrieve(img, os.path.join(odir, 'image%d.fits' % j))