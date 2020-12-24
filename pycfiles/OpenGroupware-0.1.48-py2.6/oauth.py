# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/twitter/api/oauth.py
# Compiled at: 2012-10-12 07:02:39
import cgi, urllib, time, random, urlparse, hmac, binascii
VERSION = '1.0'
HTTP_METHOD = 'GET'
SIGNATURE_METHOD = 'PLAINTEXT'

class OAuthError(RuntimeError):

    def __init__(self, message='OAuth error occured.'):
        self.message = message


def build_authenticate_header(realm=''):
    return {'WWW-Authenticate': 'OAuth realm="%s"' % realm}


def escape(s):
    return urllib.quote(s, safe='~')


def generate_timestamp():
    return int(time.time())


def generate_nonce(length=8):
    return ('').join([ str(random.randint(0, 9)) for i in range(length) ])


class OAuthConsumer(object):
    key = None
    secret = None

    def __init__(self, key, secret):
        self.key = key
        self.secret = secret


class OAuthToken(object):
    key = None
    secret = None

    def __init__(self, key, secret):
        self.key = key
        self.secret = secret

    def to_string(self):
        return urllib.urlencode({'oauth_token': self.key, 'oauth_token_secret': self.secret})

    def from_string(s):
        params = cgi.parse_qs(s, keep_blank_values=False)
        key = params['oauth_token'][0]
        secret = params['oauth_token_secret'][0]
        return OAuthToken(key, secret)

    from_string = staticmethod(from_string)

    def __str__(self):
        return self.to_string()


class OAuthRequest(object):
    """
    OAuth parameters:
        - oauth_consumer_key 
        - oauth_token
        - oauth_signature_method
        - oauth_signature 
        - oauth_timestamp 
        - oauth_nonce
        - oauth_version
        ... any additional parameters, as defined by the Service Provider.
    """
    parameters = None
    http_method = HTTP_METHOD
    http_url = None
    version = VERSION

    def __init__(self, http_method=HTTP_METHOD, http_url=None, parameters=None):
        self.http_method = http_method
        self.http_url = http_url
        self.parameters = parameters or {}

    def set_parameter(self, parameter, value):
        self.parameters[parameter] = value

    def get_parameter(self, parameter):
        try:
            return self.parameters[parameter]
        except:
            raise OAuthError('Parameter not found: %s' % parameter)

    def _get_timestamp_nonce(self):
        return (self.get_parameter('oauth_timestamp'), self.get_parameter('oauth_nonce'))

    def get_nonoauth_parameters(self):
        parameters = {}
        for (k, v) in self.parameters.iteritems():
            if k.find('oauth_') < 0:
                parameters[k] = v

        return parameters

    def to_header(self, realm=''):
        auth_header = 'OAuth realm="%s"' % realm
        if self.parameters:
            for (k, v) in self.parameters.iteritems():
                if k[:6] == 'oauth_':
                    auth_header += ', %s="%s"' % (k, escape(str(v)))

        return {'Authorization': auth_header}

    def to_postdata(self):
        return ('&').join([ '%s=%s' % (escape(str(k)), escape(str(v))) for (k, v) in self.parameters.iteritems() ])

    def to_url(self):
        return '%s?%s' % (self.get_normalized_http_url(), self.to_postdata())

    def get_normalized_parameters(self):
        params = self.parameters
        try:
            del params['oauth_signature']
        except:
            pass

        key_values = params.items()
        key_values.sort()
        return ('&').join([ '%s=%s' % (escape(str(k)), escape(str(v))) for (k, v) in key_values ])

    def get_normalized_http_method(self):
        return self.http_method.upper()

    def get_normalized_http_url(self):
        parts = urlparse.urlparse(self.http_url)
        url_string = '%s://%s%s' % (parts[0], parts[1], parts[2])
        return url_string

    def sign_request(self, signature_method, consumer, token):
        self.set_parameter('oauth_signature_method', signature_method.get_name())
        self.set_parameter('oauth_signature', self.build_signature(signature_method, consumer, token))

    def build_signature(self, signature_method, consumer, token):
        return signature_method.build_signature(self, consumer, token)

    def from_request(http_method, http_url, headers=None, parameters=None, query_string=None):
        if parameters is None:
            parameters = {}
        if headers and 'Authorization' in headers:
            auth_header = headers['Authorization']
            if auth_header.index('OAuth') > -1:
                try:
                    header_params = OAuthRequest._split_header(auth_header)
                    parameters.update(header_params)
                except:
                    raise OAuthError('Unable to parse OAuth parameters from Authorization header.')

        if query_string:
            query_params = OAuthRequest._split_url_string(query_string)
            parameters.update(query_params)
        param_str = urlparse.urlparse(http_url)[4]
        url_params = OAuthRequest._split_url_string(param_str)
        parameters.update(url_params)
        if parameters:
            return OAuthRequest(http_method, http_url, parameters)
        else:
            return

    from_request = staticmethod(from_request)

    def from_consumer_and_token(oauth_consumer, token=None, http_method=HTTP_METHOD, http_url=None, parameters=None):
        if not parameters:
            parameters = {}
        defaults = {'oauth_consumer_key': oauth_consumer.key, 'oauth_timestamp': generate_timestamp(), 
           'oauth_nonce': generate_nonce(), 
           'oauth_version': OAuthRequest.version}
        defaults.update(parameters)
        parameters = defaults
        if token:
            parameters['oauth_token'] = token.key
        return OAuthRequest(http_method, http_url, parameters)

    from_consumer_and_token = staticmethod(from_consumer_and_token)

    def from_token_and_callback(token, callback=None, http_method=HTTP_METHOD, http_url=None, parameters=None):
        if not parameters:
            parameters = {}
        parameters['oauth_token'] = token.key
        if callback:
            parameters['oauth_callback'] = callback
        return OAuthRequest(http_method, http_url, parameters)

    from_token_and_callback = staticmethod(from_token_and_callback)

    def _split_header(header):
        params = {}
        parts = header.split(',')
        for param in parts:
            if param.find('OAuth realm') > -1:
                continue
            param = param.strip()
            param_parts = param.split('=', 1)
            params[param_parts[0]] = urllib.unquote(param_parts[1].strip('"'))

        return params

    _split_header = staticmethod(_split_header)

    def _split_url_string(param_str):
        parameters = cgi.parse_qs(param_str, keep_blank_values=False)
        for (k, v) in parameters.iteritems():
            parameters[k] = urllib.unquote(v[0])

        return parameters

    _split_url_string = staticmethod(_split_url_string)


