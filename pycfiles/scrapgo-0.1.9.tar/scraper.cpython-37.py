# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\dev\scrapgo\scrapgo\scraper\scraper.py
# Compiled at: 2019-03-16 07:42:25
# Size of source mod 2**32: 3355 bytes
import re
from collections import abc
from .base import BaseScraper
from scrapgo.modules import SoupParserMixin
from scrapgo.actions import *

class Scraper(BaseScraper):
    LINK_ROUTER = None

    def __init__(self, *args, **kwargs):
        (super().__init__)(*args, **kwargs)
        loc = location(self.ROOT_URL, self.default_parser, self.ROOT_URL)
        if not self.LINK_ROUTER:
            self.LINK_ROUTER = [
             loc]
        if not isinstance(self.LINK_ROUTER[0], Location):
            self.LINK_ROUTER.insert(0, loc)

    def get_link_pattern(self, name):
        for action in self.LINK_ROUTER:
            if action.name == name:
                return action.pattern

    def scrap(self, context=None, until=None):
        self.scrap_results = {}
        urls = []
        visited = set()
        for action in self.LINK_ROUTER:
            next_urls = []
            name = action.name
            caching = action.caching
            parser = self._get_fuction(action.parser, 'parser')
            if isinstance(action, Location):
                url = self.ROOT_URL if action.url == '/' else action.url
                r = self.get(url, caching)
                soup = self._get_soup(r.content)
                parsed = parser(url, (re.compile(url).match(url)), soup=soup)
                self.reducer(parsed, name)
                next_urls.append(url)
            else:
                if isinstance(action, Link):
                    pattern = action.pattern
                    urlfilter = self._get_fuction(action.urlfilter)
                    recursive = action.recursive
                    for url in urls:
                        for link in self._scrap_links(url, pattern, urlfilter, context, recursive, cache=caching):
                            if link in visited:
                                continue
                            visited.add(link)
                            r = self.get(link, caching)
                            match = pattern.match(link).group
                            soup = self._get_soup(r.content)
                            parsed = parser(link, match, soup=soup)
                            self.reducer(parsed, name)
                            next_urls.append(link)

                else:
                    pattern = action.pattern
                    urlfilter = self._get_fuction(action.urlfilter)
                    for url in urls:
                        for src in self._scrap_links(url, pattern, urlfilter, context, cache=caching):
                            r = self.get(src, caching)
                            match = pattern.match(src).group
                            parsed = parser(src, match, content=(r.content))
                            self.reducer(parsed, name)

                    continue
            if until is not None:
                if until == name:
                    break
            urls = next_urls

        return self.scrap_results

    def reducer(self, parsed, name):
        if parsed is None:
            return
        if isinstance(parsed, (str, bytes)):
            return self.scrap_results.setdefault(name, []).append(parsed)
        if isinstance(parsed, abc.Mapping):
            return self.scrap_results.setdefault(name, []).append(parsed)
        if isinstance(parsed, abc.Iterable):
            return self.scrap_results.setdefault(name, []).extend(list(parsed))
        return parsed