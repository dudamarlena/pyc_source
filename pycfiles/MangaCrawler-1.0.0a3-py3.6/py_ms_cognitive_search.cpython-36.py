# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/MangaCrawler/py_ms_cognitive_search.py
# Compiled at: 2017-04-09 11:33:10
# Size of source mod 2**32: 6099 bytes
"""
Main class for doing actual searches.
"""
import time, re
__author__ = 'tristantao (https://github.com/tristantao)'

class PyMsCognitiveException(Exception):
    pass


class PyMsCognitiveWebSearchException(Exception):
    pass


class PyMsCognitiveSearch(object):
    __doc__ = '\n    Shell class for the individual searches\n    '

    def __init__(self, api_key, query, query_url, custom_params={}, silent_fail=False):
        self.api_key = api_key
        self.silent_fail = silent_fail
        self.current_offset = 0
        self.query = query
        self.QUERY_URL = query_url
        self.CUSTOM_PARAMS = custom_params
        self.MAX_SEARCH_PER_QUERY = 50
        self.MAX_SUGGESTIONS_PER_QUERY = 8
        self.most_recent_json = None

    def get_json_results(self, response):
        """
        Parses the request result and returns the JSON object. Handles all errors.
        """
        try:
            self.most_recent_json = response.json()
            json_results = response.json()
            if response.status_code in (401, 403):
                raise PyMsCognitiveWebSearchException('CODE {code}: {message}'.format(code=(response.status_code), message=(json_results['message'])))
            else:
                if response.status_code in (429, ):
                    message = json_results['message']
                    try:
                        timeout = int(re.search('in (.+?) seconds', message).group(1)) + 1
                        print('CODE 429, sleeping for {timeout} seconds').format(timeout=(str(timeout)))
                        time.sleep(timeout)
                    except (AttributeError, ValueError) as e:
                        if not self.silent_fail:
                            raise PyMsCognitiveWebSearchException('CODE 429. Failed to auto-sleep: {message}'.format(code=(response.status_code), message=(json_results['message'])))
                        else:
                            print('CODE 429. Failed to auto-sleep: {message}. Trying again in 5 seconds.'.format(code=(response.status_code), message=(json_results['message'])))
                            time.sleep(5)

        except ValueError as vE:
            if not self.silent_fail:
                raise PyMsCognitiveWebSearchException('Request returned with code %s, error msg: %s' % (r.status_code, r.text))
            else:
                print('[ERROR] Request returned with code %s, error msg: %s. \nContinuing in 5 seconds.' % (r.status_code, r.text))
                time.sleep(5)

        return json_results

    def search(self, limit=50, format='json'):
        """ Returns the result list, and also the uri for next page (returned_list, next_uri) """
        return self._search(limit, format)

    def search_all(self, quota=50, format='json'):
        """
        Returns a single list containing up to 'limit' Result objects
        Will keep requesting until quota is met
        Will also truncate extra results to return exactly the given quota
        """
        quota_left = quota
        results = []
        while quota_left > 0:
            more_results = self._search(quota_left, format)
            if not more_results:
                break
            results += more_results
            quota_left = quota_left - len(more_results)
            time.sleep(1)

        results = results[0:quota]
        return results


class QueryChecker:
    __doc__ = '\n    Isolated human-error-checker class.\n    All methods are static and do not modify state.\n    if/else mess below forgoes optimization in favor of clarity.\n    '

    @staticmethod
    def check_web_params(query_dict, header_dict):
        responseFilters = ('Computation', 'Images', 'News', 'RelatedSearches', 'SpellSuggestions',
                           'TimeZone', 'Videos', 'Webpages')
        if 'cc' in query_dict.keys():
            if query_dict['cc']:
                if not header_dict['Accept-Language']:
                    raise AssertionError('Attempt to use country-code without specifying language.')
            if query_dict['mkt']:
                raise ReferenceError('cc and mkt cannot be specified simultaneously')
        if 'count' in query_dict.keys():
            if int(query_dict['count']) >= 51 or int(query_dict['count']) < 0:
                raise ValueError('Count specified out of range. 50 max objects returned.')
        if 'freshness' in query_dict.keys():
            if query_dict['freshness'] not in ('Day', 'Week', 'Month'):
                raise ValueError('Freshness must be == Day, Week, or Month. Assume Case-Sensitive.')
        if 'offset' in query_dict.keys():
            if int(query_dict['offset']) < 0:
                raise ValueError('Offset cannot be negative.')
        if 'responseFilter' in query_dict.keys():
            if query_dict['responseFilter'] not in responseFilters:
                raise ValueError('Improper response filter.')
        if 'safeSearch' in query_dict.keys():
            if query_dict['safeSearch'] not in ('Off', 'Moderate', 'Strict'):
                raise ValueError('safeSearch setting must be Off, Moderate, or Strict. Assume Case-Sensitive.')
            if 'X-Search-ClientIP' in query_dict.keys():
                raw_input('You have specified both an X-Search-ClientIP header and safesearch setting\nplease note: header takes precedence')
        if 'setLang' in query_dict.keys():
            if header_dict['Accept-Language']:
                raise AssertionError('Attempt to use both language header and query param.')
        if 'textDecorations' in query_dict.keys():
            if query_dict['textDecorations'].lower() not in ('true', 'false'):
                raise TypeError('textDecorations is type bool')
        if 'textFormat' in query_dict.keys():
            if query_dict['textFormat'] not in ('Raw', 'HTML'):
                raise ValueError('textFormat must be == Raw or HTML. Assume Case-Sensitive.')
        return True