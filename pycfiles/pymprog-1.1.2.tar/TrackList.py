# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pympris/TrackList.py
# Compiled at: 2013-12-10 15:49:59
__doc__ = "\nThis module provides a `TrackList` class\nwich implemented MPRIS2 TrackList interface:\nhttp://specifications.freedesktop.org/mpris-spec/latest/Track_List_Interface.html\n\nUsage:\n\ntl = TrackList('org.mpris.MediaPlayer2.vlc')\nprint tl.Tracks\ntl.RemoveTrack(tl.Tracks[2])\n\n"
from .common import convert2dbus
from .Base import Base

class TrackList(Base):
    """class implements methods and properties
    to working with MPRIS2 TrackList interface
    """
    IFACE = 'org.mpris.MediaPlayer2.TrackList'

    def __init__(self, name, bus=None, private=False):
        super(TrackList, self).__init__(name, bus, private)

    def GetTracksMetadata(self, track_ids):
        """Gets all the metadata available for a set of tracks.
        Parameters:
            track_ids - list of track ids

        Returns:
            Metadata of the set of tracks given as input.
        """
        return self.iface.GetTracksMetadata(convert2dbus(track_ids, 'ao'))

    def AddTrack(self, uri, after_track, set_as_current):
        u"""Adds a URI in the TrackList.
        Parameters:
            uri — The uri of the item to add.
            after_track — The identifier of the track
                          after which the new item should be inserted.
            set_as_current - Whether the newly inserted track
                             should be considered as the current track.
        """
        self.iface.AddTrack(uri, convert2dbus(after_track, 'o'), convert2dbus(set_as_current, 'b'))

    def RemoveTrack(self, track_id):
        """Removes an item from the TrackList.
        Parameters:
            track_id - Identifier of the track to be removed.
        """
        self.iface.RemoveTrack(convert2dbus(track_id, 'o'))

    def GoTo(self, track_id):
        """Skip to the specified TrackId.
        Parameters:
            track_id - Identifier of the track to skip to.
        """
        self.iface.GoTo(convert2dbus(track_id, 'o'))

    @property
    def Tracks(self):
        """Returns an list which contains the identifier of each track
        in the tracklist, in order."""
        return self.get('Tracks')

    @property
    def CanEditTracks(self):
        """If false, calling AddTrack or RemoveTrack will have no effect,
        and may raise a NotSupported error."""
        return self.get('CanEditTracks')