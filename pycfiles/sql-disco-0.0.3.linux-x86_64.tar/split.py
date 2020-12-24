# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/sqldisco/split.py
# Compiled at: 2013-03-19 09:04:15
"""
File: split.py
Author: Jon Eisen
Description: Provide helpers for splitter.py
"""

class SqlSplit:

    def __init__(self, sqltype, connargs, query):
        self.sqltype = sqltype
        self.connargs = connargs
        self.query = query

    def __str__(self):
        return self.uri()

    def uri(self):
        """Format as json to be passed as the uri parameter"""
        import json
        return json.dumps({'dummy': 'notatag://', 
           'sqltype': self.sqltype, 
           'connargs': self.connargs, 
           'query': self.query})