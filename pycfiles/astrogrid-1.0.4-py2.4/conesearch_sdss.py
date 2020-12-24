# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-9.6.0-i386/egg/astrogrid/examples/conesearch_sdss.py
# Compiled at: 2008-03-31 05:26:56
"""This example shows how to submit a list of ra,dec positions to SDSS DR5.
"""
import sys, time, random, math
from astrogrid import ConeSearch
from astrogrid.threadpool import easy_pool
cone = ConeSearch('ivo://wfau.roe.ac.uk/sdssdr5-dsa/dsa', dsatab='PhotoObjAll')
nsrc = 20
ra = [ random.random() * math.pi * 2 * math.degrees(1) for i in range(nsrc) ]
dec = [ (random.random() * math.pi - math.pi / 2.0) * math.degrees(1) for i in range(nsrc) ]
radius = [0.001] * nsrc
for i in range(nsrc):
    res = cone.execute(ra[i], dec[i], radius[i])
    open('sdss%02d.vot' % (i + 1), 'w').write(res)
    print i + 1, 'sdss%02d.vot' % (i + 1)