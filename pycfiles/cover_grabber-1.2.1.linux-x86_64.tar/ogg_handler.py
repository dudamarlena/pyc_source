# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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
                        return (
                         tags['album'][0], tags['artist'][0])
                        break
            except mutagen.oggvorbis.OggVorbisHeaderError:
                continue

        return (None, None)