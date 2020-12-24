# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/playlist/tests.py
# Compiled at: 2011-01-05 07:28:06
import unittest
from datetime import datetime, timedelta
from panya.models import ModelBase
from playlist.models import Playlist, PlaylistEntry, ScheduledPlaylist

class ScheduledPlaylistTestCase(unittest.TestCase):

    def test_get_playlist_entry_for(self):
        playlist = Playlist.objects.create(title='test playlist', state='published')
        content = ModelBase.objects.create(title='test content', state='published')
        self.failIf(ScheduledPlaylist.get_current_playlist_entry_for(content))
        scheduled_playlist = ScheduledPlaylist.objects.create(playlist=playlist, content=content, start=datetime.now(), end=datetime.now() + timedelta(days=10))
        self.failIf(ScheduledPlaylist.get_current_playlist_entry_for(content))
        playlist_entry = PlaylistEntry.objects.create(title='test playlistentry', playlist=playlist, start=datetime.now() - timedelta(days=1), end=datetime.now() + timedelta(days=1))
        self.failUnless(ScheduledPlaylist.get_current_playlist_entry_for(content) == playlist_entry)
        playlist_entry = PlaylistEntry.objects.create(title='test playlistentry', playlist=playlist, start=datetime.now() + timedelta(days=1), end=datetime.now() + timedelta(days=2))
        self.failUnless(ScheduledPlaylist.get_next_playlist_entry_for(content) == playlist_entry)