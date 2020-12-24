# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/tyrs/shorter/bitly.py
# Compiled at: 2011-07-11 18:11:51
import urllib2
try:
    import json
except:
    import simplejson as json

from urlshorter import UrlShorter
APIKEY = 'apiKey=R_f806c2011339080ea0b623959bb8ecff'
VERION = 'version=2.0.1'
LOGIN = 'login=tyrs'

class BitLyUrlShorter(UrlShorter):

    def __init__(self):
        self.base = 'http://api.bit.ly/shorten?%s&%s&%s&longUrl=%s'

    def do_shorter(self, url):
        long_url = self._quote_url(url)
        request = self.base % (VERION, LOGIN, APIKEY, long_url)
        response = json.loads(urllib2.urlopen(request).read())
        return response['results'][url]['shortUrl']