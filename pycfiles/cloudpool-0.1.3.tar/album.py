# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cloudplaya/album.py
# Compiled at: 2012-07-10 04:50:32


class Album(object):
    COLUMNS = [
     'albumArtistName', 'albumName', 'artistName', 'objectId',
     'primaryGenre', 'sortAlbumArtistName', 'sortAlbumName',
     'sortArtistName', 'albumCoverImageMedium', 'albumAsin',
     'artistAsin', 'gracenoteId', 'albumReleaseDate']

    def __init__(self, client, payload):
        self.client = client
        metadata = payload['metadata']
        self.id = metadata['objectId']
        self.name = metadata['albumName']
        self.asin = metadata.get('albumAsin', None)
        self.num_tracks = int(payload['numTracks'])
        self.release_date = metadata.get('albumReleaseDate', None)
        self.artist_asin = metadata.get('artistAsin', None)
        self.artist_name = metadata['artistName']
        self.primary_genre = metadata['primaryGenre']
        self.album_artist_name = metadata['albumArtistName']
        self.cover_image_url = metadata.get('albumCoverImageMedium', None)
        self.sort_album_artist_name = metadata['sortAlbumArtistName']
        self.sort_artist_name = metadata['sortArtistName']
        self.sort_album_name = metadata['sortAlbumName']
        return

    def get_songs(self, *args, **kwargs):
        return self.client.get_track_list(self)

    def __repr__(self):
        return '<Album "%s">' % self.name

    def __str__(self):
        return self.name