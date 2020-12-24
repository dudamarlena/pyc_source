# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pympris/MediaPlayer.py
# Compiled at: 2013-12-10 15:49:59
"""
This module provides a `MediaPlayer` class
wich contains instances of all implementations of MPRIS2 interfaces.

Usage:

mp = MediaPlayer('org.mpris.MediaPlayer2.rhythmbox')
print mp.root.Identity
if mp.root.CanRaise:
    mp.root.Raise()

if mp.player.CanPause and mp.player.CanPlay:
    mp.player.PlayPause()
if mp.player.CanGoNext:
    mp.player.Next()

print mp.track_list.Tracks
print mp.playlists.GetPlaylists

if mp.root.CanQuit:
    mp.root.Quit()
"""
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