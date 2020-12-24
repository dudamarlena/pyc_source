# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\ifacetools\httputil\HTTPUtil.py
# Compiled at: 2019-08-07 05:58:54
# Size of source mod 2**32: 857 bytes
import requests

class HTTPUtil:

    def __init__(self):
        pass

    def post_form(self, url, data=None, **kwargs):
        response = (requests.post)(url=url, data=data, **kwargs)
        return response

    def post_json(self, url, json=None, **kwargs):
        response = (requests.post)(url=url, json=json, **kwargs)
        return response

    def get(self, url, params=None, **kwargs):
        response = (requests.get)(url, params, **kwargs)
        return response