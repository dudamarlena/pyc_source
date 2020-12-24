# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/diwnotifier/utils/short_links_collector/tiny4py/shorteners/bitly_shortener.py
# Compiled at: 2014-01-03 09:50:36
"""
        Developed by 
        Andrea Stagi <stagi.andrea@gmail.com>

        Tiny4py: python wrapper to use main url shortener services in your apps
        Copyright (C) 2010 Andrea Stagi

        This program is free software: you can redistribute it and/or modify
        it under the terms of the GNU Lesser General Public License as published 
        by the Free Software Foundation, either version 3 of the License, or
        (at your option) any later version.

        This program is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
        GNU Lesser General Public License for more details.

        You should have received a copy of the GNU Lesser General Public License
        along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
from shortener_qrcode import *

class BitlyShortener(ShortenerQrCode):

    def __init__(self):
        Shortener.__init__(self)
        QrCode.__init__(self)
        self.__user = TINY4PY_BITLY_USR
        self.__apikey = TINY4PY_BITLY_API
        self.setQrId('.qrcode')
        self._setBaseUrlParameters({'login': self.__user, 'apiKey': self.__apikey, 'format': 'json'})

    def setApi(self, user, apikey):
        self.__user = user
        self.__apikey = apikey
        self._setBaseUrlParameters({'login': self.__user, 'apiKey': self.__apikey, 'format': 'json'})

    def getUserClicks(self, shorturl, params={}, callback=None):
        return self._genericRequestMethod(shorturl, self.__userClicksRequest, params, callback)

    def getGlobalClicks(self, shorturl, params={}, callback=None):
        return self._genericRequestMethod(shorturl, self.__globalClicksRequest, params, callback)

    def _shortRequest(self, url, params={}):
        rq = self._genericRequest('shorten', self._getBaseUrlParameters({'longUrl': url}))
        j = loads(rq)
        if j['status_code'] == BITLY_OK:
            return j['data']['url']
        self.__responseErrorParse(j)

    def __userClicksRequest(self, shorturl, params={}):
        rq = self._genericRequest('clicks', self._getBaseUrlParameters({'shortUrl': shorturl}), 'GET')
        j = loads(rq)
        if j['status_code'] == BITLY_OK:
            return j['data']['clicks'][0]['user_clicks']
        self.__responseErrorParse(j)

    def __globalClicksRequest(self, shorturl, params={}):
        rq = self._genericRequest('clicks', self._getBaseUrlParameters({'shortUrl': shorturl}), 'GET')
        j = loads(rq)
        if j['status_code'] == BITLY_OK:
            return j['data']['clicks'][0]['global_clicks']
        self.__responseErrorParse(j)

    def __responseErrorParse(self, j):
        if j['status_code'] == BITLY_ERR:
            if j['status_txt'] == BITLY_LOGERR:
                raise ShortenerError('Invalid login')
            elif j['status_txt'] == BITLY_URLERR:
                raise ShortenerError('Invalid long URL')
        elif j['status_code'] == BITLY_TLERR:
            raise ShortenerError('Rate limit exceeded')
        else:
            raise ShortenerError('Unknown error')

    def _getBaseUrl(self):
        return BITLY_BASEURL