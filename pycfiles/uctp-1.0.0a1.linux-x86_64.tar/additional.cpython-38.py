# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.8/dist-packages/uctp/additional.py
# Compiled at: 2020-04-26 16:24:41
# Size of source mod 2**32: 286 bytes


def check_hash(hash_: str):
    if not isinstance(hash_, str) or len(hash_) != 40:
        raise TypeError('Hash must be SHA1 fingerprint of RSA key')
    else:
        pass
    try:
        bytearray.fromhex(hash_)
    except ValueError:
        raise ValueError('Wrong SHA1 hash')