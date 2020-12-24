# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/crawlib-project/crawlib/example/scrapy_movie/url_builder.py
# Compiled at: 2019-12-25 21:34:49
# Size of source mod 2**32: 219 bytes
from .config import Config

class UrlBuilder(object):

    def listpage_url(self, listpage_id):
        return '{}/listpage/{}'.format(Config.Url.domain, listpage_id)


url_builder = UrlBuilder()