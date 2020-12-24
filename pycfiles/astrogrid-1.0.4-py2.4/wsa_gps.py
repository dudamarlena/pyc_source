# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-9.6.0-i386/egg/astrogrid/examples/wsa_gps.py
# Compiled at: 2008-11-10 08:33:29
"""
Sends a query to the WFCAM Science Archive UKIDSS DR1
and saves the result to a file in local disk.

Usage:

    python wsa_gps.py

will write a file named wsa_gps_res.vot to the current directory. 

History:

   20071212 Written by E. A. Gonzalez-Solares

"""
import urllib
from time import sleep
from astrogrid import acr, DSA, MySpace
acr.login()
sql = 'SELECT TOP 10\n          s.sourceID, s.ra, s."dec", s.jmhPnt, s.pStar, s.pGalaxy, s.pNoise, s.pSaturated, \n          s.jAperMag3, s.jAperMag3Err, s.jClass, s.hAperMag3, s.hAperMag3Err, s.hClass, \n          s.k_1AperMag3, s.k_1AperMag3Err, s.k_1Class, d.x, d.y, m.xSize, m.ySize, c.xPixSize, \n          c.yPixSize \n      FROM \n          gpsSource AS s, gpsDetection AS d, MultiframeDetector AS m, CurrentAstrometry AS c \n      WHERE\n          s.k_1ObjId = d.objID AND d.multiframeID = m.multiframeID AND d.extNum = m.extNum AND\n          d.multiframeID = c.multiframeID AND d.extNum = c.extNum AND\n          d.x*c.xPixSize>10 AND d.y*c.yPixSize>10 AND\n          (m.xSize-d.x)*c.xPixSize>10 AND (m.ySize-d.y)*c.yPixSize>10'
dsa = DSA('ivo://wfau.roe.ac.uk/ukidssDR1-dsa/wsa/ceaApplication')
sql = (' ').join(sql.split())
r = dsa.query(sql, saveAs='#dsa/wsa_gps.vot')
while r.status() != 'COMPLETED':
    sleep(10)

if r.status() == 'COMPLETED':
    url = r.results()[0]
    m = MySpace()
    m.readfile(url, ofile='wsa-gps.vot')
else:
    print job.results()[0]