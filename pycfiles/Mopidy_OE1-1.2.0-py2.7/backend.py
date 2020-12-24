# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mopidy_oe1/backend.py
# Compiled at: 2017-06-07 16:19:53
from __future__ import unicode_literals
import logging
from mopidy import backend
import pykka
from mopidy_oe1.library import OE1LibraryProvider
from mopidy_oe1.playback import OE1PlaybackProvider
logger = logging.getLogger(__name__)

class OE1Backend(pykka.ThreadingActor, backend.Backend):

    def __init__(self, config, audio):
        super(OE1Backend, self).__init__()
        self.config = config
        self.library = OE1LibraryProvider(backend=self)
        self.playback = OE1PlaybackProvider(audio=audio, backend=self)
        self.uri_schemes = [b'oe1']

    def on_start(self):
        logger.info(b'Starting OE1Backend')

    def on_stop(self):
        pass