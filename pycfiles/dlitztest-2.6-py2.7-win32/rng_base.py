# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\Crypto\Random\OSRNG\rng_base.py
# Compiled at: 2013-03-13 13:15:35
__revision__ = '$Id$'
import sys
if sys.version_info[0] == 2 and sys.version_info[1] == 1:
    from Crypto.Util.py21compat import *

class BaseRNG(object):

    def __init__(self):
        self.closed = False
        self._selftest()

    def __del__(self):
        self.close()

    def _selftest(self):
        data = self.read(16)
        if len(data) != 16:
            raise AssertionError('read truncated')
        data2 = self.read(16)
        if data == data2:
            raise AssertionError('OS RNG returned duplicate data')

    def __enter__(self):
        pass

    def __exit__(self):
        """PEP 343 support"""
        self.close()

    def close(self):
        if not self.closed:
            self._close()
        self.closed = True

    def flush(self):
        pass

    def read(self, N=-1):
        """Return N bytes from the RNG."""
        if self.closed:
            raise ValueError('I/O operation on closed file')
        if not isinstance(N, (long, int)):
            raise TypeError('an integer is required')
        if N < 0:
            raise ValueError('cannot read to end of infinite stream')
        elif N == 0:
            return ''
        data = self._read(N)
        if len(data) != N:
            raise AssertionError('%s produced truncated output (requested %d, got %d)' % (self.name, N, len(data)))
        return data

    def _close(self):
        raise NotImplementedError('child class must implement this')

    def _read(self, N):
        raise NotImplementedError('child class must implement this')