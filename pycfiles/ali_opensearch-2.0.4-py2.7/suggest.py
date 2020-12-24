# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/opensearchsdk/v2/suggest.py
# Compiled at: 2015-12-05 23:58:32
from opensearchsdk.apiclient import api_base

class SuggestManager(api_base.Manager):
    """Suggest resource manage class"""

    def suggest(self, query, index_name, suggest_name, hit=10):
        """
        get suggest from user input.
        :param query: query string
        :param index_name: application name
        :param suggest_name: suggestion rule
        :param hit: count of suggestion, 1-10, default 10
        :return:
        """
        body = dict(query=query, index_name=index_name, suggest_name=suggest_name, hit=str(hit))
        return self.send_get(body)