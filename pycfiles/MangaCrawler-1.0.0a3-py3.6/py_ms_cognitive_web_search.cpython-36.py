# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/MangaCrawler/py_ms_cognitive_web_search.py
# Compiled at: 2017-04-24 15:19:13
# Size of source mod 2**32: 2341 bytes
import requests, requests.utils
from .py_ms_cognitive_search.py import PyMsCognitiveSearch, QueryChecker

class PyMsCognitiveWebSearch(PyMsCognitiveSearch):
    SEARCH_WEB_BASE = 'https://api.cognitive.microsoft.com/bing/v5.0/search'

    def __init__(self, api_key, query, custom_params={}, silent_fail=False):
        query_url = self.SEARCH_WEB_BASE
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
        packaged_results = [WebResult(single_result_json) for single_result_json in json_results.get('webPages', {}).get('value', [])]
        self.current_offset += min(50, limit, len(packaged_results))
        return packaged_results


class WebResult(object):
    __doc__ = '\n    The class represents a SINGLE search result.\n    Each result will come with the following:\n\n    the variable json will contain the full json object of the result.\n\n    title: title of the result (alternately name)\n    url: the url of the result. Seems to be a Bing redirect\n    displayUrl: the url used to display\n    snippet: description for the result (alternately description)\n    id: MsCognitive id for the page\n    '

    def __init__(self, result):
        self.json = result
        self.url = result.get('url')
        self.display_url = result.get('displayUrl')
        self.name = result.get('name')
        self.snippet = result.get('snippet')
        self.id = result.get('id')
        self.title = result.get('name')
        self.description = result.get('snippet')
        self.deep_links = result.get('deepLinks')