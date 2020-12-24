# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\time_test.py
# Compiled at: 2014-01-02 22:33:14
from FastGeo import GeoDB
import sys, random
from datetime import datetime
if __name__ == '__main__':
    t = GeoDB()
    print 'Running 50000 random lookups...'
    milli_diff = lambda a: (a.days * 24 * 60 * 60 + a.seconds) * 1000 + a.microseconds / 1000.0
    total = 0.0
    for _ in xrange(50000):
        milli_diff
        ip = random.randrange(16777216, 3758096383)
        start = datetime.now()
        t.lookup(long(ip))
        end = datetime.now()
        d = milli_diff(end - start)
        total += d

    print 'Performed 50,000 random IP lookups in %.1f milliseconds.' % total
    print 'Average lookup time: %.4f milliseconds' % (total / 50000)
    print 'Load check: %s' % ('true' if t.lookup('1.0.0.255') is not None else 'false')
    raw_input('Press enter to exit...')