# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\chunkypandas\utilities\utilities.py
# Compiled at: 2019-12-23 17:32:45
# Size of source mod 2**32: 487 bytes
__doc__ = '\nutilities.py\nwritten in Python3\nauthor: C. Lockhart\n'
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