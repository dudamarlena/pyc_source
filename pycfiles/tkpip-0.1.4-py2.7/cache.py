# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tkpip\lib\cache.py
# Compiled at: 2017-06-27 06:45:45
from __future__ import division, absolute_import, print_function, unicode_literals
import threading, logging, pip
from .backwardcompat import *

class Cache(object):

    def __init__(self, query=[]):
        self.index_url = b'https://pypi.python.org/pypi'
        try:
            self.pypi = xmlrpclib.ServerProxy(self.index_url, pip.download.xmlrpclib_transport)
        except AttributeError:
            self.pypi = xmlrpclib.ServerProxy(self.index_url)

        self.pypi_cache = {}
        self.query = query
        self.t = None
        if self.query:
            self.query_info(self.query)
        return

    def __iter__(self):
        for key in self.pypi_cache:
            name, ver, data, urls, releases = self.pypi_cache[key]
            yield (key, name, ver, data, urls, releases)

    def get(self, key):
        value = self.pypi_cache.get(key)
        if value:
            name, ver, data, urls, releases = value
        else:
            name, ver, data, urls, releases = (
             None, None, {}, [], [])
        return (
         name, ver, data, urls, releases)

    def query_info(self, query, after_func=None):
        if self.t and self.t.isAlive():
            logging.warning(b'Query is processing, new query skipped!')
            return
        self.t = threading.Thread(target=self.t_func, args=(self.cache_info, after_func, query))
        self.t.daemon = True
        self.t.start()

    def t_func(self, func, after_func, *args):
        func(*args)
        if after_func:
            after_func(*args)

    def cache_info(self, query):
        if isinstance(query, list):
            for query in query:
                self.cache_info(query)

            return
        if query in self.pypi_cache:
            return
        releases = self.pypi.package_releases(query)
        if not releases:
            for item in self.pypi.search({b'name': query}):
                if query.lower() == item[b'name'].lower():
                    query = item[b'name']
                    break
            else:
                logging.info((b'No packages found matching {0}').format(query))
                self.pypi_cache[query] = (b'No found', {}, [], [])

            releases = self.pypi.package_releases(query)
        ver = releases[0] if releases else b'No info'
        data = self.pypi.release_data(query, ver) if ver else {}
        urls = self.pypi.release_urls(query, ver) if ver else []
        self.pypi_cache[query.lower()] = (
         query, ver, data, urls, releases)


pipcache = Cache()