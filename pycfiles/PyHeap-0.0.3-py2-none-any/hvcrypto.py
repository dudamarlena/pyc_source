# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/healthvaultlib/hvcrypto.py
# Compiled at: 2015-12-15 14:36:17
import base64, hashlib
from Crypto.PublicKey import RSA
from binascii import a2b_hex, b2a_hex

class HVCrypto(object):

    def __init__(self, public_key, private_key):
        self.em = None
        self.private_key = None
        public_key_long = long(public_key, 16)
        private_key_long = long(private_key, 16)
        rsa_n_bit_length = 2048
        self.em = (rsa_n_bit_length + 7) / 8
        exponent = long(65537)
        self.private_key = RSA.construct((public_key_long,
         exponent,
         private_key_long))
        return

    def i2osp(self, long_integer, block_size):
        """Convert a long integer into an octet string."""
        hex_string = '%X' % long_integer
        if len(hex_string) > 2 * block_size:
            raise ValueError('integer %i too large to encode in %i octets' % (long_integer, block_size))
        return a2b_hex(hex_string.zfill(2 * block_size))

    def os2ip(self, octet_string):
        """Convert an octet string to a long integer."""
        return long(b2a_hex(octet_string), 16)

    def pad_rsa(self, hashed_msg):
        prefix = '0!0\t\x06\x05+\x0e\x03\x02\x1a\x05\x00\x04\x14'
        padlen = self.em - len(prefix) - len(hashed_msg) - 3
        padding = ('').join([ b'\xff' for x in range(padlen) ])
        pad_result = ('').join(['\x00\x01', padding, '\x00', prefix, hashed_msg])
        return pad_result

    def sign(self, data2sign):
        hashed_msg = hashlib.sha1(data2sign).digest()
        pad_result = self.pad_rsa(hashed_msg)
        sig = self.private_key.sign(self.os2ip(pad_result), None)[0]
        bsig = base64.encodestring(self.i2osp(sig, self.em))
        return bsig