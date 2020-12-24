# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\supervisor\tests\fixtures\unkillable_spew.py
# Compiled at: 2015-07-18 10:13:57
import time, signal
signal.signal(signal.SIGTERM, signal.SIG_IGN)
counter = 0
while 1:
    time.sleep(0.01)
    print 'more spewage %s' % counter
    counter += 1