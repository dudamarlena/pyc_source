# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\dev\scrapgo\scrapgo\scraper\requests\crawler.py
# Compiled at: 2019-04-16 15:10:35
# Size of source mod 2**32: 8397 bytes
import re
from collections import deque, namedtuple
from scrapgo.utils.urlparser import queryjoin, parse_src, parse_query, filter_params
from scrapgo.utils.shortcuts import abs_path
from scrapgo.lib.history import HistoryDict
from scrapgo.modules import CachedRequests, SoupParserMixin
ScrapResponse = namedtuple('ScrapResponse', 'query match history')

class RequestsSoupCrawler(SoupParserMixin, CachedRequests):
    ROOT_URL = None

    def __init__(self, url=None, root_params=None, **kwargs):
        (super().__init__)(**kwargs)
        self.ROOT_URL = queryjoin(url or self.ROOT_URL, root_params)
        self.history = HistoryDict()

    def _set_history(self, url, previous, name):
        url = abs_path(self.ROOT_URL, url)
        self.history.set_history(url, previous, name)

    def _set_response_meta(self, response, query, match, previous, name):
        self.history.set_history(response.url, previous, name)
        meta = ScrapResponse(query, match, self.history)
        setattr(response, 'scraper', meta)

    def get(self, link, headers=None, **kwargs):
        url = abs_path(self.ROOT_URL, link)
        response = (self._get)(url, headers=headers, **kwargs)
        return response

    def post(self, url, headers=None, **kwargs):
        response = (self._post)(url, headers=headers, **kwargs)
        return response

    def _link2response(self, link, link_pattern, previous, filters, refresh, fields, referer, name, context):
        headers = self.get_header()
        match = None
        if link_pattern is not None:
            if isinstance(link_pattern, re.Pattern):
                match = link_pattern.match(link).group
        else:
            query = parse_query(link)
            return all((f(link, query, match, context) for f in filters)) or None
        if referer:
            headers['Referer'] = referer
        response = self.get(link,
          headers=headers, refresh=refresh, fields=fields)
        self._set_response_meta(response, query, match, previous, name)
        return response

    def _parse_response(self, response, parser, context):
        soup = self._get_soup(response)
        return parser(response, soup, context)

    def _crawl(self, response, link_pattern, previous, filters, parser, name, context=None, recursive=False, refresh=False, referer=None, fields=None, _visited=None):
        _visited = _visited or set()
        if isinstance(link_pattern, re.Pattern):
            for link in self._parse_link(response, link_pattern):
                if link not in _visited:
                    _visited.add(link)
                    rsp = self._link2response(link, link_pattern, previous, filters, refresh, fields, referer, name, context)
                    if rsp is None:
                        continue
                    soup = self._get_soup(rsp)
                    yield (
                     rsp, parser(rsp, soup, context))
                    if recursive and soup is not None:
                        yield self._crawl(rsp, link_pattern, previous, filters, parser, name, context, recursive, refresh, referer, fields, _visited)

        else:
            if isinstance(link_pattern, str):
                rsp = self._link2response(link_pattern, None, previous, filters, refresh, fields, referer, name, context)
                if rsp:
                    soup = self._get_soup(rsp)
                    yield (rsp, parser(rsp, soup, context))