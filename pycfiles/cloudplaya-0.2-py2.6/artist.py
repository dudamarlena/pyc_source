# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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