class OAuthServer(object):
    timestamp_threshold = 300
    version = VERSION
    signature_methods = None
    data_store = None

    def __init__(self, data_store=None, signature_methods=None):
        self.data_store = data_store
        self.signature_methods = signature_methods or {}

    def set_data_store(self, oauth_data_store):
        self.data_store = data_store

    def get_data_store(self):
        return self.data_store

    def add_signature_method(self, signature_method):
        self.signature_methods[signature_method.get_name()] = signature_method
        return self.signature_methods

    def fetch_request_token(self, oauth_request):
        try:
            token = self._get_token(oauth_request, 'request')
        except OAuthError:
            version = self._get_version(oauth_request)
            consumer = self._get_consumer(oauth_request)
            self._check_signature(oauth_request, consumer, None)
            token = self.data_store.fetch_request_token(consumer)

        return token

    def fetch_access_token(self, oauth_request):
        version = self._get_version(oauth_request)
        consumer = self._get_consumer(oauth_request)
        token = self._get_token(oauth_request, 'request')
        self._check_signature(oauth_request, consumer, token)
        new_token = self.data_store.fetch_access_token(consumer, token)
        return new_token

    def verify_request(self, oauth_request):
        version = self._get_version(oauth_request)
        consumer = self._get_consumer(oauth_request)
        token = self._get_token(oauth_request, 'access')
        self._check_signature(oauth_request, consumer, token)
        parameters = oauth_request.get_nonoauth_parameters()
        return (consumer, token, parameters)

    def authorize_token(self, token, user):
        return self.data_store.authorize_request_token(token, user)

    def get_callback(self, oauth_request):
        return oauth_request.get_parameter('oauth_callback')

    def build_authenticate_header(self, realm=''):
        return {'WWW-Authenticate': 'OAuth realm="%s"' % realm}

    def _get_version(self, oauth_request):
        try:
            version = oauth_request.get_parameter('oauth_version')
        except:
            version = VERSION

        if version and version != self.version:
            raise OAuthError('OAuth version %s not supported.' % str(version))
        return version

    def _get_signature_method(self, oauth_request):
        try:
            signature_method = oauth_request.get_parameter('oauth_signature_method')
        except:
            signature_method = SIGNATURE_METHOD

        try:
            signature_method = self.signature_methods[signature_method]
        except:
            signature_method_names = (', ').join(self.signature_methods.keys())
            raise OAuthError('Signature method %s not supported try one of the following: %s' % (signature_method, signature_method_names))

        return signature_method

    def _get_consumer(self, oauth_request):
        consumer_key = oauth_request.get_parameter('oauth_consumer_key')
        if not consumer_key:
            raise OAuthError('Invalid consumer key.')
        consumer = self.data_store.lookup_consumer(consumer_key)
        if not consumer:
            raise OAuthError('Invalid consumer.')
        return consumer

    def _get_token(self, oauth_request, token_type='access'):
        token_field = oauth_request.get_parameter('oauth_token')
        token = self.data_store.lookup_token(token_type, token_field)
        if not token:
            raise OAuthError('Invalid %s token: %s' % (token_type, token_field))
        return token

    def _check_signature(self, oauth_request, consumer, token):
        (timestamp, nonce) = oauth_request._get_timestamp_nonce()
        self._check_timestamp(timestamp)
        self._check_nonce(consumer, token, nonce)
        signature_method = self._get_signature_method(oauth_request)
        try:
            signature = oauth_request.get_parameter('oauth_signature')
        except:
            raise OAuthError('Missing signature.')

        valid_sig = signature_method.check_signature(oauth_request, consumer, token, signature)
        if not valid_sig:
            (key, base) = signature_method.build_signature_base_string(oauth_request, consumer, token)
            raise OAuthError('Invalid signature. Expected signature base string: %s' % base)
        built = signature_method.build_signature(oauth_request, consumer, token)

    def _check_timestamp(self, timestamp):
        timestamp = int(timestamp)
        now = int(time.time())
        lapsed = now - timestamp
        if lapsed > self.timestamp_threshold:
            raise OAuthError('Expired timestamp: given %d and now %s has a greater difference than threshold %d' % (timestamp, now, self.timestamp_threshold))

    def _check_nonce(self, consumer, token, nonce):
        nonce = self.data_store.lookup_nonce(consumer, token, nonce)
        if nonce:
            raise OAuthError('Nonce already used: %s' % str(nonce))


