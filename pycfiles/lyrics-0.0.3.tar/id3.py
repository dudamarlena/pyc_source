# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/david/source/lyrics/lyrics/id3.py
# Compiled at: 2013-01-28 20:28:56
import os, mutagen.mp3, threading, lyrics
from lyrics import database
from _compatibility import unicode

class Song(object):

    def __init__(self, path, use_cache=False):
        self.path = path
        self.use_cache = use_cache
        self.__id3 = None
        self.broken = False
        self._lyrics = None
        return

    def __repr__(self):
        if not self.artist:
            return unicode(self.file_name)
        return '<%s: %s - %s>' % (self.__class__.__name__, self.artist,
         self.song)

    @property
    def file_name(self):
        return os.path.basename(self.path)

    @property
    def file_name_no_extension(self):
        return self.file_name.rsplit(os.extsep, 1)

    @property
    def _id3(self):
        if self.__id3 is None:
            if self.use_cache:
                self.__id3 = database.ID3Cache.load(self.path)
            if self.__id3 is None:
                try:
                    self.__id3 = mutagen.File(self.path)
                except mutagen.mp3.HeaderNotFoundError:
                    self.__id3 = {}
                    self.broken = True
                else:
                    if self.use_cache and self.__id3 is not None:
                        database.ID3Cache.save(self.export())
        return self.__id3

    def _get_id3(self, *keys):
        if self._id3 is None:
            return ''
        else:
            for k in keys:
                result = self._id3.get(k, None)
                if result is not None:
                    break

            return unicode(result or '')

    @property
    def artist(self):
        return self._get_id3('TPE1', 'artist')

    @property
    def song(self):
        return self._get_id3('TIT2', 'song')

    @property
    def album(self):
        return self._get_id3('TALB', 'album')

    @property
    def year(self):
        return self._get_id3('TDRC', 'year')

    @property
    def track(self):
        return self._get_id3('TRCK', 'track')

    @property
    def genre(self):
        return self._get_id3('TCON', 'genre')

    def get_lyrics_thread(self, on_finish_callback):

        def run_in_thread():
            lyr = lyrics.get(self.artist, self.song, self.album)
            self._lyrics = lyr
            if on_finish_callback is not None:
                on_finish_callback(self, lyr)
            return

        thread = threading.Thread(target=run_in_thread)
        thread.daemon = True
        thread.start()
        return thread

    def export(self):
        """ export all useful id3 values """
        return dict(song=self.song, artist=self.artist, album=self.album, year=self.year, track=self.track, genre=self.genre, path=self.path)