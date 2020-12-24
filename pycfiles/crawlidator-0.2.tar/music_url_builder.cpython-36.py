# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/sanhehu/Documents/GitHub/crawlib-project/crawlib/tests/dummy_site_crawler/music_url_builder.py
# Compiled at: 2019-12-27 22:14:22
# Size of source mod 2**32: 622 bytes
from crawlib.tests.dummy_site.config import PORT
from crawlib.middleware.url_builder import BaseUrlBuilder

class UrlBuilder(BaseUrlBuilder):
    domain = 'http://127.0.0.1:{}'.format(PORT)

    def url_random_music(self):
        return self.join_all('music', 'random')

    def url_artist(self, artist_id):
        return self.join_all('music', 'artist', str(artist_id))

    def url_genre(self, genre_id):
        return self.join_all('music', 'genre', str(genre_id))

    def url_music_detail(self, music_id):
        return self.join_all('music', str(music_id))


url_builder = UrlBuilder()