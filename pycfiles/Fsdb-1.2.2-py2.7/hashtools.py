# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fsdb/hashtools.py
# Compiled at: 2016-03-24 13:25:59
import hashlib
from os import stat

def calc_file_digest(filePath, algorithm):
    try:
        block_size = stat(filePath).st_blksize
    except AttributeError:
        block_size = None

    with open(filePath, 'rb', block_size) as (f):
        digest = calc_digest(f, algorithm, block_size)
    return digest


def calc_digest(origin, algorithm='sha1', block_size=None):
    """Calculate digest of a readable object

     Args:
        origin -- a readable object for which calculate digest
        algorithn -- the algorithm to use. See ``hashlib.algorithms_available`` for supported algorithms.
        block_size -- the size of the block to read at each iteration
    """
    try:
        hashM = hashlib.new(algorithm)
    except ValueError:
        raise ValueError(('hash algorithm not supported by the underlying platform: "{0}"').format(algorithm))

    while True:
        chunk = origin.read(block_size) if block_size else origin.read()
        if not chunk:
            break
        hashM.update(chunk)

    return hashM.hexdigest()