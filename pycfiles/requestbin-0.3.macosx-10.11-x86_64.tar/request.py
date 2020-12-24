# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/requestbin/request.py
# Compiled at: 2016-09-29 06:06:37
"""
Request module
"""
from tools import pathjoin

class Request(object):
    path = 'requests'

    def __init__(self, bin=None, body={}, content_length=0, content_type='', form_data={}, headers={}, id='', method='', path='/', query_string={}, remote_addr='', time=None, **kwargs):
        self.bin = bin
        self.body = body
        self.content_length = content_length
        self.content_type = content_type
        self.form_data = form_data
        self.headers = headers
        self.id = id
        self.method = method
        self.path = path
        self.query_string = query_string
        self.remote_addr = remote_addr
        self.time = time

    @classmethod
    def from_response(cls, response, bin=None):
        assert 200 <= response.status_code < 400, response.reason
        data = response.json()
        if type(data) == list:
            ret = list()
            for item in data:
                ret.append(cls(bin=bin, **item))

            return ret
        return cls(bin=bin, **data)

    @property
    def api_url(self):
        """return the api url of this request"""
        return pathjoin(Request.path, self.id, url=self.bin.api_url)