# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\floscraper\models.py
# Compiled at: 2019-08-03 22:42:16
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
__author__ = b'the01'
__email__ = b'jungflor@gmail.com'
__copyright__ = b'Copyright (C) 2017-19, Florian JUNG'
__license__ = b'MIT'
__version__ = b'0.1.2'
__date__ = b'2018-08-04'
import flotils

class CacheInfo(flotils.FromToDictBase, flotils.PrintableBase):
    """ Cache information """

    def __init__(self, access_time=None, etag=None):
        super(CacheInfo, self).__init__()
        self.etag = etag
        self.access_time = access_time
        self.hit = None
        return


class Response(flotils.FromToDictBase, flotils.PrintableBase):
    """ Scrapper response object """

    def __init__(self, html=None, cache_info=None, scraped=None, raw=None):
        super(Response, self).__init__()
        self.cache_info = cache_info
        self.raw = raw
        self.html = html
        self.scraped = scraped

    def __str__(self):
        return (b'({}), {}, {}, {}').format(self.cache_info, self.html, self.scraped, self.raw)

    def to_dict(self):
        """
        Response as dict

        :return: response
        :rtype: dict
        """
        res = super(Response, self).to_dict()
        if self.cache_info:
            res[b'cache_info'] = self.cache_info.to_dict()
        return res

    @staticmethod
    def from_dict(d):
        """
        Response from dict

        :param d: Dict to load
        :type d: dict
        :return: response
        :rtype: Response
        """
        if d is None:
            return
        else:
            return Response(d.get(b'html'), CacheInfo.from_dict(d.get(b'cache_info')), d.get(b'scraped'), d.get(b'raw'))