# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n8f5s77x/tzutil/tzutil/retry.py
# Compiled at: 2018-12-04 01:36:04
# Size of source mod 2**32: 312 bytes
import traceback
from functools import wraps
from time import sleep

def retry(func):

    @wraps(func)
    def _(*args, **kwds):
        for i in range(3):
            try:
                return func(*args, **kwds)
            except:
                traceback.print_exc()
                sleep(1)

    return _