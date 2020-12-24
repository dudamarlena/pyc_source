# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/foxylib/tools/http/http_tool.py
# Compiled at: 2020-01-01 18:45:46
# Size of source mod 2**32: 2590 bytes
import os
from functools import reduce
import time, requests
from markupsafe import Markup

class HttpTool:

    @classmethod
    def url2httpr(cls, url, args=None, kwargs=None, session=None, adapter=None):
        _a = args or []
        _HttpTool__k = kwargs or {}
        s = session or requests.Session()
        a = adapter or requests.adapters.HTTPAdapter()
        s.mount('http://', a)
        s.mount('https://', a)
        return (s.get)(url, *_a, **_HttpTool__k)

    @classmethod
    def url_retries2httpr(cls, url, max_retries):
        adapter = requests.adapters.HTTPAdapter(max_retries=max_retries)
        return cls.url2httpr(url, adapter=adapter)


class HttprTool:

    @classmethod
    def httpr2status_code(cls, httpr):
        return httpr.status_code

    @classmethod
    def httpr2is_ok(cls, httpr):
        return httpr.ok

    @classmethod
    def request2curl(cls, request):
        command = "curl -X {method} -H {headers} -d '{data}' '{uri}'"
        method = request.method
        uri = request.url
        data = request.body
        headers = ['"{0}: {1}"'.format(k, v) for k, v in request.headers.items()]
        headers = ' -H '.join(headers)
        return command.format(method=method, headers=headers, data=data, uri=uri)