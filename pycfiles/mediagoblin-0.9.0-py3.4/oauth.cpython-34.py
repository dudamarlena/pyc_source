# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mediagoblin/oauth/oauth.py
# Compiled at: 2016-03-29 15:18:42
# Size of source mod 2**32: 7099 bytes
import datetime
from oauthlib.common import Request
from oauthlib.oauth1 import RequestValidator
from mediagoblin import oauth
from mediagoblin.db.models import NonceTimestamp, Client, RequestToken, AccessToken

class GMGRequestValidator(RequestValidator):
    enforce_ssl = False

    def __init__(self, data=None, *args, **kwargs):
        self.POST = data
        super(GMGRequestValidator, self).__init__(*args, **kwargs)

    def check_nonce(self, nonce):
        """
        This checks that the nonce given is a valid nonce

        RequestValidator.check_nonce checks that it's between a maximum and
        minimum length which, not only does pump.io not do this from what
        I can see but there is nothing in rfc5849 which suggests a maximum or
        minium length should be required so I'm removing that check
        """
        return set(nonce) <= self.safe_characters

    def save_request_token(self, token, request):
        """ Saves request token in db """
        client_id = self.POST['oauth_consumer_key']
        request_token = RequestToken(token=token['oauth_token'], secret=token['oauth_token_secret'])
        request_token.client = client_id
        if 'oauth_callback' in self.POST:
            request_token.callback = self.POST['oauth_callback']
        request_token.save()

    def save_verifier(self, token, verifier, request):
        """ Saves the oauth request verifier """
        request_token = RequestToken.query.filter_by(token=token).first()
        request_token.verifier = verifier['oauth_verifier']
        request_token.save()

    def save_access_token(self, token, request):
        """ Saves access token in db """
        access_token = AccessToken(token=token['oauth_token'], secret=token['oauth_token_secret'])
        access_token.request_token = request.oauth_token
        request_token = RequestToken.query.filter_by(token=request.oauth_token).first()
        access_token.actor = request_token.actor
        access_token.save()

    def get_realms(*args, **kwargs):
        """ Currently a stub - called when making AccessTokens """
        return list()

    def validate_timestamp_and_nonce(self, client_key, timestamp, nonce, request, request_token=None, access_token=None):
        try:
            timestamp = datetime.datetime.fromtimestamp(float(timestamp))
        except ValueError:
            return False

        nc = NonceTimestamp.query.filter_by(timestamp=timestamp, nonce=nonce)
        nc = nc.first()
        if nc is None:
            return True
        return False

    def validate_client_key(self, client_key, request):
        """ Verifies client exists with id of client_key """
        client_query = Client.query.filter(Client.id != oauth.DUMMY_CLIENT_ID)
        client = client_query.filter_by(id=client_key).first()
        if client is None:
            return False
        return True

    def validate_verifier(self, token, verifier):
        """ Verifies the verifier token is correct. """
        request_token = RequestToken.query.filter_by(token=token).first()
        if request_token is None:
            return False
        if request_token.verifier != verifier:
            return False
        return True

    def validate_access_token(self, client_key, token, request):
        """ Verifies token exists for client with id of client_key """
        client_query = Client.query.filter(Client.id != oauth.DUMMY_CLIENT_ID)
        client = client_query.filter_by(id=client_key).first()
        if client is None:
            return False
        access_token_query = AccessToken.query.filter(AccessToken.token != oauth.DUMMY_ACCESS_TOKEN)
        access_token = access_token_query.filter_by(token=token).first()
        if access_token is None:
            return False
        request_token_query = RequestToken.query.filter(RequestToken.token != oauth.DUMMY_REQUEST_TOKEN, RequestToken.token == access_token.request_token)
        request_token = request_token_query.first()
        if client.id != request_token.client:
            return False
        return True

    def validate_realms(self, *args, **kwargs):
        """ Would validate reals however not using these yet. """
        return True

    def get_client_secret(self, client_key, request):
        """ Retrives a client secret with from a client with an id of client_key """
        client = Client.query.filter_by(id=client_key).first()
        return client.secret

    def get_access_token_secret(self, client_key, token, request):
        access_token = AccessToken.query.filter_by(token=token).first()
        return access_token.secret

    @property
    def dummy_client(self):
        return oauth.DUMMY_CLIENT_ID

    @property
    def dummy_request_token(self):
        return oauth.DUMMY_REQUEST_TOKEN

    @property
    def dummy_access_token(self):
        return oauth.DUMMY_ACCESS_TOKEN


class GMGRequest(Request):
    __doc__ = '\n        Fills in data to produce a oauth.common.Request object from a\n        werkzeug Request object\n    '

    def __init__(self, request, *args, **kwargs):
        """
            :param request: werkzeug request object

            any extra params are passed to oauthlib.common.Request object
        """
        kwargs['uri'] = kwargs.get('uri', request.url)
        kwargs['http_method'] = kwargs.get('http_method', request.method)
        kwargs['body'] = kwargs.get('body', request.data)
        kwargs['headers'] = kwargs.get('headers', dict(request.headers))
        super(GMGRequest, self).__init__(*args, **kwargs)