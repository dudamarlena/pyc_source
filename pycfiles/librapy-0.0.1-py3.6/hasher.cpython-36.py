# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/librapy/lib/hasher.py
# Compiled at: 2019-09-01 21:32:55
# Size of source mod 2**32: 530 bytes
"""
Common hash wrapper for sha3 256. Libra prefixes / salts all hash objects,
first with the role of the hashing function, e.g. AccountAddress,
RawTransaction,  and second by Libra specific prefix, @@$$LIBRA$$@@..
"""
from hashlib import sha3_256
COMMON_HASH_PREFIX = b'@@$$LIBRA$$@@'

def get_hash_function(hashable_type):
    sha3 = sha3_256()
    sha3.update(hashable_type.get_hash_prefix() + COMMON_HASH_PREFIX)
    base = sha3.digest()
    sha3 = sha3_256()
    sha3.update(base)
    return sha3