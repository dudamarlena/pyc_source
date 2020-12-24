# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nex/projects/snoopdroid/snoopdroid/utils.py
# Compiled at: 2020-04-03 08:08:14
# Size of source mod 2**32: 1019 bytes
import hashlib

def get_sha256(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, 'rb') as (handle):
        for byte_block in iter(lambda : handle.read(4096), ''):
            sha256_hash.update(byte_block)

    return sha256_hash.hexdigest()