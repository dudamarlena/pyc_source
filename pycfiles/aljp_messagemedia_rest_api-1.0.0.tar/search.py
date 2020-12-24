# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/opensearchsdk/v2/search.py
# Compiled at: 2015-12-05 11:03:20
from opensearchsdk.apiclient import api_base

class SearchManager(api_base.Manager):
    """Search resource manage class"""

    def search(self, query=None, index_name=None, fetch_fields=None, qp=None, disable=None, first_formula_name=None, formula_name=None, summary=None, scroll=None, search_type=None, scroll_id=None):
        """
        do search with given parameters
        :param query: query string
        :param index_name: application name(s), separate by ';'
        :param fetch_fields: field to return, separate by ';'
        :param qp: search analyse rules, separate by ','
        :param disable: whether turn off search analyse
        :param first_formula_name:
        :param formula_name:
        :param summary:
        :param scroll: expire time, default ms
        :param search_type: scan
        :param scroll_id: last search id, None if first time search
        :return: dict, search result
        """
        body = {}

        def _simple_search():
            body['index_name'] = index_name
            body['query'] = query
            if fetch_fields:
                body['fetch_fields'] = fetch_fields
            if qp:
                body['qp'] = qp
            if disable:
                body['disable'] = disable
            if first_formula_name:
                body['first_formula_name'] = first_formula_name
            if formula_name:
                body['formula_name'] = formula_name
            if summary:
                body['summary'] = summary

        if scroll:
            body['scroll'] = scroll
            if scroll_id:
                body['scroll_id'] = scroll_id
            else:
                body['search_type'] = search_type
                _simple_search()
        else:
            _simple_search()
        return self.send_get(body)