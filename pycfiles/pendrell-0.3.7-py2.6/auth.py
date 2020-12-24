# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pendrell/auth.py
# Compiled at: 2010-10-05 15:28:43
import hashlib
from twisted.internet.defer import maybeDeferred
from zope.interface import Interface, Attribute, implements

class IAuthenticator(Interface):
    schemes = Attribute('Sequence of authentication schemes')
    secure = Attribute('True iff this authorization is plaintext-safe')

    def authorize(scheme, **params):
        """Generate an authorization string."""
        pass


class UserPassAuthenticatorBase(object):

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def authorize(self, scheme, **params):
        raise NotImplementedError()


class BasicAuthenticator(UserPassAuthenticatorBase):
    implements(IAuthenticator)
    schemes = ('Basic', )
    secure = False

    def authorize(self, scheme, **params):
        cred = '%s:%s' % (self.username, self.password)
        return ('{scheme} {params}').format(scheme=scheme, params=cred.encode('base64').replace('\n', ''))


class DigestAuthenticator(UserPassAuthenticatorBase):
    implements(IAuthenticator)
    schemes = ('Digest', )
    secure = True
    defaultAlgorithm = 'md5'

    def authorize(self, scheme, **params):
        """Compute the digested authentication token as specfied by RFC 2617.

        Arguments:
            params --  Dictionary with the following keys:
                algorithm [default: "md5"] --  Digest algorithm.
                realm --  Authentication realm as specified by the server.
                method --  Request method (e.g. GET, POST)
                uri --  URI of the requested resource.
                nonce --  Server-provided nonce value.
        """
        algorithm = params.get('algorithm', self.defaultAlgorithm).lower()
        realm = params['realm']
        method = params['method']
        uri = params['uri']
        nonce = params['nonce']
        rsp = self._generateResponse(algorithm, realm, method, uri, nonce)
        return ('{scheme} username="{username}", realm="{realm}", nonce="{nonce}", uri="{uri}", response="{rsp}"').format(scheme=scheme, username=self.username, realm=realm, nonce=nonce, uri=uri, rsp=rsp)

    def _generateResponse(self, algorithm, realm, method, uri, nonce):
        r1 = hashlib.new(algorithm, ('{0.username}:{1}:{0.password}').format(self, realm)).hexdigest()
        r2 = hashlib.new(algorithm, ('{0}:{1}').format(method, uri)).hexdigest()
        rsp = hashlib.new(algorithm, ('{0}:{1}:{2}').format(r1, nonce, r2)).hexdigest()
        return rsp