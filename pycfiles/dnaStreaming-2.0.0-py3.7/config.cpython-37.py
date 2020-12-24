# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/dnaStreaming/config.py
# Compiled at: 2020-05-12 03:20:35
# Size of source mod 2**32: 7484 bytes
from __future__ import absolute_import, division
import errno, json, os, requests

class Config(object):
    OAUTH_URL = 'https://accounts.dowjones.com/oauth2/v1/token'
    DEFAULT_HOST = 'https://api.dowjones.com'
    DEFAULT_CUST_CONFIG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), './customer_config.json'))
    ENV_VAR_SUBSCRIPTION_ID = 'SUBSCRIPTION_ID'
    ENV_VAR_USER_KEY = 'USER_KEY'
    ENV_VAR_SERVICE_ACCOUNT_ID = 'SERVICE_ACCOUNT_ID'
    ENV_VAR_USER_ID = 'USER_ID'
    ENV_VAR_CLIENT_ID = 'CLIENT_ID'
    ENV_VAR_PASSWORD = 'PASSWORD'
    ENV_VAR_EXTRACTION_API_HOST = 'EXTRACTION_API_HOST'

    def __init__(self, service_account_id=None, user_key=None, user_id=None, client_id=None, password=None):
        self.customer_config_path = self.DEFAULT_CUST_CONFIG_PATH
        self.initialized = False
        self.service_account_id = service_account_id
        self.user_key = user_key
        self.user_id = user_id
        self.client_id = client_id
        self.password = password
        self.headers = None

    def _initialize(self):
        self._validate()
        with open(self.customer_config_path, 'r') as (f):
            self.customer_config = json.load(f)
        self.initialized = True
        self.headers = None

    def _validate(self):
        if not os.path.isfile(self.customer_config_path):
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), self.customer_config_path)
        if not os.access(self.customer_config_path, os.R_OK):
            raise Exception("Encountered permission problem reading file from path '{}'.".format(self.customer_config_path))

    def get_headers(self):
        if self.headers:
            return self.headers
        self.headers = self.get_authentication_headers()
        return self.headers

    def get_authentication_headers(self):
        if self.oauth2_credentials():
            return {'Authorization': self._fetch_jwt()}
        user_key = self.get_user_key()
        if user_key:
            return {'user-key': user_key}
        msg = 'Could not find determine credentials:\n                Must specify account credentials as user_id, client_id, and password, either through env vars, customer_config.json, or as args to Listener constructor\n                (see README.rst)'
        raise Exception(msg)

    def _fetch_jwt(self):
        oauth2_credentials = self.oauth2_credentials()
        user_id = oauth2_credentials.get('user_id')
        client_id = oauth2_credentials.get('client_id')
        password = oauth2_credentials.get('password')
        body = {'username':user_id, 
         'client_id':client_id, 
         'password':password, 
         'connection':'service-account', 
         'grant_type':'password', 
         'scope':'openid service_account_id'}
        try:
            response = _get_requests().post((self.OAUTH_URL), data=body).json()
            body['scope'] = 'openid pib'
            body['grant_type'] = 'urn:ietf:params:oauth:grant-type:jwt-bearer'
            body['access_token'] = response.get('access_token')
            body['assertion'] = response.get('id_token')
            response = _get_requests().post((self.OAUTH_URL), data=body).json()
            return '{0} {1}'.format(response['token_type'], response['access_token'])
        except (KeyError, ValueError):
            msg = 'Unable to retrieve JWT with the given credentials:\n                User ID: {0}\n                Client ID: {1}\n                Password: {2}\n            '.format(user_id, client_id, password)
            raise Exception(msg)

    def get_uri_context(self):
        headers = self.get_headers()
        host = os.getenv(self.ENV_VAR_EXTRACTION_API_HOST, self.DEFAULT_HOST)
        if 'Authorization' in headers:
            return host + '/dna'
        if 'user-key' in headers:
            return host + '/alpha'
        msg = 'Could not determine user credentials:\n                Must specify account credentials as user_id, client_id, and password, either through env vars, customer_config.json, or as args to Listener constructor\n                (see README.rst)'
        raise Exception(msg)

    def oauth2_credentials(self):
        creds = self._build_oauth2_credentials(self.user_id, self.client_id, self.password)
        if not creds:
            creds = self._build_oauth2_credentials(os.getenv(self.ENV_VAR_USER_ID), os.getenv(self.ENV_VAR_CLIENT_ID), os.getenv(self.ENV_VAR_PASSWORD))
        if not creds:
            creds = self._oauth2_credentials_from_file()
        return creds

    def _oauth2_credentials_from_file(self):
        if not self.initialized:
            self._initialize()
        return self._build_oauth2_credentials(self.customer_config.get('user_id'), self.customer_config.get('client_id'), self.customer_config.get('password'))

    def _build_oauth2_credentials(self, user_id, client_id, password):
        if user_id:
            if client_id:
                if password:
                    return {'user_id':user_id, 
                     'client_id':client_id, 
                     'password':password}

    def get_user_key(self):
        user_key = self.user_key if self.user_key else self.service_account_id
        if user_key is None:
            user_key = os.getenv(self.ENV_VAR_USER_KEY, os.getenv(self.ENV_VAR_SERVICE_ACCOUNT_ID))
            if user_key is None:
                user_key = self._user_key_id_from_file()
        return user_key

    def _user_key_id_from_file(self):
        if not self.initialized:
            self._initialize()
        return self.customer_config.get('user_key', self.customer_config.get('service_account_id'))

    def subscription(self):
        if os.getenv(self.ENV_VAR_SUBSCRIPTION_ID) is not None:
            subscription = os.getenv(self.ENV_VAR_SUBSCRIPTION_ID)
        else:
            subscription = self._subscription_id_from_file()
        return subscription

    def _set_customer_config_path(self, path):
        self.customer_config_path = path
        self._initialize()

    def _subscription_id_from_file(self):
        if not self.initialized:
            self._initialize()
        return self.customer_config['subscription_id']


def _get_requests():
    return requests