# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tomchristie/GitHub/tomchristie/falcon-api/falcon_api/request.py
# Compiled at: 2016-04-22 08:47:34
# Size of source mod 2**32: 645 bytes
from api_star.request import RequestMixin
from falcon.request import Request as _Request

class CaseInsensitiveDict(dict):
    __doc__ = "\n    Falcon uses all uppercase values for the request headers.\n    We'd like to ensure case-insensitive lookups, so that eg.\n    `request.headers['Accept']` is valid.\n    "

    def get(self, key, default=None):
        return super(CaseInsensitiveDict, self).get(key.upper(), default)


class Request(RequestMixin, _Request):

    @property
    def headers(self):
        if not hasattr(self, '_headers'):
            self._headers = CaseInsensitiveDict(super(Request, self).headers)
        return self._headers