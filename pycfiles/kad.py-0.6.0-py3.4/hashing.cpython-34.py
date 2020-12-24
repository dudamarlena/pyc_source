# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/kad/hashing.py
# Compiled at: 2017-12-29 11:36:17
# Size of source mod 2**32: 253 bytes
import hashlib, random
id_bits = 128

def hash_function(data):
    return int(hashlib.md5(data.encode('ascii')).hexdigest(), 16)


def random_id(seed=None):
    if seed:
        random.seed(seed)
    return random.randint(0, 2 ** id_bits - 1)