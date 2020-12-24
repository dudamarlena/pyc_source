# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/postlund/pyatv_dev/pyatv/pyatv/mrp/chacha20.py
# Compiled at: 2019-09-26 00:19:20
# Size of source mod 2**32: 1260 bytes
"""Transparent encryption layer using Chacha20_Pooly1305."""
from tlslite.utils.chacha20_poly1305 import CHACHA20_POLY1305

class Chacha20Cipher:
    __doc__ = 'CHACHA20 encryption/decryption layer.'

    def __init__(self, out_key, in_key):
        """Initialize a new Chacha20Cipher."""
        self._enc_out = CHACHA20_POLY1305(out_key, 'python')
        self._enc_in = CHACHA20_POLY1305(in_key, 'python')
        self._out_counter = 0
        self._in_counter = 0

    def encrypt(self, data, nounce=None):
        """Encrypt data with counter or specified nounce."""
        if nounce is None:
            nounce = self._out_counter.to_bytes(length=8, byteorder='little')
            self._out_counter += 1
        return self._enc_out.seal(b'\x00\x00\x00\x00' + nounce, data, bytes())

    def decrypt(self, data, nounce=None):
        """Decrypt data with counter or specified nounce."""
        if nounce is None:
            nounce = self._in_counter.to_bytes(length=8, byteorder='little')
            self._in_counter += 1
        decrypted = self._enc_in.open(b'\x00\x00\x00\x00' + nounce, data, bytes())
        if not decrypted:
            raise Exception('data decrypt failed')
        return bytes(decrypted)