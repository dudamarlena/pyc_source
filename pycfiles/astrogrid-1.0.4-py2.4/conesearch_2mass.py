# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-9.6.0-i386/egg/astrogrid/examples/conesearch_2mass.py
# Compiled at: 2008-04-02 04:57:55
"""
Given an input table containig a list of objects, 
queries the 2MASS catalogue returning a VOTable for each object.

History:
   Mar 2008. Updated IVORN for registry version 1 included in VODesktop 1.0 [EGS]
   Written by E. A. Gonzalez-Solares [EGS]

"""
import os
from astrogrid import ConeSearch
from astrogrid.utils import read_votable
import urllib
url = 'http://help.astrogrid.org/raw-attachment/wiki/Help/IntroScripting/AstrogridPython/sample.vot'
urllib.urlretrieve(url, 'sample.vot')
vot = read_votable('sample.vot')
id = vot['ID_IDENTIFIER']
ra = map(float, vot['POS_EQ_RA_MAIN'])
dec = map(float, vot['POS_EQ_DEC_MAIN'])
ivorn = 'ivo://wfau.roe.ac.uk/twomass-dsa/wsa'
cone = ConeSearch(ivorn)
nsrc = len(ra)
radius = 0.1
print 'Starting Query: %d objects' % nsrc
nsrc = 2
if not os.access('out', os.R_OK):
    os.makedirs('out')
for i in range(nsrc):
    res = cone.execute(ra[i], dec[i], radius, dsatab='twomass_psc')
    ofile = id[i].replace(' ', '_')
    print 'Writting 2mass_%s.vot' % ofile
    if res:
        open(os.path.join('out', '2mass_%s.vot' % ofile), 'w').write(res)