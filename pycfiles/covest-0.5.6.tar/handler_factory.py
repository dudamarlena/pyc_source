# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/lib/python2.7/site-packages/cover_grabber/handler/handler_factory.py
# Compiled at: 2012-07-04 22:00:06
import os
from cover_grabber.handler.mp3_handler import MP3Handler
from cover_grabber.handler.ogg_handler import OGGHandler
from cover_grabber.handler.flac_handler import FLACHandler

class HandlerFactory(object):

    @staticmethod
    def get_handler(dirname, filenames):
        """ Factory method to return proper Handler subclass """
        for file in filenames:
            if '.mp3' in file:
                return MP3Handler(dirname, filenames)
            if '.ogg' in file:
                return OGGHandler(dirname, filenames)
            if '.flac' in file:
                return FLACHandler(dirname, filenames)

        return False