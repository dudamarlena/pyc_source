# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/dotcloud/client/auth.py
# Compiled at: 2012-09-19 14:56:08
import json, requests
from requests.auth import HTTPBasicAuth

class BaseAuth(object):

    def args_hook(self, args):
        pass

    def pre_request_hook(self, request):
        pass

    def response_hook(self, response):
        pass


class NullAuth(BaseAuth):
    pass


class BasicAuth(BaseAuth):

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def args_hook(self, args):
        args['auth'] = HTTPBasicAuth(self.username, self.password)


class OAuth2Auth(BaseAuth):

    def __init__(self, access_token=None, refresh_token=None, scope=None, client_id=None, client_secret=None, token_url=None):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.scope = scope
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_url = token_url
        self._retry_count = 0

    def pre_request_hook(self, request):
        request.headers.setdefault('Authorization', ('Bearer {0}').format(self.access_token))

    def response_hook(self, response):
        if response.status_code == requests.codes.unauthorized:
            if self._retry_count >= 1:
                return
            self._retry_count += 1
            if self.refresh_credentials():
                response.request.send(anyway=True)
                return response.request.response

    def refresh_credentials(self):
        data = {'grant_type': 'refresh_token', 'refresh_token': self.refresh_token, 
           'client_id': self.client_id, 
           'client_secret': self.client_secret, 
           'scope': self.scope or ''}
        if hasattr(self, 'pre_refresh_callback'):
            self.pre_refresh_callback(data)
        res = requests.post(self.token_url, data=data)
        res.raise_for_status()
        if not res.ok:
            return False
        data = json.loads(res.text)
        if data.get('access_token'):
            self.access_token = data['access_token']
            self.refresh_token = data['refresh_token']
            if hasattr(self, 'post_refresh_callback'):
                return self.post_refresh_callback(data)
        return False