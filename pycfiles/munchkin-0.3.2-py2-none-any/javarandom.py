# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/gszathmari/munchkin/munchkin/lib/passwordcard/javarandom.py
# Compiled at: 2016-05-02 03:44:35
import threading, time

class JavaRandom(object):
    """A partial implementation of a java-compatible random number generator"""

    def __init__(self, seed=None):
        if seed is None:
            seed = int(time.time() * 1000)
        self.seed = seed
        self.lock = threading.Lock()
        return

    @property
    def seed(self):
        return self._seed

    @seed.setter
    def seed(self, seed):
        self._seed = (seed ^ 25214903917) & 281474976710655

    def next(self, bits):
        """Return `bits` random bits as a signed 32 bits integer"""
        with self.lock:
            self._seed = self._seed * 25214903917 + 11 & 281474976710655
            ret = self._seed >> 48 - bits
            if ret & 2147483648:
                ret -= 4294967296
            return ret

    def next_int(self, maxint=None):
        """Return an integer evenly distributed between 0 and maxint-1"""
        if maxint is None:
            return self.next(32)
        else:
            if maxint <= 0 or maxint > 2147483647:
                raise ValueError('maxint needs to be in range 1 - 2^31-1')
            if maxint & -maxint == maxint:
                return maxint * self.next(31) >> 31
            bits = self.next(31)
            val = bits % maxint
            while bits - val + maxint - 1 & 2147483648:
                bits = self.next(31)
                val = bits % maxint

            return val

    def shuffle(self, list):
        """Shuffle the list given in the argument, using the algorithm from java.collections"""
        for i in reversed(range(2, len(list) + 1)):
            rnd = self.next_int(i)
            list[i - 1], list[rnd] = list[rnd], list[(i - 1)]