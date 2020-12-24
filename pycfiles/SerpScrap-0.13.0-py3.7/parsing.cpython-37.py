# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\scrapcore\parsing.py
# Compiled at: 2017-08-18 10:54:52
# Size of source mod 2**32: 1631 bytes
import logging, re
from scrapcore.database import SearchEngineResultsPage
from scrapcore.parser.google_parser import GoogleParser
logger = logging.getLogger(__name__)

class Parsing:

    def get_parser_by_url(self, url):
        """Get the appropriate parser by an search engine url."""
        parser = None
        if re.search('^http[s]?://www\\.google', url):
            parser = GoogleParser
        if not parser:
            raise Exception('No parser for {}.'.format(url))
        return parser

    def get_parser_by_search_engine(self, search_engine):
        """Get the appropriate parser for the search_engine"""
        if search_engine == 'google' or search_engine == 'googleimg':
            return GoogleParser
        raise Exception('No such parser for "{}"'.format(search_engine))

    def parse_serp(self, config, html=None, parser=None, scraper=None, search_engine=None, query=''):
        """parse and store data in the sqlalchemy session.
        Returns:
            The parsed SERP object.
        """
        if not parser:
            if html:
                parser = self.get_parser_by_search_engine(search_engine)
                parser = parser(config, query=query)
                parser.parse(html)
        serp = SearchEngineResultsPage()
        if query:
            serp.query = query
        if parser:
            serp.set_values_from_parser(parser)
        if scraper:
            serp.set_values_from_scraper(scraper)
        return serp