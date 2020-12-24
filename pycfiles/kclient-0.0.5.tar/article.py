# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/a11960/p-project/k-client-pub/kclient/article.py
# Compiled at: 2018-03-10 05:03:50
"""
    kclient.article
    ~~~~~~~~~~

    Python wrapper for k-client Article API.
"""
from .enums import Groups
from .client import Client

class Article(Client):

    def count(self, group=Groups.KEYAKIZAKA):
        """
        :return:
        """
        param = {'group': group.value}
        return self._post('/article/count', param)

    def get(self, contents):
        """
        :param contents: contents id
        :return:
        """
        return self._post('/article', {'article': contents})

    def allhistory(self, group=Groups.KEYAKIZAKA, count=100, fromdate=None, sortorder=0, letter=False):
        """
        :param group:
        :param count:
        :param fromdate:
        :param sortorder: 0: ascending order, 1: descending order
        :param letter: include letter.
        :return:
        """
        param = {'count': count, 
           'fromdate': fromdate, 
           'group': group.value, 
           'sortorder': sortorder}
        allhistory = self._post('/article/allhistory', param)
        if not letter:
            allhistory['history'] = filter(lambda h: 'letter' not in h['body'], allhistory['history'])
        return allhistory