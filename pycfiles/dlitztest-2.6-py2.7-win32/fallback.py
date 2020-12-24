# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\Crypto\Random\OSRNG\fallback.py
# Compiled at: 2013-03-13 13:15:35
__revision__ = '$Id$'
__all__ = ['PythonOSURandomRNG']
import os
from rng_base import BaseRNG

class PythonOSURandomRNG(BaseRNG):
    name = '<os.urandom>'

    def __init__(self):
        self._read = os.urandom
        BaseRNG.__init__(self)

    def _close(self):
        self._read = None
        return


def new(*args, **kwargs):
    return PythonOSURandomRNG(*args, **kwargs)