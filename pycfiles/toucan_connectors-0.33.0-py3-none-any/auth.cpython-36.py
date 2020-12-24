# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/rachelle2/webprojects/toucan-connectors/toucan_connectors/auth.py
# Compiled at: 2020-04-08 11:34:17
# Size of source mod 2**32: 3127 bytes
from enum import Enum
from typing import List
import pyjq
from oauthlib.oauth2 import BackendApplicationClient
from pydantic import BaseModel, Field
from requests import Session
from requests.auth import AuthBase, HTTPBasicAuth, HTTPDigestAuth
from requests_oauthlib import OAuth1, OAuth2Session

def oauth2_backend(token_url, client_id, client_secret):
    oauthclient = BackendApplicationClient(client_id=client_id)
    oauthsession = OAuth2Session(client=oauthclient)
    token = oauthsession.fetch_token(token_url=token_url,
      client_id=client_id,
      client_secret=client_secret)
    return OAuth2Session(client_id=client_id, token=token)


class CustomTokenServer(AuthBase):
    __doc__ = '\n    Get a token from a request to a custom token server.\n    '

    def __init__(self, method, url, params=None, data=None, headers=None, auth=None, json=None, filter='.'):
        self.request_kwargs = {'method':method, 
         'url':url, 
         'params':params, 
         'data':data, 
         'headers':headers, 
         'json':json}
        self.auth = auth
        self.filter = filter

    def __call__(self, r):
        if self.auth:
            session = Auth(**self.auth).get_session()
        else:
            session = Session()
        res = (session.request)(**self.request_kwargs)
        token = pyjq.first(self.filter, res.json())
        r.headers['Authorization'] = f"Bearer {token}"
        return r


class AuthType(str, Enum):
    basic = 'basic'
    digest = 'digest'
    oauth1 = 'oauth1'
    oauth2_backend = 'oauth2_backend'
    custom_token_server = 'custom_token_server'


class Auth(BaseModel):
    type: AuthType = Field(...,
      description='As we rely on the python request lirary, we suggest that you refer to the dedicated <a href="https://2.python-requests.org/en/master/user/authentication/">documentation</a> for more details.',
      description_mimetype='text/html')
    args = Field(...,
      title='Positionnal arguments',
      description='For example for a basic authentication, you can provide your username and password here')
    args: List[str]
    kwargs: dict = Field(None,
      title='Named arguments',
      description='A JSON object with argument name as key and corresponding value as value')

    def get_session(self) -> Session:
        auth_class = {'basic':HTTPBasicAuth, 
         'digest':HTTPDigestAuth, 
         'oauth1':OAuth1, 
         'oauth2_backend':oauth2_backend, 
         'custom_token_server':CustomTokenServer}.get(self.type.value)
        kwargs = {} if not self.kwargs else self.kwargs
        auth_instance = auth_class(*self.args, **kwargs)
        if isinstance(auth_instance, Session):
            return auth_instance
        else:
            session = Session()
            session.auth = auth_instance
            return session