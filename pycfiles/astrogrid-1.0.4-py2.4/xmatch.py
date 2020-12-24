# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-9.6.0-i386/egg/astrogrid/examples/xmatch.py
# Compiled at: 2008-03-28 18:57:04
"""
Executes two cone searches to NED and 2MASS and cross matches the resultant tables
retrieving the cross match outout to local disk.
"""
import time, urllib
from astrogrid import acr
from astrogrid import Applications, ConeSearch, MySpace
acr.login()
cone1 = ConeSearch('ivo://ned.ipac/Basic_Data_Near_Position')
vot1 = cone1.execute(242.811, 54.596, 0.1, saveAs='#cones/ned.vot')
cone2 = ConeSearch('ivo://wfau.roe.ac.uk/twomass-dsa/wsa')
vot2 = cone2.execute(242.811, 54.596, 0.1, dsatab='twomass_psc', saveAs='#cones/twomass_psc.vot')
app = Applications('ivo://uk.ac.starlink/stilts', 'tmatch2')
app.inputs['tmatch2_in1']['value'] = vot1
app.inputs['tmatch2_in2']['value'] = vot2
app.inputs['tmatch2_params']['value'] = '2'
app.inputs['tmatch2_values1']['value'] = '$3 $4'
app.inputs['tmatch2_values2']['value'] = 'ra dec'
app.inputs['tmatch2_ofmt']['value'] = 'votable-tabledata'
app.outputs['tmatch2_out']['value'] = '#cones/ned2mass-xmatch.vot'
app.inputs.pop('tmatch2_icmd1')
app.inputs.pop('tmatch2_icmd2')
app.inputs.pop('tmatch2_ocmd')
job = app.submit()
while job.status() not in ['COMPLETED', 'ERROR']:
    time.sleep(10)

if job.status() == 'COMPLETED':
    url = job.results()[0]
    m = MySpace()
    m.readfile(url, ofile='ned2mass-xmatch.vot')
else:
    print job.results()[0]