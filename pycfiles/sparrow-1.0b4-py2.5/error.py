# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/sparrow/error.py
# Compiled at: 2009-07-20 09:57:48


class ConnectionError(Exception):
    pass


class TripleStoreError(Exception):
    pass


class QueryError(Exception):
    pass