# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-9.6.0-i386/egg/astrogrid/examples/xmatch_ukidss_sdss.py
# Compiled at: 2008-10-17 05:03:56
"""
Executes two cone searches to UKIDSS DR1 and SDSS and cross matches the resultant tables
retrieving the cross match outout to local disk.
"""
import time, urllib
from astrogrid import acr
from astrogrid import Applications, ConeSearch, MySpace
acr.login()
ra = 152.8
dec = 8.5
radius = 0.1
cone1 = ConeSearch('ivo://wfau.roe.ac.uk/ukidssDR1-dsa/wsa')
vot1 = cone1.execute(ra, dec, radius, saveAs='#cones/ukidsslas.vot', dsatab='lasSource', clobber=True)
cone2 = ConeSearch('ivo://wfau.roe.ac.uk/sdssdr5-dsa/dsa')
vot2 = cone2.execute(ra, dec, radius, dsatab='PhotoObjAll', saveAs='#cones/sdsslas.vot', clobber=True)
app = Applications('ivo://uk.ac.starlink/stilts', 'tmatch2')
app.inputs['tmatch2_in1']['value'] = vot1
app.inputs['tmatch2_in2']['value'] = vot2
app.inputs['tmatch2_params']['value'] = '1.0'
app.inputs['tmatch2_values1']['value'] = 'ra dec'
app.inputs['tmatch2_values2']['value'] = 'ra dec'
app.inputs['tmatch2_ofmt']['value'] = 'votable-tabledata'
app.outputs['tmatch2_out']['value'] = '#cones/lassdss-xmatch.vot'
app.inputs.pop('tmatch2_icmd1')
app.inputs.pop('tmatch2_icmd2')
app.inputs.pop('tmatch2_ocmd')
job = app.submit()
while job.status() not in ['COMPLETED', 'ERROR']:
    time.sleep(10)

if job.status() == 'COMPLETED':
    url = job.results()[0]
    m = MySpace()
    m.readfile(url, ofile='lassdss-xmatch.vot')
else:
    print job.results()[0]