# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/zeta/tests/loopfetch.py
# Compiled at: 2010-07-15 08:55:39
import httplib, time
while 1:
    start = time.time()
    conn = httplib.HTTPConnection('sandbox.devwhiz.net')
    conn.request('GET', '/help/zwiki')
    print time.time() - start