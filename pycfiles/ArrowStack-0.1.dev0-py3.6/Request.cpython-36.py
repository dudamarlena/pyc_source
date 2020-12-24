# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/arrow/Request.py
# Compiled at: 2018-09-05 11:48:44
# Size of source mod 2**32: 674 bytes
import webob, json

class Request(object):

    def __init__(self, environ):
        self.webob_request = webob.Request(environ)

    def method(self):
        return self.webob_request.method

    def path(self):
        return self.webob_request.path

    def params(self):
        return self.webob_request.params

    def param(self, name, placeholder=None):
        return self.webob_request.params.get(name, placeholder)

    def header(self, name, placeholder=None):
        return self.webob_request.headers.get(name, placeholder)

    def json(self):
        try:
            return json.loads(self.webob_request.body)
        except:
            return