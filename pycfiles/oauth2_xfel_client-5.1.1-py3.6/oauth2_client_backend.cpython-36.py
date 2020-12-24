# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/oauth2_xfel_client/oauth2_client_backend.py
# Compiled at: 2019-08-12 09:08:21
# Size of source mod 2**32: 5506 bytes
import logging, sys
from datetime import datetime
from oauthlib.oauth2 import BackendApplicationClient
from requests import Timeout
from requests_oauthlib.oauth2_session import OAuth2Session
__author__ = 'Luis Maia <luis.maia@xfel.eu>'
__date__ = 'September 4, 2014'

class Oauth2ClientBackend(object):
    oauth_token = {}
    headers = {}
    session = None
    timeout = 3
    max_retries = 3

    def __init__(self, client_id, client_secret, scope, token_url, refresh_url, auth_url, session_token=None):
        self.oauth_config = {'client_id':client_id, 
         'client_secret':client_secret, 
         'scope':scope, 
         'token_url':token_url, 
         'refresh_url':refresh_url, 
         'auth_url':auth_url}
        cert_url = 'https://in.xfel.eu'
        self.ssl_verify = cert_url in self.oauth_config['token_url']
        self.client = BackendApplicationClient(client_id)
        self.auth_session(session_token=session_token)

    def auth_session(self, session_token=None):
        if self.is_session_token_dt_valid(session_token):
            self._re_used_existing_session_token(session_token)
        else:
            for attempt in range(self.max_retries):
                try:
                    logging.debug('Will try to create a new session token')
                    self._create_new_session_token()
                except Timeout:
                    logging.debug('Got an exception from the server: {0}'.format(sys.exc_info()[0]))
                    continue
                else:
                    logging.debug('Got a new session token successfully')
                    break

        return True

    def _re_used_existing_session_token(self, session_token):
        self.session = OAuth2Session(client_id=(self.oauth_config['client_id']),
          client=(self.client),
          token=session_token,
          auto_refresh_url=(self.oauth_config['refresh_url']),
          auto_refresh_kwargs=(self.oauth_config),
          token_updater=(self._Oauth2ClientBackend__token_saver(session_token)))

    def _create_new_session_token(self):
        self.session = OAuth2Session(client_id=(self.oauth_config['client_id']),
          client=(self.client))
        session_token = self.session.fetch_token((self.oauth_config['token_url']),
          client_id=(self.oauth_config['client_id']),
          client_secret=(self.oauth_config['client_secret']),
          timeout=(self.timeout),
          verify=(self.ssl_verify))
        self._Oauth2ClientBackend__token_saver(session_token)

    def check_session_token(self):
        if not self.is_session_token_valid():
            self._Oauth2ClientBackend__refresh_session_token()

    def get_session_token(self):
        return self.session.token

    def is_session_token_valid(self):
        current_token = self.get_session_token()
        return Oauth2ClientBackend.is_session_token_dt_valid(current_token)

    def __refresh_session_token(self):
        self.auth_session(session_token=(self.get_session_token()))

    def __token_saver(self, session_token):
        self.oauth_token['access_token'] = session_token['access_token']
        self.oauth_token['refresh_token'] = None
        self.oauth_token['token_type'] = 'bearer'
        self.oauth_token['expires_at'] = datetime.fromtimestamp(session_token['expires_at'])
        self.headers['Authorization'] = 'Bearer ' + session_token['access_token']

    @staticmethod
    def is_session_token_dt_valid(session_token, dt=None):
        if session_token and 'expires_at' in session_token:
            expires_dt = datetime.fromtimestamp(session_token['expires_at'])
            if dt is None:
                dt = datetime.now()
            return expires_dt > dt
        else:
            return False