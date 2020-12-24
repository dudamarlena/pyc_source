# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/sanhehu/Documents/GitHub/crawlib-project/crawlib/tests/dummy_site_crawler/movie_url_builder.py
# Compiled at: 2019-12-26 18:59:51
# Size of source mod 2**32: 531 bytes
from crawlib.tests.dummy_site.config import PORT
from crawlib.middleware.url_builder import BaseUrlBuilder

class UrlBuilder(BaseUrlBuilder):
    domain = 'http://127.0.0.1:{}'.format(PORT)

    def url_first_listpage(self):
        return self.join_all('movie', 'listpage', str(1))

    def url_nth_listpage(self, nth):
        return self.join_all('movie', 'listpage', str(nth))

    def url_movie_detail(self, movie_id):
        return self.join_all('movie', str(movie_id))


url_builder = UrlBuilder()