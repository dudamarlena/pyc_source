# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\Crypto\Util\randpool.py
# Compiled at: 2013-03-13 13:15:35
__revision__ = '$Id$'
from Crypto.pct_warnings import RandomPool_DeprecationWarning
import Crypto.Random, warnings

class RandomPool:
    """Deprecated.  Use Random.new() instead.

    See http://www.pycrypto.org/randpool-broken
    """

    def __init__(self, numbytes=160, cipher=None, hash=None, file=None):
        warnings.warn('This application uses RandomPool, which is BROKEN in older releases.  See http://www.pycrypto.org/randpool-broken', RandomPool_DeprecationWarning)
        self.__rng = Crypto.Random.new()
        self.bytes = numbytes
        self.bits = self.bytes * 8
        self.entropy = self.bits

    def get_bytes(self, N):
        return self.__rng.read(N)

    def _updateEntropyEstimate(self, nbits):
        self.entropy += nbits
        if self.entropy < 0:
            self.entropy = 0
        elif self.entropy > self.bits:
            self.entropy = self.bits

    def _randomize(self, N=0, devname='/dev/urandom'):
        """Dummy _randomize() function"""
        self.__rng.flush()

    def randomize(self, N=0):
        """Dummy randomize() function"""
        self.__rng.flush()

    def stir(self, s=''):
        """Dummy stir() function"""
        self.__rng.flush()

    def stir_n(self, N=3):
        """Dummy stir_n() function"""
        self.__rng.flush()

    def add_event(self, s=''):
        """Dummy add_event() function"""
        self.__rng.flush()

    def getBytes(self, N):
        """Dummy getBytes() function"""
        return self.get_bytes(N)

    def addEvent(self, event, s=''):
        """Dummy addEvent() function"""
        return self.add_event()