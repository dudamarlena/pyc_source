# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/MangaCrawler/py_ms_cognitive_search/py_ms_cognitive_image_search.py
# Compiled at: 2017-04-09 11:33:10
# Size of source mod 2**32: 2574 bytes
import requests, requests.utils
from .py_ms_cognitive_search import PyMsCognitiveSearch
from .py_ms_cognitive_search import QueryChecker

class PyMsCognitiveImageException(Exception):
    pass


class PyMsCognitiveImageSearch(PyMsCognitiveSearch):
    SEARCH_IMAGE_BASE = 'https://api.cognitive.microsoft.com/bing/v5.0/images/search'

    def __init__(self, api_key, query, custom_params={}, silent_fail=False):
        query_url = self.SEARCH_IMAGE_BASE
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
        packaged_results = [ImageResult(single_result_json) for single_result_json in json_results['value']]
        self.current_offset += min(50, limit)
        return packaged_results


class ImageResult(object):
    __doc__ = '\n    The class represents a SINGLE Image result.\n    Each result will come with the following:\n\n    the variable json will contain the full json object of the result.\n\n    conten_url: duration of the Image\n    name: name of the image / page title\n    image_id: image id\n    image_insights_token: image insights token\n    web_search_url: the bing search url for the image\n    host_page_url: the bing url to the host page\n    content_size: size of the image\n    thumbnail_url: url of the thumbnail\n\n    Not included: lots of info, poke in json to see.\n    '

    def __init__(self, result):
        self.json = result
        self.content_url = result.get('contentUrl')
        self.name = result.get('name')
        self.image_id = result.get('ImageId')
        self.image_insights_token = result.get('imageInsightsToken')
        self.web_search_url = result.get('webSearchUrl')
        self.host_page_url = result.get('hostPageUrl')
        self.content_size = result.get('contentSize')
        self.thumbnail_url = result.get('thumbnailUrl')