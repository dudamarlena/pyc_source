# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-9.6.0-i386/egg/astrogrid/examples/siapsearch_hst.py
# Compiled at: 2008-03-28 08:04:05
"""
Given a list of object names perform a SIAP search to the HST archive and retrieve the
list of images (Note: not the images)

"""
import os, time
from optparse import OptionParser
from astrogrid import acr, sesame
from astrogrid import SiapSearch
parser = OptionParser()
parser.add_option('-b', '--broadcast', action='store_true', default=False)
(options, args) = parser.parse_args()
if options.broadcast:
    acr.startplastic()
    time.sleep(2)
objects = [
 'HH111', 'HH30', 'HH211', 'HH47', 'M16', 'Trifid', 'HH524', 'Sigma Orionis', 'DG Tau', 'HL Tau', 'M16', 'IRAS 04302+2247']
s = sesame()
siap = SiapSearch('ivo://cadc.nrc.ca/siap/hst')
if not os.path.isdir('hst'):
    os.mkdir('hst')
for obj in objects:
    (coords, ra, dec) = s.resolve(obj)
    ofile = 'hst/%s.vot' % obj.replace(' ', '_').replace('+', 'p')
    if not os.access(ofile, os.F_OK):
        res = siap.execute(ra, dec, 30.0 / 3600.0)
        open(ofile, 'w').write(res)
        print obj, ofile
    if options.broadcast:
        acr.plastic.broadcast(ofile, 'TOPCAT')