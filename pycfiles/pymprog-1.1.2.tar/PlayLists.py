# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pympris/PlayLists.py
# Compiled at: 2013-12-10 15:49:59
__doc__ = "\nThis module provides a `PlayLists` class\nwich implemented MPRIS2 PlayLists interface:\nhttp://specifications.freedesktop.org/mpris-spec/latest/Playlists_Interface.html\n\nclass PlaylistOrdering uses as an enum for Ordering type.\n\npl = PlayLists('org.mpris.MediaPlayer2.rhythmbox')\nprint pl.PlaylistCount\nprint pl.ActivePlaylist\n\nitems = pl.GetPlaylists(0, 100, PlaylistOrdering.Alphabetical, reversed=False)\nfor uri, name, icon_uri in items:\n    print uri, name, icon_uri\n"
from .common import convert2dbus
from .Base import Base

class PlaylistOrdering(object):
    Alphabetical = 'Alphabetical'
    CreationDate = 'Created'
    ModifiedDate = 'Modified'
    LastPlayDate = 'Played'
    UserDefined = 'User'


class PlayLists(Base):
    """class implements methods and properties
    to working with MPRIS2 Playlists interface
    """
    IFACE = 'org.mpris.MediaPlayer2.Playlists'

    def __init__(self, name, bus=None, private=False):
        super(PlayLists, self).__init__(name, bus, private)

    def ActivatePlaylist(self, playlist_id):
        """Starts playing the given playlist.
        Parameters:
            playlist_id - The id of the playlist to activate.
        """
        self.iface.ActivatePlaylist(playlist_id)

    def GetPlaylists(self, start, max_count, order, reversed):
        """Gets a set of playlists.
        Parameters:
            start - The index of the first playlist to be fetched
                    (according to the ordering).
            max_count - The maximum number of playlists to fetch.
            order - The ordering that should be used.
            reversed - Whether the order should be reversed.

        """
        cv = convert2dbus
        return self.iface.GetPlaylists(cv(start, 'u'), cv(max_count, 'u'), cv(order, 's'), cv(reversed, 'b'))

    @property
    def PlaylistCount(self):
        """The number of playlists available."""
        return self.get('PlaylistCount')

    @property
    def Orderings(self):
        """The available orderings. At least one must be offered."""
        return self.get('Orderings')

    @property
    def ActivePlaylist(self):
        """The currently-active playlist."""
        valid, info = tuple(self.get('ActivePlaylist'))
        if valid:
            return info