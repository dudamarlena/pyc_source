# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jstutters/.virtualenvs/pirec/lib/python3.6/site-packages/pirec/utils.py
# Compiled at: 2017-02-10 11:03:57
# Size of source mod 2**32: 347 bytes
"""Utility functions."""
import hashlib
BUF_SIZE = 65536

def file_sha1sum(filename):
    """Calculate the SHA-1 checksum of a file."""
    sha1 = hashlib.sha1()
    with open(filename, 'rb') as (f):
        data = f.read(BUF_SIZE)
        while data:
            sha1.update(data)
            data = f.read(BUF_SIZE)

    return sha1.hexdigest()