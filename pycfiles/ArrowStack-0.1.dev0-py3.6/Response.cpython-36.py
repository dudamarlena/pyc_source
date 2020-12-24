# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/arrow/Response.py
# Compiled at: 2018-09-05 11:51:56
# Size of source mod 2**32: 1712 bytes
import webob, json

class Response(webob.Response):

    def __init__(self):
        self.webob_response = webob.Response()
        self._body = ''

    def header(self, name, value=None):
        if value:
            self.webob_response.headers[name] = value
        else:
            return self.webob_response.headers.get(name)

    def headers(self, data=None):
        if data:
            self.webob_response.headers = data
        else:
            return self.webob_response.headers

    def headerlist(self, data=None):
        if data:
            self.webob_response.headerlist = data
        else:
            return self.webob_response.headerlist

    def add(self, data):
        self.set_body(self.body() + data)

    def body(self, data=None):
        if data:
            self.set_body(data)
        else:
            return self.body

    def json(self, data=None):
        if data:
            self.set_body(json.dumps(data))
        else:
            return json.loads(self.body())

    def status(self, data=None):
        if data:
            self.webob_response.status = data
        else:
            return self.webob_response.status

    def status_code(self, data=None):
        if data:
            self.webob_response.status = data
        else:
            return self.webob_response.status_code

    def binary(self):
        return self.webob_response.body

    def set_body(self, new_body):
        self._body = new_body
        self.webob_response.text = new_body

    def set_cookie(self, *args, **kwargs):
        (self.webob_response.set_cookie)(*args, **kwargs)

    def delete_cookie(self, *args, **kwargs):
        (self.webob_response.delete_cookie)(*args, **kwargs)