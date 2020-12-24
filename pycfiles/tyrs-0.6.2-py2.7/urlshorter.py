# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/tyrs/shorter/urlshorter.py
# Compiled at: 2011-07-04 17:37:11
import urllib2

class UrlShorter(object):

    def _quote_url(self, url):
        long_url = urllib2.quote(url)
        long_url = long_url.replace('/', '%2F')
        return long_url

    def _get_request(self, url, data=None):
        return urllib2.urlopen(url, data).read()