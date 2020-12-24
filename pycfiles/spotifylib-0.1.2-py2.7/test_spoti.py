# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-intel/egg/spotifylib/test_spoti.py
# Compiled at: 2017-10-09 12:13:37
from spotifylib import Spotify
import os, logging
from pprint import pprint
logging.basicConfig(level=logging.DEBUG)
spotify = Spotify(client_id=os.environ.get('CLIENT_ID'), client_secret=os.environ.get('CLIENT_SECRET'), username=os.environ.get('USERNAME'), password=os.environ.get('PASSWORD'), callback=os.environ.get('CALLBACK_URL'), scope=os.environ.get('SCOPE'))
playlists = spotify.user_playlists(os.environ.get('USERNAME'))
for playlist in playlists.get('items'):
    pprint(spotify.user_playlist_tracks(user=os.environ.get('USERNAME'), playlist_id=playlist.get('id')))