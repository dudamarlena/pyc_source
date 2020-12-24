# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyrana/players/pygstplayer.py
# Compiled at: 2011-07-09 22:56:18
import pygst
pygst.require('0.10')
import gst, gobject
from feather import Plugin

class PyGSTPlayer(Plugin):
    """A player based on gstreamer"""
    listeners = set(['songloaded', 'pause', 'skipsong', 'skipalbum'])
    messengers = set(['songstart', 'songpause', 'songend', 'songresume'])
    name = 'PyGSTPlayer'

    def pre_run(self):
        gobject.threads_init()
        self.player = gst.element_factory_make('playbin2', 'player')
        fakesink = gst.element_factory_make('fakesink', 'fakesink')
        self.player.connect('about-to-finish', self.on_eos)
        self.player.set_property('video-sink', fakesink)
        self.playing = False

    def on_eos(self, bus=None, msg=None):
        self.send('songend')

    def stop(self, payload=None):
        self.player.set_state(gst.STATE_NULL)
        self.player.set_state(gst.STATE_READY)
        self.playing = False

    skipsong = stop
    skipalbum = stop

    def songloaded(self, songpath):
        self.stop()
        self.player.set_property('uri', 'file://%s' % songpath)
        self.player.set_state(gst.STATE_PLAYING)
        self.playing = True
        self.send('songstart', songpath)

    def pause(self, payload):
        if self.playing:
            self.player.set_state(gst.STATE_PAUSED)
            self.playing = False
            self.send('songpause')
        else:
            self.player.set_state(gst.STATE_PLAYING)
            self.playing = True
            self.send('songresume')