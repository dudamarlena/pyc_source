# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/parser_engine/request.py
# Compiled at: 2019-04-16 05:55:04
# Size of source mod 2**32: 2479 bytes
from scrapy.http.request import Request
import simplejson as json
from scrapy.http.request.form import FormRequest
from six.moves.urllib.parse import urlencode, urlparse
from .utils import is_url

class TaskRequest(dict):

    def __init__(self, url, method='GET', body=None, headers=None, cookies=None, meta=None, **kwargs):
        if not is_url(url):
            raise NotImplementedError(url)
        else:
            if headers is None:
                headers = {}
            else:
                if not body:
                    js = kwargs.pop('json', None)
                    if js:
                        if isinstance(js, dict):
                            body = json.dumps(js)
                        else:
                            body = js
                        if not headers.get('Content-Type'):
                            headers['Content-Type'] = 'application/json'
                    else:
                        form = kwargs.pop('form', None)
                        if form:
                            if not headers.get('Content-Type'):
                                headers['Content-Type'] = 'application/x-www-form-urlencoded'
                            if isinstance(form, dict):
                                body = urlencode(form)
                            else:
                                body = form
            super().__init__()
            if meta is None:
                meta = kwargs
        self.url = url
        self.method = method
        self.body = body
        self.headers = headers
        self.cookies = cookies
        self.meta = meta

    def __setattr__(self, key, value):
        self[key] = value

    def __getattr__(self, item):
        return self.get(item)


class JsonRequest(Request):

    def __init__(self, *args, **kwargs):
        jsondata = kwargs.pop('jsondata', None)
        if jsondata:
            if kwargs.get('method') is None:
                kwargs['method'] = 'POST'
        (super(JsonRequest, self).__init__)(*args, **kwargs)
        if jsondata:
            data = json.dumps(jsondata) if isinstance(jsondata, dict) else jsondata
            if self.method == 'POST':
                self.headers.setdefault(b'Content-Type', b'application/json')
                self._set_body(data)


def make_request(url, method='GET', formdata=None, jsondata=None, headers=None, **kwargs):
    if formdata:
        return FormRequest(url=url, method=method, formdata=formdata, headers=headers, **kwargs)
    else:
        if jsondata:
            return JsonRequest(url=url, method=method, jsondata=jsondata, headers=headers, **kwargs)
        return Request(url, method=method, headers=headers, **kwargs)