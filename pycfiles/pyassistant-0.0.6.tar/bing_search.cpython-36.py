# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/garicchi/projects/remote/python/pyassistant/pyassistant/search/bing_search.py
# Compiled at: 2018-01-13 22:22:58
# Size of source mod 2**32: 749 bytes
import urllib.request as request, urllib.parse as parse, json

class BingSearch:

    def __init__(self, api_key):
        self.api_key = api_key

    def search_video(self, word, lang='ja-JP', count=35, videoLength='short'):
        word = parse.quote(word)
        url = 'https://api.cognitive.microsoft.com/bing/v7.0/videos/search?q={}'.format(word)
        url += '&mkt={}'.format(lang)
        url += '&count={}'.format(count)
        url += '&videoLength={}'.format(videoLength)
        req = request.Request(url)
        req.add_header('Ocp-Apim-Subscription-Key', self.api_key)
        with request.urlopen(req) as (res):
            result = res.read().decode('utf-8')
            result = json.loads(result)
        return result