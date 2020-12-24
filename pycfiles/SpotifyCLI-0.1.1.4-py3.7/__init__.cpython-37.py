# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/SpotifyCLI/__init__.py
# Compiled at: 2019-01-27 12:27:59
# Size of source mod 2**32: 4729 bytes
import sys, spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
import spotipy.client as client
import os
from os.path import expanduser

def get_artist(name):
    results = sp.search(q=('artist:' + name), type='artist')
    items = results['artists']['items']
    if len(items) > 0:
        return items[0]
    return


def get_album_uri(name):
    albums = []
    uris = []
    results = sp.search(q=name, limit=10, type='album')
    items = results['albums'].get('items')
    for count in range(0, len(items)):
        uris.append(items[count]['uri'])
        artist = results['albums'].get('items')[count].get('artists')[0].get('name')
        print('(' + str(count) + ') ' + items[count]['name'] + ': ' + artist)

    selection = int(input('Selection: '))
    selectedURI = uris[selection]
    sp.start_playback(context_uri=(get_uri_from_album(selectedURI)))


def show_artist_albums(artist):
    albums = []
    uris = []
    results = sp.artist_albums((artist['id']), album_type='album')
    albums.extend(results['items'])
    while results['next']:
        results = sp.next(results)
        albums.extend(results['items'])

    seen = set()
    albums.sort(key=(lambda album: album['name'].lower()))
    count = 0
    for album in albums:
        name = album['name']
        if name not in seen:
            print('(' + str(count) + ') ' + name)
            uris.append(album['uri'])
            count += 1
        seen.add(name)

    selection = int(input('Selection: '))
    selectedURI = uris[selection]
    sp.start_playback(context_uri=(get_uri_from_album(selectedURI)))


def get_uri_from_album(albumuri):
    ourAlbum = sp.album(albumuri)
    return ourAlbum.get('uri')


def get_uri_from_track(track_uri):
    ourTrack = sp.track(track_uri)
    return ourTrack.get('uri')


def show_arist_songs(artist):
    songs = []
    uris = []
    results = sp.artist_top_tracks(artist['id'])
    for count in range(1, 10):
        songs.append(results['tracks'][count]['name'])
        uris.append(results['tracks'][count]['uri'])

    count = 0
    for song in songs:
        print('(' + str(count) + ') ' + song)
        count += 1

    selection = int(input('Selection: '))
    selectedURI = uris[selection]
    ourID = get_uri_from_track(selectedURI)
    sp.start_playback(uris=[ourID])


def search_songs(query):
    songs = []
    uris = []
    artists = []
    results = sp.search(query, limit=10)
    for count in range(0, len(results['tracks']['items'])):
        artists.append(results['tracks']['items'][count]['artists'][0]['name'])
        songs.append(results['tracks']['items'][count]['name'])
        uris.append(results['tracks']['items'][count]['uri'])

    count = 0
    for song in songs:
        print('(' + str(count) + ') ' + song + ': ' + artists[count])
        count += 1

    selection = int(input('Selection: '))
    selectedURI = uris[selection]
    ourID = get_uri_from_track(selectedURI)
    sp.start_playback(uris=[ourID])


ourClientID = os.environ['SpotifyClientID']
ourSecret = os.environ['SpotifyClientSecret']
ourUsername = os.environ['SpotifyUsername']
if (ourClientID == '') | (ourSecret == '') | (ourUsername == ''):
    print('Error: SpotifyClientID, SpotifyClientSecret, and SpotifyUsername need to be set in path')
    sys.exit()
else:
    scope = 'user-modify-playback-state user-read-playback-state'
    cachePath = expanduser('~/.spotify/cache')
    token = util.prompt_for_user_token(ourUsername, scope, client_id=ourClientID, client_secret=ourSecret,
      redirect_uri='http://localhost/',
      cache_path=cachePath)
    sp = spotipy.Spotify(auth=token)
    if len(sys.argv) < 2:
        print('Usage: {0} artist name'.format(sys.argv[0]))
    else:
        if sys.argv[1] == '-aa':
            name = ' '.join(sys.argv[2:])
            artist = get_artist(name)
            if artist:
                show_artist_albums(artist)
            else:
                print("Can't find that artist")
        else:
            if sys.argv[1] == '-album':
                name = ' '.join(sys.argv[2:])
                albums = get_album_uri(name)
            else:
                if sys.argv[1] == '-ff':
                    sp.next_track()
                else:
                    if sys.argv[1] == '-b':
                        sp.previous_track()
                    else:
                        if sys.argv[1] == '-p':
                            if sp.current_playback()['is_playing']:
                                sp.pause_playback()
                            else:
                                sp.start_playback()
                        else:
                            if sys.argv[1] == '-artist':
                                name = ' '.join(sys.argv[2:])
                                artist = get_artist(name)
                                show_arist_songs(artist)
                            else:
                                if sys.argv[1] == '-song':
                                    name = ' '.join(sys.argv[2:])
                                    search_songs(name)