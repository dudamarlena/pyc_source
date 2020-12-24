# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/stackoverflow/stackexchange.py
# Compiled at: 2014-02-22 10:22:35
import os, json, requests
from BeautifulSoup import BeautifulSoup
from stackoverflow.utils import unescape

class StackExchange:

    def __init__(self, cache):
        self._cache = os.path.expanduser(cache)

    def list(self):
        if not os.path.exists(self._cache):
            cache_dict = {}
            with open(self._cache, 'w+') as (cache):
                cache.write(json.dumps(cache_dict))
        else:
            with open(self._cache, 'r') as (cache):
                cache_dict = json.load(cache)
        if 'sites' not in cache_dict.keys():
            cache_dict['sites'] = dict()
        r = requests.head('http://api.stackexchange.com/sites')
        length = r.headers['content-length']
        if 'content-length' in cache_dict['sites'].keys():
            if length == cache_dict['sites']['content-length']:
                return cache_dict['sites']
        cache_dict['sites']['content-length'] = length
        cache_dict['sites'].update(requests.get('http://api.stackexchange.com/sites').json())
        with open(self._cache, 'w') as (cache):
            cache.write(json.dumps(cache_dict))
        return cache_dict['sites']

    def list_sites(self):
        for site in self.list()['items']:
            yield site

    def list_urls(self):
        for site in self.list()['items']:
            yield site['site_url']