# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./build/lib/supervisor/tests/fixtures/unkillable_spew.py
# Compiled at: 2019-04-05 17:19:18
# Size of source mod 2**32: 186 bytes
import time, signal
signal.signal(signal.SIGTERM, signal.SIG_IGN)
counter = 0
while True:
    time.sleep(0.01)
    print('more spewage %s' % counter)
    counter += 1