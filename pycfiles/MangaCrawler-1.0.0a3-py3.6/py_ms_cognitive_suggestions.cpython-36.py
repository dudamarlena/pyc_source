# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/MangaCrawler/py_ms_cognitive_search/py_ms_cognitive_suggestions.py
# Compiled at: 2017-04-09 11:33:10
# Size of source mod 2**32: 2182 bytes
import requests, requests.utils
from .py_ms_cognitive_search import PyMsCognitiveSearch
from .py_ms_cognitive_search import QueryChecker

class PyMsCognitiveSuggestions(PyMsCognitiveSearch):
    COGNITIVE_SUGGESTIONS_BASE = 'https://api.cognitive.microsoft.com/bing/v5.0/suggestions'

    def __init__(self, api_key, query, custom_params={}, silent_fail=False):
        query_url = self.COGNITIVE_SUGGESTIONS_BASE
        PyMsCognitiveSearch.__init__(self, api_key, query, query_url, custom_params, silent_fail=silent_fail)

    def _search(self, limit, format):
        """
        Returns a list of results objects
        """
        limit = min(limit, self.MAX_SEARCH_PER_QUERY)
        payload = {'q':self.query, 
         'mkt':'en-us', 
         'count':limit, 
         'offset':self.current_offset}
        payload.update(self.CUSTOM_PARAMS)
        headers = {'Ocp-Apim-Subscription-Key': self.api_key}
        if not self.silent_fail:
            QueryChecker.check_web_params(payload, headers)
        response = requests.get((self.QUERY_URL), params=payload, headers=headers)
        json_results = self.get_json_results(response)
        packaged_results = [SuggestResult(single_result_json) for single_result_json in json_results.get('suggestionGroups', [])[0].get('searchSuggestions', [])]
        self.current_offset += min(50, limit, len(packaged_results))
        return packaged_results


class SuggestResult(object):
    __doc__ = '\n    The class represents a SINGLE suggest result.\n    Each result will come with the following:\n\n    the variable json will contain the full json object of the result.\n\n    url: The URL for the suggestion. Internal to Bing, it seems\n    query: The original query submited\n    display_text: The suggestion generated\n    search_kind: The type of search performed for the suggestion\n\n    '

    def __init__(self, result):
        self.json = result
        self.url = result.get('url')
        self.query = result.get('query')
        self.display_text = result.get('displayText')
        self.searck_kind = result.get('searchKind')