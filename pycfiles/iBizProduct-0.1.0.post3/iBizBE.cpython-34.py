# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\lrivera\Documents\Visual Studio 2013\Projects\iBizProduct-Python\iBizProduct-Python\src\iBizBE.py
# Compiled at: 2016-04-11 18:24:45
# Size of source mod 2**32: 1508 bytes
from __future__ import unicode_literals
import requests, os
from builtins import dict
from future.utils import raise_with_traceback

class iBizBE(object):
    _iBizBE__PRODUCTION_API = 'https://backend.ibizapi.com:8888'
    _iBizBE__STAGING_API = 'https://backendbeta.ibizapi.com:8888'

    def __init__(self, isDev, verifySSL):
        self._client_opts = dict(defaults=dict(verify=verifySSL))
        self._IsDev = isDev

    def getIsDev(self):
        return self._IsDev

    def setIsDev(self, value):
        self._IsDev = value

    IsDev = property(getIsDev, setIsDev)

    def call(self, endpoint, action='VIEW', params={}):
        uri = self.EndpointFormatter(self._IsDev, endpoint, action)
        return self.JsonCall(uri, params)

    def EndpointFormatter(self, isDev, endpoint, action):
        if isDev:
            return iBizBE._iBizBE__STAGING_API + '/JSON/' + endpoint + '?action=' + action
        else:
            return iBizBE._iBizBE__PRODUCTION_API + '/JSON/' + endpoint + '?action=' + action

    def JsonCall(self, uri, params):
        response = requests.post(url=uri, data=None, json=params, verify=self._client_opts.get('verify'))
        result = response.json()
        if response.status_code == 500:
            if result.get('error') != None:
                raise_with_traceback(ValueError(result.get('error')))
            else:
                raise_with_traceback(requests.exceptions.ContentDecodingError)
        return result