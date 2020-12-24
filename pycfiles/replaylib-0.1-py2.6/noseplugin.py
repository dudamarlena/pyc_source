# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/replaylib/noseplugin.py
# Compiled at: 2010-06-14 06:18:09
import logging, os, replaylib
from nose.plugins import Plugin
log = logging.getLogger(__name__)

class ReplayLibPlugin(Plugin):
    enabled = False
    name = 'replaylib'
    score = 0

    def options(self, parser, env=os.environ):
        """Add options to nosetests."""
        parser.add_option('--%s-record' % self.name, action='store', metavar='FILE', dest='record_filename', help='Record actions to this file.')
        parser.add_option('--%s-playback' % self.name, action='store', metavar='FILE', dest='playback_filename', help='Playback actions from this file.')

    def configure(self, options, config):
        Plugin.configure(self, options, config)
        self.record_filename = options.record_filename
        self.playback_filename = options.playback_filename
        if self.record_filename or self.playback_filename:
            self.enabled = True

    def begin(self):
        if self.playback_filename:
            replaylib.start_playback(self.playback_filename)
        else:
            replaylib.start_record()

    def report(self, stream):
        if self.playback_filename:
            replaylib.stop_playback()
        else:
            replaylib.stop_record(self.record_filename)