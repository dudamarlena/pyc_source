# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/diwnotifier/utils/short_links_collector/tiny4py/shorteners/tinyurl_shortener.py
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
from shortener import *

class TinyurlShortener(Shortener):

    def __init__(self):
        Shortener.__init__(self)
        self._setBaseUrlParameters({'User-Agent': 'toolbar'})

    def _shortRequest(self, url, params={}):
        return self._genericRequest('create.php', self._getBaseUrlParameters({'url': url}))

    def _getBaseUrl(self):
        return TINYURL_BASEURL