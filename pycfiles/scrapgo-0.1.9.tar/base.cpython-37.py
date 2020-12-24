# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\dev\scrapgo\scrapgo\scraper\base.py
# Compiled at: 2019-03-16 07:37:27
# Size of source mod 2**32: 2255 bytes
from collections import OrderedDict
import requests
from scrapgo.lib.data_structure import SetStack
from scrapgo.utils.shortcuts import abs_path
from scrapgo.modules import RequestsManager, SoupParserMixin

class BaseScraper(SoupParserMixin):
    ROOT_URL = None
    requests_manager = RequestsManager()

    def __init__(self, root=None, **kwargs):
        (super().__init__)(**kwargs)
        self.ROOT_URL = self.ROOT_URL or root

    def get(self, link, cache, headers=None):
        url = abs_path(self.ROOT_URL, link)
        return self.requests_manager._get(url, cache=cache, headers=headers)

    def _get_fuction(self, func, kind='urlfilter'):
        if callable(func):
            return func
        if isinstance(func, str):
            if hasattr(self, func):
                return getattr(self, func)
        if kind == 'urlfilter':
            return self.main_urlfilter
        return self.default_parser

    def _scrap_links(self, root, link_pattern, urlfilter, context=None, recursive=None, cache=True, set_headers=None):
        linkstack = SetStack([(root, self.requests_manager.get_header())])
        visited = set()
        set_headers = set_headers or (lambda location, previous, headers: headers)
        while linkstack:
            root, headers = linkstack.pop()
            requests = self.get(root, cache=cache, headers=headers)
            for link in self._parse_link(requests, link_pattern):
                if link not in visited:
                    visited.add(link)
                    match = link_pattern.match(link).group
                    if not self.main_urlfilter(link, match, context=context):
                        continue
                    if urlfilter(link, match, context=context):
                        if recursive:
                            current_headers = self.requests_manager.get_header()
                            headers = set_headers(link, root, current_headers)
                            linkstack.push((link, headers))
                        yield link

    def main_urlfilter(self, url, pattern, context=None):
        return True

    def default_parser(self, url, pattern, content=None, soup=None):
        pass