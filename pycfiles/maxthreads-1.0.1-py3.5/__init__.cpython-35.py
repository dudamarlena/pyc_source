# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/maxthreads/__init__.py
# Compiled at: 2016-04-26 16:32:57
# Size of source mod 2**32: 172 bytes
from .maxthreads import MaxThreads
with open(__path__[0] + '/version', 'r') as (r):
    __version__ = r.read()
__all__ = ['MaxThreads', '__version__']