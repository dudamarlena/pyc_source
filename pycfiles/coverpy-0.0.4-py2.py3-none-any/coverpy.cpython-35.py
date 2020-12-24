# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sergio/Projects/cpy/coverpy/build/lib/coverpy/coverpy.py
# Compiled at: 2016-05-21 19:17:13
# Size of source mod 2**32: 1936 bytes
import os, requests
from . import exceptions

class Result:

    def __init__(self, item):
        self.artworkThumb = item['artworkUrl100']
        self.artist = item['artistName']
        self.album = item['collectionName']
        self.url = item['url']
        if 'kind' in item:
            self.type = item['kind'].lower()
        else:
            if 'wrapperType' in item:
                if item['wrapperType'].lower() == 'track':
                    self.type = 'song'
                elif item['wrapperType'].lower() == 'collection':
                    self.type = 'album'
            else:
                if 'collectionType' in item:
                    self.type = 'album'
                else:
                    self.type = 'unknown'
                if self.type == 'song':
                    self.name = item['trackName']
                else:
                    if self.type == 'album':
                        self.name = item['collectionName']
                    else:
                        self.name = 'unknown'

    def artwork(self, size=625):
        return self.artworkThumb.replace('100x100bb', '%sx%s' % (size, size))


class CoverPy:

    def __init__(self):
        self.base_url = 'https://itunes.apple.com/search/'

    def _get(self, payload, override=False, entities=False):
        if override:
            data = requests.get('%s%s' % (self.base_url, override))
        else:
            payload['entity'] = 'musicArtist,musicTrack,album,mix,song'
            payload['media'] = 'music'
            data = requests.get(self.base_url, params=payload)
        if data.status_code != 200:
            raise requests.HTTPError
        else:
            return data

    def _search(self, term, limit=1):
        payload = {'term': term, 
         'limit': limit}
        req = self._get(payload)
        return req

    def get_cover(self, term, limit=1, debug=False):
        search = self._search(term, limit)
        parsed = search.json()
        if parsed['resultCount'] == 0:
            raise exceptions.NoResultsException
        result = parsed['results'][0]
        result['url'] = search.url
        return Result(result)