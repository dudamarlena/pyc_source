# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cloudplaya/artist.py
# Compiled at: 2012-07-07 20:58:37


class Artist(object):
    COLUMNS = [
     'artistName', 'objectId', 'sortArtistName', 'artistAsin']

    def __init__(self, client, payload):
        self.client = client
        metadata = payload['metadata']
        self.id = metadata['objectId']
        self.name = metadata['artistName']
        self.asin = metadata.get('artistAsin', None)
        self.sort_name = metadata['sortArtistName']
        self.num_tracks = payload['numTracks']
        return

    def __repr__(self):
        return '<Artist "%s">' % self.name

    def __str__(self):
        return self.name