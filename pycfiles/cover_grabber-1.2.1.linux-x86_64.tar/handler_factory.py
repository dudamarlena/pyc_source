# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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