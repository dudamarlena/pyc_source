# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fixture/test/conf.py
# Compiled at: 2017-10-02 03:31:12
# Size of source mod 2**32: 371 bytes
from fixture import TempIO
import os
LITE_DSN = os.environ.get('FIXTURE_TEST_LITE_DSN', 'sqlite:///:memory:')
HEAVY_DSN = os.environ.get('FIXTURE_TEST_HEAVY_DSN', None)
HEAVY_DSN_IS_TEMPIO = False

def reset_heavy_dsn():
    global HEAVY_DSN
    if HEAVY_DSN_IS_TEMPIO:
        tmp = TempIO(deferred=True)
        HEAVY_DSN = 'sqlite:///%s' % tmp.join('tmp.db')