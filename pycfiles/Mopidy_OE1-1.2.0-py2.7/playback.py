# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mopidy_oe1/playback.py
# Compiled at: 2017-06-11 06:46:50
from __future__ import unicode_literals
import logging
from client import OE1Client
from mopidy import backend
from mopidy_oe1.library import InvalidOE1Uri, OE1LibraryUri, OE1UriType
logger = logging.getLogger(__name__)

class OE1PlaybackProvider(backend.PlaybackProvider):

    def __init__(self, audio, backend, client=OE1Client()):
        super(OE1PlaybackProvider, self).__init__(audio, backend)
        self.client = client

    def translate_uri(self, uri):
        try:
            library_uri = OE1LibraryUri.parse(uri)
        except InvalidOE1Uri:
            return

        if library_uri.uri_type == OE1UriType.LIVE:
            return OE1Client.LIVE
        else:
            if library_uri.uri_type == OE1UriType.CAMPUS:
                return OE1Client.CAMPUS
            if library_uri.uri_type == OE1UriType.ARCHIVE_ITEM:
                return self.client.get_item_url(library_uri.day_id, library_uri.item_id)
            return