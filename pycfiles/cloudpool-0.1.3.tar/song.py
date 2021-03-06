# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cloudplaya/song.py
# Compiled at: 2012-07-10 05:09:37


class Song(object):
    COLUMNS = [
     'albumArtistName', 'albumName', 'artistName', 'assetType',
     'duration', 'objectId', 'sortAlbumArtistName', 'sortAlbumName',
     'sortArtistName', 'title', 'status', 'trackStatus', 'extension',
     'asin', 'trackNum', 'discNum', 'albumReleaseDate']

    def __init__(self, client, payload):
        self.client = client
        metadata = payload['metadata']
        self.id = metadata['objectId']
        self.asset_type = metadata['assetType']
        self.title = metadata['title']
        self.asin = metadata.get('asin', None)
        self.status = metadata['status']
        self.duration = metadata['duration']
        self.extension = metadata['extension']
        self.album_name = metadata['albumName']
        self.album_release_date = metadata.get('albumReleaseDate', None)
        self.artist_name = metadata['artistName']
        self.album_artist_name = metadata['albumArtistName']
        self.track_num = int(metadata.get('trackNum', 0))
        self.disc_num = int(metadata.get('discNum', 0))
        self.sort_album_artist_name = metadata['sortAlbumArtistName']
        self.sort_album_name = metadata['sortAlbumName']
        return

    def get_stream_url(self):
        return self.client.get_song_stream_urls([self.id])[0]

    def __repr__(self):
        return '<Song "%s">' % self.title

    def __str__(self):
        return self.title