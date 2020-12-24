# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/thirdparty_libs/dns/entropy.py
# Compiled at: 2013-08-26 10:52:44
import os, time
try:
    import threading as _threading
except ImportError:
    import dummy_threading as _threading

class EntropyPool(object):

    def __init__(self, seed=None):
        self.pool_index = 0
        self.digest = None
        self.next_byte = 0
        self.lock = _threading.Lock()
        try:
            import hashlib
            self.hash = hashlib.sha1()
            self.hash_len = 20
        except:
            try:
                import sha
                self.hash = sha.new()
                self.hash_len = 20
            except:
                import md5
                self.hash = md5.new()
                self.hash_len = 16

        self.pool = '\x00' * self.hash_len
        if seed is not None:
            self.stir(seed)
            self.seeded = True
        else:
            self.seeded = False
        return

    def stir(self, entropy, already_locked=False):
        if not already_locked:
            self.lock.acquire()
        try:
            bytes = [ ord(c) for c in self.pool ]
            for c in entropy:
                if self.pool_index == self.hash_len:
                    self.pool_index = 0
                b = ord(c) & 255
                bytes[self.pool_index] ^= b
                self.pool_index += 1

            self.pool = ('').join([ chr(c) for c in bytes ])
        finally:
            if not already_locked:
                self.lock.release()

    def _maybe_seed(self):
        if not self.seeded:
            try:
                seed = os.urandom(16)
            except:
                try:
                    r = file('/dev/urandom', 'r', 0)
                    try:
                        seed = r.read(16)
                    finally:
                        r.close()

                except:
                    seed = str(time.time())

            self.seeded = True
            self.stir(seed, True)

    def random_8(self):
        self.lock.acquire()
        self._maybe_seed()
        try:
            if self.digest is None or self.next_byte == self.hash_len:
                self.hash.update(self.pool)
                self.digest = self.hash.digest()
                self.stir(self.digest, True)
                self.next_byte = 0
            value = ord(self.digest[self.next_byte])
            self.next_byte += 1
        finally:
            self.lock.release()

        return value

    def random_16(self):
        return self.random_8() * 256 + self.random_8()

    def random_32(self):
        return self.random_16() * 65536 + self.random_16()

    def random_between(self, first, last):
        size = last - first + 1
        if size > 4294967296:
            raise ValueError('too big')
        if size > 65536:
            rand = self.random_32
            max = 4294967295
        elif size > 256:
            rand = self.random_16
            max = 65535
        else:
            rand = self.random_8
            max = 255
        return first + size * rand() // (max + 1)


pool = EntropyPool()

def random_16():
    return pool.random_16()


def between(first, last):
    return pool.random_between(first, last)