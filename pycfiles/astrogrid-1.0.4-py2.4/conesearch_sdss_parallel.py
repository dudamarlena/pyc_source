# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-9.6.0-i386/egg/astrogrid/examples/conesearch_sdss_parallel.py
# Compiled at: 2008-03-31 05:28:12
"""This example shows how to submit a list of ra,dec positions to SDSS DR5
running 4 in parallel.
"""
import sys, time, math, random
from astrogrid import ConeSearch
from astrogrid.threadpool import easy_pool
cone = ConeSearch('ivo://wfau.roe.ac.uk/sdssdr5-dsa/dsa', dsatab='PhotoObjAll')
nsrc = 20
ra = [ random.random() * math.pi * 2 * math.degrees(1) for i in range(nsrc) ]
dec = [ (random.random() * math.pi - math.pi / 2.0) * math.degrees(1) for i in range(nsrc) ]
radius = [0.001] * nsrc
pool = easy_pool(cone.execute)
pool.start_threads(4)
for i in range(nsrc):
    input = (
     ra[i], dec[i], radius[i])
    pool.put(input)

i = 0
while 1:
    p = pool.qinfo()
    print 'Time: %3d sec    Queued: %2d    Running: %2d    Finished: %2d' % (i, p[1], nsrc - p[1] - p[3], p[3])
    time.sleep(2)
    i = i + 2
    if p[3] == nsrc:
        break

pool.stop_threads()
i = 0
for res in pool.get_all():
    i = i + 1
    open('sdss%02d.vot' % i, 'w').write(res)