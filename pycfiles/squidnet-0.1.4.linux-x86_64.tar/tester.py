# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.5/site-packages/squidnet/tester.py
# Compiled at: 2010-04-06 18:14:05
import sexp, time
N = 100
data = open('./data').read()
start = time.time()
for i in xrange(N):
    sexp.read_all(data)

print 'Rate: %0.2d creates/sec' % (N / float(time.time() - start))