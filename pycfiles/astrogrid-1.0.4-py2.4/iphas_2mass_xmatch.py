# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-9.6.0-i386/egg/astrogrid/examples/iphas_2mass_xmatch.py
# Compiled at: 2008-03-28 18:59:31
import sys
from math import cos, radians
import time
from astrogrid import acr
from astrogrid import Applications, DSA, MySpace
acr.login('leicester')
(ra, dec) = (312.75, 44.37)
output_dir = '#iphas'
ra1 = ra - 0.25 / cos(radians(ra))
dec1 = dec - 0.25
ra2 = ra + 0.25 / cos(radians(ra))
dec2 = dec + 0.25
twomass = DSA('ivo://wfau.roe.ac.uk/twomass-dsa/wsa/ceaApplication')
job1 = twomass.query('select * from twomass_psc as x where x.ra between %s and %s and x."dec" between %s and %s' % (ra1, ra2, dec1, dec2), saveAs='%s/twomass.vot' % output_dir)
while job1.status() in ['INITIALIZING', 'RUNNING', 'UNKNOWN']:
    time.sleep(10)

if job1.status() == 'ERROR':
    print 'Error querying 2MASS database'
    print job1.results()[0]
    sys.exit()
print '2MASS Query: ', job1.status()
iphas = DSA('ivo://uk.ac.cam.ast/iphas-dsa-catalog/IDR/ceaApplication')
job2 = iphas.query('select * from PhotoObjBest as x where x.ra between %s and %s and x."dec" between %s and %s' % (ra1, ra2, dec1, dec2), saveAs='%s/iphas.vot' % output_dir)
while job2.status() in ['INITIALIZING', 'RUNNING', 'UNKNOWN']:
    time.sleep(10)

if job2.status() == 'ERROR':
    print 'Error querying IPHAS database'
    print job2.results()[0]
    sys.exit()
print 'IPHAS Query: ', job1.status()
m = MySpace()
app = Applications('ivo://uk.ac.starlink/stilts', 'tmatch2')
app.inputs['tmatch2_in1']['value'] = '%s/iphas.vot' % output_dir
app.inputs['tmatch2_in2']['value'] = '%s/twomass.vot' % output_dir
app.inputs['tmatch2_values1']['value'] = 'ra dec'
app.inputs['tmatch2_values2']['value'] = 'ra dec'
app.inputs['tmatch2_params']['value'] = '1.5'
app.inputs['tmatch2_ifmt1']['value'] = '(auto)'
app.inputs['tmatch2_ifmt2']['value'] = '(auto)'
app.inputs['tmatch2_ofmt']['value'] = 'vot'
app.inputs.pop('tmatch2_icmd1')
app.inputs.pop('tmatch2_icmd2')
app.inputs.pop('tmatch2_ocmd')
app.outputs['tmatch2_out']['value'] = '%s/iphas_twomass.vot' % output_dir
job = app.submit()
while job.status() in ['INITIALIZING', 'RUNNING', 'UNKNOWN']:
    time.sleep(10)

if job.status() == 'ERROR':
    print 'Error running xmatch'
    sys.exit()
print 'Xmatch: ', job.status()
if job.status() == 'COMPLETED':
    url = job.results()[0]
    m = MySpace()
    m.readfile(url, ofile='iphas2mass-xmatch.vot')
else:
    print job.results()[0]