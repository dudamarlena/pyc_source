# uncompyle6 version 3.7.4
# Python bytecode 3.1 (3151)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/dust/crypto/skeinUtil.py
# Compiled at: 2010-06-01 14:58:21
import random, struct
from dust.crypto.pyskein import skein512
from dust.core.util import splitFields, splitField, xor, encode
SEED_SIZE = 16
BLOCK_SIZE = 32

def hash(data, digest_bits=512, mac=None, pers=None):
    if pers:
        if mac:
            return skein512(data, pers=pers, digest_bits=digest_bits)
        else:
            return skein512(data, pers=pers, digest_bits=digest_bits)
    else:
        if mac:
            return skein512(data, digest_bits=digest_bits)
        else:
            return skein512(data, digest_bits=digest_bits)


def pbkdf(pb, salt, i, pers=None, digest_bits=256):
    data = (pb.encode('ascii') + salt) * i
    if pers:
        return skein512(data, pers=pers, digest_bits=digest_bits)
    else:
        return skein512(data, digest_bits=digest_bits)


class SkeinPRNG:

    def __init__(self, seed=None, pers=None):
        if seed:
            self.seed = seed
        else:
            self.seed = self.generateSeed()
        self.pers = pers

    def generateSeed(self):
        return bytes(random.randint(0, 255) for _ in range(SEED_SIZE))

    def reseed(self, seed):
        if self.pers:
            self.seed = skein512(self.seed + seed, pers=self.pers, digest_bits=SEED_SIZE * 8)
        else:
            self.seed = skein512(self.seed + seed, digest_bits=SEED_SIZE * 8)

    def getBytes(self, n):
        if self.pers:
            result = skein512(self.seed, pers=self.pers, digest_bits=(SEED_SIZE + n) * 8)
        else:
            result = skein512(self.seed, digest_bits=(SEED_SIZE + n) * 8)
        self.seed, r = splitFields(result, [SEED_SIZE, n])
        return r

    def getInt(self, max=None):
        bs = self.getBytes(4)
        i = struct.unpack('I', bs)[0]
        if max:
            return i % max
        else:
            return i


def encrypt(k, iv, data):
    cipher = SkeinCipherOFB(k, iv)
    return cipher.encrypt(data)


def decrypt(k, iv, data):
    cipher = SkeinCipherOFB(k, iv)
    return cipher.decrypt(data)


class SkeinCipherOFB:

    def __init__(self, key, iv, pers=None):
        self.key = key
        self.iv = iv
        self.entropy = b''
        self.pers = pers

    def getBytes(self, n):
        while len(self.entropy) < n:
            if self.pers:
                result = skein512(self.iv, mac=self.key, pers=self.pers, digest_bits=BLOCK_SIZE * 8)
            else:
                result = skein512(self.iv, mac=self.key, digest_bits=BLOCK_SIZE * 8)
            self.entropy = self.entropy + result
            self.iv = result

        b, self.entropy = splitField(self.entropy, n)
        return b

    def encrypt(self, data):
        l = len(data)
        entropy = self.getBytes(l)
        return xor(data, entropy)

    def decrypt(self, data):
        return self.encrypt(data)