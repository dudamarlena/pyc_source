# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-9.6.0-i386/egg/astrogrid/examples/sdss_adql.py
# Compiled at: 2008-03-28 19:01:16
import time, urllib
from astrogrid import acr, DSA, MySpace
acr.login()
m = MySpace()
dsa = DSA('ivo://wfau.roe.ac.uk/sdssdr5-dsa/dsa/ceaApplication')
tsql = 'SELECT a.ra, a."dec", a.psfMag_g, a.psfMag_r FROM PhotoTag AS a '
tsql += 'WHERE a.ra>110 AND a.ra<230 AND a."dec">%s AND a."dec"<=%s AND  (a.psfMag_g-a.psfMag_r <0.4 )  AND '
tsql += 'a.psfMag_r>20.0 AND a.psfMag_g>0 AND a.mode=1 AND a.probPSF=1'
for i in range(0, 60, 2):
    sql = tsql % (i, i + 2)
    r = dsa.query(sql, saveAs='#cam/ndec%02d-%02d.vot' % (i, i + 2))
    time.sleep(10)
    while r.status() not in ['COMPLETED', 'ERROR']:
        print r.status()
        time.sleep(10)

    print r.status()
    if r.status() == 'COMPLETED':
        url = r.results()[0]
        m.readfile(url, ofile='ndec%02d-%02d.vot' % (i, i + 2))
        print 'ndec%02d-%02d.vot' % (i, i + 2)