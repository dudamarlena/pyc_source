# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mop/core.py
# Compiled at: 2020-03-28 19:12:32
# Size of source mod 2**32: 527 bytes
from eyed3.id3 import GenreMap, Genre
__all__ = ['Genre', 'GENRES']

class Genres(GenreMap):
    _next_gid = GenreMap.GENRE_ID3V1_MAX + 1

    def __init__(self, *args):
        (super().__init__)(*args)

    def add(self, name) -> Genre:
        if name in self:
            raise ValueError(f"Genre exists: {name}")
        assert self._next_gid not in self
        gid = self._next_gid
        self._next_gid += 1
        self[gid] = name
        self[name.lower()] = gid
        return self.get(gid)


GENRES = Genres()