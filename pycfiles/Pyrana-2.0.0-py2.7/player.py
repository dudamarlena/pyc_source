# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyrana/player.py
# Compiled at: 2011-07-09 22:56:06
import pygst
pygst.require('0.10')
import gst

class PyranaPlayer(object):
    """ An abstraction layer on top of our actual music player. """

    def __init__(self, helper):
        self.helper = helper

    def start(self):
        self.player = gst.element_factory_make('playbin2', 'player')
        bus = self.player.get_bus()
        bus.add_signal_watch()
        bus.enable_sync_message_emission()
        bus.connect('message', self.on_message)

    def on_message(self, bus, msg):
        if msg.type == gst.MESSAGE_EOS:
            self.helper.end_of_song()
        elif msg.type == gst.MESSAGE_ERROR:
            raise Exception(msg)

    def stop(self):
        self.player.set_state(gst.STATE_NULL)

    @property
    def song(self):
        return self.song

    @song.setter
    def song(self, song):
        self.player.set_property('uri', 'file://%s' % song)

    def play(self):
        self.player.set_state(gst.STATE_PLAYING)

    def pause(self):
        self.player.set_state(gst.STATE_PAUSED)