# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: M:\Programming\Project\django-auth\auth\CustomAuth\decorators\timer.py
# Compiled at: 2019-12-10 17:11:23
# Size of source mod 2**32: 297 bytes
import time

def timeit(function):

    def timed(*args, **kwargs):
        ts = time.time()
        result = function(*args, **kwargs)
        te = time.time()
        print('%r (%r, %r) %2.2f sec' % (function.__name__, args, kwargs, te - ts))
        return result

    return timed