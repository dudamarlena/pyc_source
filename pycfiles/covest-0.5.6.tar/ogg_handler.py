# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/lib/python2.7/site-packages/cover_grabber/ogg_handler.py
# Compiled at: 2012-07-03 20:53:30
import os, mutagen
from mutagen.oggvorbis import OggVorbis

class OGGHandler(object):

    def __init__(self, dirname, filenames):
        """ Initialize OggVorbis Handler """
        self.dirname = dirname
        self.filenames = filenames
        self.audio_files = [ os.path.join(dirname, file) for file in filenames if '.ogg' in file ]

    def get_album_and_artist(self):
        """ Return Ogg tags for album and artist"""
        self.audio_files.sort()
        for file in self.audio_files:
            try:
                tags = OggVorbis(file)
                if tags:
                    if 'album' in tags.keys() and 'artist' in tags.keys():
                        return (tags['album'][0], tags['artist'][0])
                        break
            except mutagen.oggvorbis.OggVorbisHeaderError:
                continue

        return (None, None)