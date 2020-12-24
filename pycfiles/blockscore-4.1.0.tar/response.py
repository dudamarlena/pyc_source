# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/johnbackus/Dropbox/coding/blockscore/blockscore-python/blockscore/http_client/response.py
# Compiled at: 2015-03-04 21:31:22


class Response:

    def __init__(self, body, code, headers):
        self.body = body
        self.code = code
        self.headers = headers