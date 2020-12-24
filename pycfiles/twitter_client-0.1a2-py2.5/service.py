# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/twitter_client/service.py
# Compiled at: 2008-10-27 22:14:38
"""TwitterService streamlines Twitter operations.

  TwitterService: Provides methods to query feeds and manipulate items.
"""
__author__ = 'livibetter (Yu-Jie Lin)'
import urllib, atom.service, atom, twitter_client as tc
SEARCH_ATOM_URI = 'http://search.twitter.com/search.atom'

class Search(object):
    """A searching helper"""

    def __init__(self, client, keywords=None, lang='', rpp=15, page=1, since_id='', geocode='', show_user=False):
        """Initializes Search helper"""
        self.__client = client
        self.keywords = keywords or []
        self.lang = lang
        self.rpp = rpp
        self.page = page
        self.since_id = since_id
        self.geocode = geocode
        self.show_user = show_user
        self.query = ''
        self.result = None
        return

    def _ParseQueryString(self, query):
        pass

    def _BuildQueryString(self):
        query = {}
        if self.keywords:
            query['q'] = (' ').join(self.keywords)
        if self.lang:
            query['lang'] = self.lang
        if self.rpp:
            query['rpp'] = str(self.rpp)
        if self.page:
            query['page'] = str(self.page)
        if self.since_id:
            query['since_id'] = str(self.since_id)
        if self.geocode:
            query['geocode'] = self.geocode
        if self.show_user:
            query['show_user'] = str(self.show_user)
        return urllib.urlencode(query)

    def Search(self):
        """Does searching"""
        self.query = self._BuildQueryString()
        self.result = self.__client.Search(self.query)
        return self.result

    def Refresh(self):
        if self.result is None:
            return
        link_refresh = self.result.GetLinkByRel('refresh')
        if link_refresh is None:
            return
        self.query = link_refresh.href.split('?', 1)[1]
        self.result = self.__client.Search(self.query)
        return self.result


class TwitterService(atom.service.AtomService):
    """Client for the Twitter service."""

    def __init__(self, application_name, **kwargs):
        """Initializes Twitter Service

    Args:
      application_name: str In order to comply with Terms of Service of Twitter API,
                        developers must set this variable to something meaningful.
    """
        atom.service.AtomService.__init__(self, application_name=application_name, **kwargs)

    def NewSearch(self, *args, **kwargs):
        """Helps create new search helper"""
        search = Search(self, *args, **kwargs)
        return search

    def Search(self, query, converter=tc.SearchResultFeedFromString):
        """Searchs on Twitter via Search API

    Args:
      query: str Querying string.
    """
        response = self.Get(SEARCH_ATOM_URI + '?' + query)
        response = response.read()
        if converter:
            return converter(response)
        return response