# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gmsdk/services.py
# Compiled at: 2015-04-06 14:01:01
import json
from requests import Request, Session
from requests.adapters import HTTPAdapter
from django.conf import settings
from gmsdk.connection import BaseConnection
from gmsdk.connection import HTTP_SSL

class AuthenticateAPIService(BaseConnection):
    """
    Input username and password.
    makes request to generate token.
    """

    def __init__(self, **kwargs):
        self.config.resp_format = 'json'
        super(AuthenticateAPIService, self).__init__(**kwargs)

    def generate_token(self, data):
        self.method = 'POST'
        self.config.uri = '/api-token-auth/'
        self.headers.update(**{'content-type': 'application/x-www-form-urlencoded', 
           'accept': 'application/json'})
        url = '%s://%s%s' % (
         HTTP_SSL[self.config.https],
         self.config.domain,
         self.config.uri)
        request = Request(self.method, url, data=data, headers=self.headers)
        self.request = request.prepare()
        self.response = self.session.send(self.request, verify=False, proxies=self.proxies, timeout=self.timeout, allow_redirects=True)
        f = json.loads(self.response.content)
        return f