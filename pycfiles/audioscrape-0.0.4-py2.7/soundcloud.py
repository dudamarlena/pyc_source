# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/audioscrape/soundcloud.py
# Compiled at: 2016-12-05 03:11:37
"""Search SoundCloud playlists for audio."""
from __future__ import absolute_import
import os, string, sys, requests, soundcloud
from tqdm import tqdm

def sanitize(s):
    return ('').join(c for c in s if c in ('-_.() {}{}').format(string.ascii_letters, string.digits))


if 'SOUNDCLOUD_API_KEY' in os.environ:
    API_KEY = os.environ['SOUNDCLOUD_API_KEY']
else:
    API_KEY = '81f430860ad96d8170e3bf1639d4e072'

def scrape(query, include, exclude, quiet, overwrite):
    """Search SoundCloud and download audio from discovered playlists."""
    client = soundcloud.Client(client_id=API_KEY)

    def pagination(x):
        yield x
        while x.next_href:
            x = client.get(x.next_href)
            yield x

    for playlists in pagination(client.get('/playlists', q=query, tags=(',').join(include) if include else '', linked_partitioning=1, representation='compact')):
        for playlist in playlists.collection:
            haystack = (playlist.title + (' ' + playlist.description if playlist.description else '')).lower()
            if any(needle in haystack for needle in exclude):
                continue
            directory = sanitize(playlist.title)
            if directory == '':
                continue
            if not os.path.exists(directory):
                os.mkdir(directory)
            for track in client.get(playlist.tracks_uri):
                file = os.path.join(directory, sanitize(track.title) + '.mp3')
                if os.path.exists(file) and not overwrite:
                    continue
                if not track.streamable:
                    continue
                haystack = (track.title + ' ' + track.description + ' ' + track.tag_list).lower()
                if any(needle in haystack for needle in exclude):
                    continue
                r = requests.get(client.get(track.stream_url, allow_redirects=False).location, stream=True)
                total_size = int(r.headers['content-length'])
                chunk_size = 1000000
                with open(file, 'wb') as (f):
                    for data in tqdm(r.iter_content(chunk_size), desc=track.title, total=total_size / chunk_size, unit='MB', file=sys.stdout):
                        f.write(data)