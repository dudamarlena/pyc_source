# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ymizushi/Develop/ymizushi/nicosearch/nicosearch/__init__.py
# Compiled at: 2015-08-15 05:35:14
# Size of source mod 2**32: 2708 bytes
import requests, json
from .config import API_ENTRY_POINT, API_END_POINT

class SearchQueryBuilder(object):

    def __init__(self, keyword, **option):
        self._SearchQueryBuilder__query = {'query': keyword, 
         'service': [
                     'video'], 
         'search': [
                    'title'], 
         'join': [
                  'cmsid', 'title', 'view_counter'], 
         'from': 0, 
         'size': 10, 
         'sort_by': 'view_counter', 
         'issuer': 'nicosearcy.py', 
         'reason': 'searching niconico with python'}
        for k, v in option.items():
            if k is 'frm':
                k = 'from'
            self._SearchQueryBuilder__query[k] = v

    def build(self):
        return self._SearchQueryBuilder__query


class SearchRequest(object):
    _SearchRequest__URL = API_ENTRY_POINT + API_END_POINT
    _SearchRequest__HEADERS = {'content-type': 'application/json'}

    def __init__(self, data, url=_SearchRequest__URL):
        self._SearchRequest__data = data
        self._SearchRequest__url = url

    def fetch(self):
        return SearchResponse(requests.post(self._SearchRequest__url, data=json.dumps(self._SearchRequest__data), headers=self._SearchRequest__HEADERS))


class SearchResponse(object):

    @classmethod
    def __filter_contents(cls, text):
        json_list = text.splitlines()
        json_object_list = []
        for json_object in json_list:
            json_object_list += [json.loads(json_object, 'utf-8')]

        contents = []
        for json_object in json_object_list:
            if 'values' in json_object.keys():
                for value in json_object['values']:
                    if 'cmsid' in value.keys():
                        contents += [value]
                        continue

                continue

        return contents

    def __init__(self, response):
        self._SearchResponse__response = response
        self._SearchResponse__contents = self._SearchResponse__filter_contents(self._SearchResponse__response.text)

    @property
    def contents(self):
        return self._SearchResponse__contents


class Content:

    def __init__(self, rowid, cmsid, title, view_counter):
        self._Content__rowid = rowid
        self._Content__cmsid = cmsid
        self._Content__title = title
        self._Content__view_counter = view_counter

    @property
    def rowid(self):
        return self._Content__rowid

    @property
    def cmsid(self):
        return self._Content__cmsid

    @property
    def title(self):
        return self._Content__title

    @property
    def view_counter(self):
        return self._Content__view_counter


class ContentsBuilder:

    def __init__(self, contents):
        self._contents = contents

    def build(self):
        return map(lambda x: Content(x['_rowid'], x['cmsid'], x['title'], x['view_counter']), self._contents)


def search(keyword, **option):
    query = SearchQueryBuilder(keyword, **option).build()
    return SearchRequest(query).fetch().contents