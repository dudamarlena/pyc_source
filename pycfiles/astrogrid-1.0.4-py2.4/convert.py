# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-9.6.0-i386/egg/astrogrid/examples/convert.py
# Compiled at: 2008-03-31 06:02:01
"""
Convert a file from one format to another using STILTS.
"""
import time, urllib
from astrogrid import acr
from astrogrid import Applications, MySpace, ConeSearch
acr.login()
cone = ConeSearch('ivo://ned.ipac/Basic_Data_Near_Position')
vot = cone.execute(242.811, 54.596, 0.1, saveAs='#cones/ned.vot')
app = Applications('ivo://uk.ac.starlink/stilts', 'tcopy')
app.inputs['tcopy_in']['value'] = '#cones/ned.vot'
app.inputs['tcopy_ifmt']['value'] = 'VOTABLE'
app.inputs['tcopy_ofmt']['value'] = 'FITS'
app.outputs['tcopy_out']['value'] = '#cones/ned.fits'
res = app.submit()