# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\chunkypandas\utilities\utilities.py
# Compiled at: 2019-12-23 17:32:45
# Size of source mod 2**32: 487 bytes
"""
utilities.py
written in Python3
author: C. Lockhart
"""
import atexit
from glob import iglob
import os
from tempfile import gettempdir

def clean():
    for file in iglob(os.path.join(gettempdir(), 'chunkypandas_*')):
        os.remove(file)


atexit.register(clean)

def get_named_tempfile():
    return os.path.join(gettempdir(), 'chunkypandas_' + os.urandom(24).hex() + '.csv')