class OAuthClient(object):
    consumer = None
    token = None

    def __init__(self, oauth_consumer, oauth_token):
        self.consumer = oauth_consumer
        self.token = oauth_token

    def get_consumer(self):
        return self.consumer

    def get_token(self):
        return self.token

    def fetch_request_token(self, oauth_request):
        raise NotImplementedError

    def fetch_access_token(self, oauth_request):
        raise NotImplementedError

    def access_resource(self, oauth_request):
        raise NotImplementedError


class OAuthDataStore(object):

    def lookup_consumer(self, key):
        raise NotImplementedError

    def lookup_token(self, oauth_consumer, token_type, token_token):
        raise NotImplementedError

    def lookup_nonce(self, oauth_consumer, oauth_token, nonce, timestamp):
        raise NotImplementedError

    def fetch_request_token(self, oauth_consumer):
        raise NotImplementedError

    def fetch_access_token(self, oauth_consumer, oauth_token):
        raise NotImplementedError

    def authorize_request_token(self, oauth_token, user):
        raise NotImplementedError


class OAuthSignatureMethod(object):

    def get_name(self):
        raise NotImplementedError

    def build_signature_base_string(self, oauth_request, oauth_consumer, oauth_token):
        raise NotImplementedError

    def build_signature(self, oauth_request, oauth_consumer, oauth_token):
        raise NotImplementedError

    def check_signature(self, oauth_request, consumer, token, signature):
        built = self.build_signature(oauth_request, consumer, token)
        return built == signature


class OAuthSignatureMethod_HMAC_SHA1(OAuthSignatureMethod):

    def get_name(self):
        return 'HMAC-SHA1'

    def build_signature_base_string(self, oauth_request, consumer, token):
        sig = (
         escape(oauth_request.get_normalized_http_method()),
         escape(oauth_request.get_normalized_http_url()),
         escape(oauth_request.get_normalized_parameters()))
        key = '%s&' % escape(consumer.secret)
        if token:
            key += escape(token.secret)
        raw = ('&').join(sig)
        return (key, raw)

    def build_signature(self, oauth_request, consumer, token):
        (key, raw) = self.build_signature_base_string(oauth_request, consumer, token)
        try:
            import hashlib
            hashed = hmac.new(key, raw, hashlib.sha1)
        except:
            import sha
            hashed = hmac.new(key, raw, sha)

        return binascii.b2a_base64(hashed.digest())[:-1]


class OAuthSignatureMethod_PLAINTEXT(OAuthSignatureMethod):

    def get_name(self):
        return 'PLAINTEXT'

    def build_signature_base_string(self, oauth_request, consumer, token):
        sig = escape(consumer.secret) + '&'
        if token:
            sig = sig + escape(token.secret)
        return sig

    def build_signature(self, oauth_request, consumer, token):
        return self.build_signature_base_string(oauth_request, consumer, token)