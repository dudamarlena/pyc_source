# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pympris/MediaPlayer.py
# Compiled at: 2013-12-10 15:49:59
__doc__ = "\nThis module provides a `MediaPlayer` class\nwich contains instances of all implementations of MPRIS2 interfaces.\n\nUsage:\n\nmp = MediaPlayer('org.mpris.MediaPlayer2.rhythmbox')\nprint mp.root.Identity\nif mp.root.CanRaise:\n    mp.root.Raise()\n\nif mp.player.CanPause and mp.player.CanPlay:\n    mp.player.PlayPause()\nif mp.player.CanGoNext:\n    mp.player.Next()\n\nprint mp.track_list.Tracks\nprint mp.playlists.GetPlaylists\n\nif mp.root.CanQuit:\n    mp.root.Quit()\n"
from .Root import Root
from .Player import Player
from .PlayLists import PlayLists
from .TrackList import TrackList

class MediaPlayer(object):
    """Class uses as helper class."""

    def __init__(self, dbus_name, bus=None, private=False):
        super(MediaPlayer, self).__init__()
        self.root = Root(dbus_name, bus, private)
        self.player = Player(dbus_name, bus, private)
        self.playlists = PlayLists(dbus_name, bus, private)
        self.track_list = TrackList(dbus_name, bus, private)