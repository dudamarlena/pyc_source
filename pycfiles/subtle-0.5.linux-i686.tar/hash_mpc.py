# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/guessit/hash_mpc.py
# Compiled at: 2013-03-18 16:30:48
from __future__ import unicode_literals
import struct, os

def hash_file(filename):
    """This function is taken from:
    http://trac.opensubtitles.org/projects/opensubtitles/wiki/HashSourceCodes
    and is licensed under the GPL."""
    longlongformat = b'q'
    bytesize = struct.calcsize(longlongformat)
    f = open(filename, b'rb')
    filesize = os.path.getsize(filename)
    hash_value = filesize
    if filesize < 131072:
        raise Exception(b'SizeError: size is %d, should be > 132K...' % filesize)
    for x in range(65536 / bytesize):
        buf = f.read(bytesize)
        l_value, = struct.unpack(longlongformat, buf)
        hash_value += l_value
        hash_value = hash_value & 18446744073709551615

    f.seek(max(0, filesize - 65536), 0)
    for x in range(65536 / bytesize):
        buf = f.read(bytesize)
        l_value, = struct.unpack(longlongformat, buf)
        hash_value += l_value
        hash_value = hash_value & 18446744073709551615

    f.close()
    return b'%016x' % hash_value