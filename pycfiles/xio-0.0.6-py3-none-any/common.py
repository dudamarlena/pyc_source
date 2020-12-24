# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /apps/xio/core/lib/crypto/common.py
# Compiled at: 2018-12-07 08:05:33
from xio.core.lib.utils import is_int, is_string, str_to_bytes, decode_hex, encode_hex, to_string
import uuid, nacl.hash

def sha256(x):
    return nacl.hash.sha256(x)


sha3_keccak_256 = None
try:
    from Crypto.Hash import keccak

    def sha3_keccak_256(x):
        x = str_to_bytes(x)
        h = keccak.new(digest_bits=256, data=x).hexdigest()
        return str_to_bytes(h)


except ImportError:
    try:
        import sha3 as _sha3

        def sha3_keccak_256(x):
            x = str_to_bytes(x)
            h = _sha3.keccak_256(x).hexdigest()
            return str_to_bytes(h)


    except:
        pass

assert sha3_keccak_256