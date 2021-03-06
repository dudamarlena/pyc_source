# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/webapptitude/httpauth.py
# Compiled at: 2016-08-31 16:32:16
"""
A library to support HTTP DIGEST authentication on Google AppEngine.

This provides substantial support for RFCs 2069 and 2617, with few exceptions.
Notably is does not currently support "algorithm=MD5-sess" or "qop=auth-int",
however these are signaled in the server response, so most clients should be
quite compatible. (Some browsers doesn't support these anyway.)
See also: https://en.wikipedia.org/wiki/Digest_access_authentication

Provides classes:

- DigestAuthenticatedRequestHandler(webapp2.RequestHandler)
- Authorization(webapp2_extras.appengine.auth.models.User)

"""
from google.appengine.ext import ndb
from webapp2_extras.appengine import auth
from webapp2_extras.appengine.auth.models import User
import hashlib, random, time, os, re, webapp2, datetime, logging
from util import base62encode
from handlers import RequestHandler
from handlers import augment
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())
ONE_DAY = 86400
TWO_WEEKS = 1209600
ONE_MONTH = 2592000
ONE_YEAR = 31536000
RE_AUTHPARAM_PARSE = re.compile('([a-z]+)="([^"]*)"(?:,\\s)?')
DEFAULT_NONCE_PEPPER = '$0Z8kl23b81lknakdjfakj_al3joiqnb./13joi'

def epoch_seconds(dt):
    """Calculate the Unix Epoch value of a timestamp."""
    return (dt - datetime.datetime.utcfromtimestamp(0)).total_seconds()


def md5(text):
    return hashlib.md5(text).hexdigest()


class NONCE(ndb.Expando):
    """A single-use token for signatures."""
    pepper = os.environ.get('NONCE_PEPPER', DEFAULT_NONCE_PEPPER)
    nonce_text = ndb.StringProperty(indexed=True)
    expires_ts = ndb.DateTimeProperty(required=False)

    def __str__(self):
        """Coerce to string properly."""
        expires_ts = epoch_seconds(self.expires_ts)
        return '%d:%s' % (expires_ts, self.nonce_text)

    @property
    def expired(self):
        return not self.still_valid()

    def still_valid(self):
        return self.expires_ts > datetime.datetime.now()

    @classmethod
    def generate(cls, expiration=3600, spread=30, **params):
        """Produce a new NONCE from a series of values."""
        numbrand = int(time.time()) + random.randint(2, 1e+16)
        expiration = int(time.time() + expiration)
        if isinstance(spread, int):
            expiration += random.randint(-1 * spread, spread)
        checksum = hashlib.md5(base62encode(numbrand))
        checksum.update(base62encode(expiration))
        parts = [ '%s:%s' % (i, repr(v)) for i, v in params.items() ]
        checksum.update((';').join(parts))
        checksum.update(cls.pepper)
        nonce = cls(nonce_text=checksum.hexdigest(), expires_ts=datetime.datetime.utcfromtimestamp(expiration))
        nonce.put()
        return nonce

    @classmethod
    def find(cls, full_nonce):
        """Find a matching NONCE if not yet expired."""
        try:
            expires_ts, rand_text = full_nonce.split(':')
            result = cls.query(cls.nonce_text == rand_text).get()
            if result is not None:
                expires_ts = int(expires_ts)
                expires_ts = datetime.datetime.utcfromtimestamp(expires_ts)
                if expires_ts != result.expires_ts:
                    return
            return result
        except:
            return

        return

    @classmethod
    def allowed(cls, full_nonce):
        """
        Assess whether a given NONCE value is still valid.

        Upon evaluation, the NONCE is considered expired. A given NONCE can
        only be evaluated once. (Hence the name.)
        """
        found = cls.find(full_nonce)
        if isinstance(found, cls):
            is_valid = bool(found.still_valid())
            found.key.delete()
            return is_valid
        else:
            return False


class Authorization(User):
    """Datastore model for Digest authorization records."""
    http_username_auth_id_prefix = 'digest:'
    digest = ndb.PickleProperty(default={})

    @classmethod
    def get_by_http_username(cls, username):
        """Convenience method with similar convention to {auth.models.User}."""
        exist = cls.get_by_auth_id(cls.http_username_auth_id_prefix + username)
        if not exist:
            exist = cls.create_digest_auth_user(username)
        return exist

    @classmethod
    def create_digest_auth_user(cls, username):
        return cls.create_user(cls.http_username_auth_id_prefix + username)

    def store_digest(self, username, password_raw, *realms):
        """Store the checksum of specific (known-good) credentials."""
        auth_id = self.http_username_auth_id_prefix + username
        if auth_id not in self.auth_ids:
            self.add_auth_id(auth_id)
        realms = [ q for q in realms if isinstance(q, basestring) ]
        if not len(realms):
            realms = self.digest.keys()
        for k in realms:
            checksum = md5(username + ':' + k + ':' + password_raw)
            self.digest[k] = checksum

        self.put()

    def check_digest(self, realm, method, uri, **props):
        """
        Validate the particulars of a request digest.

        See also: https://en.wikipedia.org/wiki/Digest_access_authentication
        """
        if realm not in self.digest:
            return False
        nonce = props.get('nonce')
        nonce_valid = NONCE.allowed(nonce)
        if not nonce_valid:
            return False
        response = props.get('response')
        if props.get('qop') in ('auth', ):
            parts = [self.digest[realm], nonce]
            for i in ('nc', 'cnonce', 'qop'):
                parts.append(props.get(i))

            parts.append(md5(method + ':' + uri))
        else:
            parts = [
             self.digest[realm], nonce, md5(method + ':' + uri)]
        result = md5((':').join(parts))
        success = result == response
        return success


