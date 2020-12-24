# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/david/source/lyrics/lyrics/__init__.py
# Compiled at: 2013-02-11 17:44:32
""" lyrics -- Lyrics fetcher & console music player. """
version_info = (0, 0, 3)
__version__ = version = ('.').join(map(str, version_info))
__project__ = __name__
__author__ = 'David Halter'
__license__ = 'GPL 3'
import database, fetcher, id3

def get(artist, song, album=None):
    """Fetch the lyrics as text."""
    info = (
     artist, song, album or '')
    try:
        return database.load(*info)
    except LookupError:
        return fetcher.fetch(*info)


def from_file(path, use_id3_cache=False):
    song = id3.Song(path, use_id3_cache)
    if song.artist and song.song:
        args = (
         song.artist, song.song, song.album)
    else:
        args = (
         '', song.file_name_no_extension, '')
    return get(*args)