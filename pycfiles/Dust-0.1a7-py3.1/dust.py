# uncompyle6 version 3.7.4
# Python bytecode 3.1 (3151)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/dust/crypto/dust.py
# Compiled at: 2010-06-01 14:59:30
import random, struct
from dust.crypto import skeinUtil
SEED_SIZE = 16
IV_SIZE = 16
BLOCK_SIZE = 32
PBKDF_ITERATIONS = 13000
MAC_PERS = b'1978-10-26 dust@blanu.net Dust/MAC'
PRNG_PERS = b'1978-10-26 dust@blanu.net Dust/PRNG'
HASH_PERS = b'1978-10-26 dust@blanu.net Dust/hash'
PBKDF_PERS = b'1978-10-26 dust@blanu.net Dust/PBKDF'
CIPHER_PERS = b'1978-10-26 dust@blanu.net Dust/cipher'

def hash(data):
    return skeinUtil.hash(data, digest_bits=256, pers=HASH_PERS)


def mac(key, data):
    return skeinUtil.hash(data, digest_bits=256, mac=key, pers=MAC_PERS)


def pbkdf(pb, salt):
    return skeinUtil.pbkdf(pb, salt, PBKDF_ITERATIONS, pers=PBKDF_PERS)


class DustPRNG(skeinUtil.SkeinPRNG):

    def __init__(self):
        skeinUtil.SkeinPRNG.__init__(self, pers=PRNG_PERS)


def encrypt(k, iv, data):
    cipher = DustCipher(k, iv)
    return cipher.encrypt(data)


def decrypt(k, iv, data):
    cipher = DustCipher(k, iv)
    return cipher.decrypt(data)


class DustCipher(skeinUtil.SkeinCipherOFB):

    def __init__(self, key, iv):
        skeinUtil.SkeinCipherOFB.__init__(self, key, iv, pers=CIPHER_PERS)