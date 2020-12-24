# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/lib.linux-i686-2.6/m_lib/hash/zshelve.py
# Compiled at: 2016-07-25 10:38:46
"""Compressed shelves"""
from shelve import DbfilenameShelf
from zlib import compress, decompress
try:
    from cPickle import dumps, loads
except ImportError:
    from Pickle import dumps, loads

class CompressedShelf(DbfilenameShelf):
    """Shelf implementation using zlib for compressing data."""
    compress_level = 6

    def __getitem__(self, key):
        return loads(decompress(self.dict[key]))

    def __setitem__(self, key, value):
        self.dict[key] = compress(dumps(value), self.compress_level)


class CompressedKeysShelf(CompressedShelf):
    """CompressedShelf implementation that also compresses keys."""

    def keys(self):
        _keys = []
        for key in self.dict.keys():
            _keys.append(decompress(key))

        return _keys

    def has_key(self, key):
        return self.dict.has_key(compress(key, self.compress_level))

    def __getitem__(self, key):
        return CompressedShelf.__getitem__(self, compress(key, self.compress_level))

    def __setitem__(self, key, value):
        CompressedShelf.__setitem__(self, compress(key, self.compress_level), value)

    def __delitem__(self, key):
        del self.dict[compress(key, self.compress_level)]