# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/guessit/hash_ed2k.py
# Compiled at: 2013-03-18 16:30:48
from __future__ import unicode_literals
from guessit import s, to_hex
import hashlib, os.path

def hash_file(filename):
    """Returns the ed2k hash of a given file.

    >>> s(hash_file('tests/dummy.srt'))
    'ed2k://|file|dummy.srt|44|1CA0B9DED3473B926AA93A0A546138BB|/'
    """
    return b'ed2k://|file|%s|%d|%s|/' % (os.path.basename(filename),
     os.path.getsize(filename),
     hash_filehash(filename).upper())


def hash_filehash(filename):
    """Returns the ed2k hash of a given file.

    This function is taken from:
    http://www.radicand.org/blog/orz/2010/2/21/edonkey2000-hash-in-python/
    """
    md4 = hashlib.new(b'md4').copy

    def gen(f):
        while True:
            x = f.read(9728000)
            if x:
                yield x
            else:
                return

    def md4_hash(data):
        m = md4()
        m.update(data)
        return m

    with open(filename, b'rb') as (f):
        a = gen(f)
        hashes = [ md4_hash(data).digest() for data in a ]
        if len(hashes) == 1:
            return to_hex(hashes[0])
        return md4_hash(reduce(lambda a, d: a + d, hashes, b'')).hexd