class DigestAuthenticatedRequestHandler(RequestHandler):
    """Integrates HTTP Digest authentication (when configured)."""

    def prompt_header(self, **values):
        """Generate the full header definition to request authentication."""
        formatted = (', ').join(self.prompt_header_format).format(**values)
        return ('WWW-Authenticate', formatted)

    @property
    def prompt_header_format(self):
        """Generate the template of a request for authentication."""
        yield 'Digest realm="{realm}"'
        yield 'algorithm="MD5", qop="auth"'
        yield 'nonce="{nonce}"'
        yield 'opaque="{opaque}"'

    @webapp2.cached_property
    def request_digest(self):
        """Extract authorization digest (if it looks like a digest)."""
        reqauth = self.request.authorization
        if reqauth is None:
            return
        else:
            if isinstance(reqauth, tuple) and reqauth[0] == 'Digest':
                return reqauth[1]
            else:
                return

            return

    @property
    def opaque(self):
        """Generate a new opaque value and store it in session."""
        if 'opaque' not in self.session:
            checksum = hashlib.md5(self.application_id)
            checksum.update(self.request.remote_addr)
            checksum.update(str(random.randint(0, 100000000000.0)))
            self.session['opaque'] = checksum.hexdigest()
        return self.session['opaque']

    def generate_nonce(self, expiration=3600, **props):
        """A simple wrapper for mock classes to override."""
        return str(NONCE.generate(expiration=expiration, **props))

    def authenticate_user(self, realm, method, uri, **props):
        """Attempt to validate the user per their current digest."""
        reqauth = Authorization.get_by_http_username(props.get('username'))
        if auth is not None:
            result = reqauth.check_digest(realm, method, uri, **props)
            return bool(result)
        else:
            return False
            return

    def inject_response_header(self, realm, cause=None):
        """Request user to authenticate (i.e. the appropriate headers)."""
        nonce = self.generate_nonce(expiration=300, ip=self.request.remote_addr, app=self.application_id)
        opaque = self.opaque
        header, value = self.prompt_header(realm=realm, nonce=nonce, opaque=opaque)
        self.response.headers.add_header(header, value)

    def require_auth(self, realm, callback, args, kwargs):
        """
        Validate user's authentication before running callback.

        Wraps the callback with authentication controls.
        """
        props = self.request_digest
        failed = False
        cause = None
        if props is None:
            failed = True
            cause = 'Digest properties not found'
        else:
            params = ('response', 'nonce', 'username', 'cnonce', 'nc', 'qop', 'algorithm')
            params = dict([ (i, props.get(i, None)) for i in params ])
            if 'username' not in params:
                failed = True
                cause = 'Username not provided'
            if props.get('uri', None) != self.request.path:
                failed = True
                cause = 'Mismatch request URI'
            method = self.request.method
            uri = self.request.path
            if props.get('opaque', None) != self.opaque:
                cause = 'Opaque mismatch'
                failed = True
            if props.get('realm', None) != realm:
                cause = 'Realm mismatch'
                failed = True
            elif not self.authenticate_user(realm, method, uri, **params):
                cause = 'Authentication mismatch'
                failed = True
        if failed:
            self.inject_response_header(realm, cause)
            self.response.set_status(401, 'Unauthorized')
        else:
            return callback(self, *args, **kwargs)
        return


def patch_request_method(request_func, _realm):
    """Wrap the request method with authorization validator."""

    def _wrapper(self, *args, **kwargs):
        instance = augment(self, DigestAuthenticatedRequestHandler)
        return instance.require_auth(_realm, request_func, args, kwargs)

    return _wrapper


def authenticate(_realm):
    """
    Decorator for RequestHandler methods.

    Usage:

        class xyz(webapp2.RequestHandler):

            @authenticate("mydomain.com") # method-specific
            def get(self):
                ...

    """

    def auth_wrapper(request_cls):
        if isinstance(request_cls, type(authenticate)):
            return patch_request_method(request_cls, _realm)
        raise TypeError('A request-handling method, on a webapp2.RequestHandler subclass must be patched.')

    return auth_wrapper