# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/cover_grabber/handler/flac_handler.py
# Compiled at: 2012-07-05 18:18:49
import os, mutagen
from mutagen.flac import FLAC
from cover_grabber.handler.handler import Handler
from cover_grabber.logging.config import logger

class FLACHandler(Handler):

    def __init__(self, dirname, filenames):
        """ Initialize FLAC Handler """
        super(FLACHandler, self).__init__(dirname, filenames)
        self.audio_files = [ os.path.join(dirname, file) for file in filenames if '.flac' in file ]

    def get_album_and_artist(self):
        """ Return FLAC tags for album and artist"""
        self.audio_files.sort()
        for file in self.audio_files:
            try:
                tags = FLAC(file)
                if tags:
                    if 'album' in tags.keys() and 'artist' in tags.keys():
                        logger.debug(('album -> {album}, artist -> {artist}').format(album=tags['album'][0], artist=tags['artist'][0]))
                        return (tags['album'][0], tags['artist'][0])
                        break
            except mutagen.flac.FLACNoHeaderError:
                logger.error('No FLAC Header data')
                continue

        return (None, None)