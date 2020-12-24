# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/MangaCrawler/py_ms_cognitive_search/py_ms_cognitive_news_search.py
# Compiled at: 2017-04-09 11:33:10
# Size of source mod 2**32: 2485 bytes
import requests, requests.utils
from .py_ms_cognitive_search import PyMsCognitiveSearch
from .py_ms_cognitive_search import QueryChecker

class PyMsCognitiveNewsException(Exception):
    pass


class PyMsCognitiveNewsSearch(PyMsCognitiveSearch):
    SEARCH_NEWS_BASE = 'https://api.cognitive.microsoft.com/bing/v5.0/news/search'

    def __init__(self, api_key, query, custom_params={}, silent_fail=False):
        query_url = self.SEARCH_NEWS_BASE
        PyMsCognitiveSearch.__init__(self, api_key, query, query_url, custom_params, silent_fail=silent_fail)

    def _search(self, limit, format):
        """
        Returns a list of result objects, with the url for the next page MsCognitive search url.
        """
        limit = min(limit, self.MAX_SEARCH_PER_QUERY)
        payload = {'q':self.query, 
         'count':limit, 
         'offset':self.current_offset}
        payload.update(self.CUSTOM_PARAMS)
        headers = {'Ocp-Apim-Subscription-Key': self.api_key}
        if not self.silent_fail:
            QueryChecker.check_web_params(payload, headers)
        response = requests.get((self.QUERY_URL), params=payload, headers=headers)
        json_results = self.get_json_results(response)
        packaged_results = [NewsResult(single_result_json) for single_result_json in json_results['value']]
        self.current_offset += min(50, limit, len(packaged_results))
        return packaged_results


class NewsResult(object):
    __doc__ = '\n    The class represents a SINGLE news result.\n    Each result will come with the following:\n\n    the variable json will contain the full json object of the result.\n\n    category: category of the news\n    name: name of the article (title)\n    url: the url used to display.\n    image_url: url of the thumbnail\n    date_published: the date the article was published\n    description: description for the result\n\n    Not included: about, provider, mentions\n    '

    def __init__(self, result):
        self.json = result
        self.category = result.get('category')
        self.name = result.get('name')
        self.url = result.get('url')
        try:
            self.image_url = result['image']['thumbnail']['contentUrl']
        except KeyError as kE:
            self.image_url = None

        self.date_published = result.get('datePublished')
        self.description = result.get('description')