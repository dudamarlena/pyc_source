# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoli/PycharmProjects/iqiyi/venv/lib/python2.7/site-packages/iqiyiop/BaiduCoreRequest.py
# Compiled at: 2018-11-18 22:17:03
__author__ = 'luoli'
import abc

class AcsRequest:
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self._query_params = {}
        self._header_params = {}
        self._add_request_params = {}
        self._uri_params = {}
        self.__uri = None
        return

    def get_query_params(self):
        return self._query_params

    def add_header_params(self, k, v):
        if self._header_params is None:
            self._header_params = {}
        else:
            self._header_params[k] = v
        return

    def add_request_params(self, k, v):
        if self._add_request_params is None:
            self._add_request_params = {}
        else:
            self._header_params[k] = v
        return

    def get_header_params(self):
        return self._header_params

    def get_uri_params(self):
        return self._uri_params

    def get_uri(self):
        uid = self._uri_params['uid']
        item = self._uri_params['item']
        uri = '/json-api/v1/metricdata/%s/BCE_BCC/%s' % (uid, item)
        return uri


class IqiyiOpRequest(AcsRequest):

    def __init__(self, endpoint):
        AcsRequest.__init__(self)
        self.add_header_params('Content-Type', 'application/json')
        self.add_header_params('Expect', '100-continue')
        self.add_header_params('Host', endpoint)

    def add_query_params(self, k, v):
        if self._query_params is None:
            self._query_params = {}
        else:
            self._query_params[k] = v
        return

    def add_uri_params(self, k, v):
        if self._uri_params is None:
            self._uri_params = {}
        else:
            self._uri_params[k] = v
        return