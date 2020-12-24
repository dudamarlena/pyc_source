# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/lib/python2.7/site-packages/cover_grabber/handler/handler.py
# Compiled at: 2012-07-05 18:18:49
import os

class Handler(object):

    def __init__(self, dirname, filenames):
        """ Initialize Handler """
        self.dirname = dirname
        self.filenames = filenames
        self.audio_files = [ os.path.join(dirname, file) for file in filenames ]

    def get_album_and_artist(self):
        """ Return tags for album and artist"""
        pass