# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/bridgedb/txrecaptcha.py
# Compiled at: 2015-11-05 10:40:17
__doc__ = 'Twisted-based reCAPTCHA client.\n\nThis client *always* uses TLS with strict hostname checking, unlike the\nofficial Google Python recaptcha-client_, which is hardcoded_ to use plaintext\nHTTP.\n\nSmall portions of this code were taken from the official Google Python\nrecaptcha-client_ module, version 1.0.6.  Those portions are\n:class:`RecaptchaResponse`, :data:`API_SERVER`, They total 5 lines of code,\nwhich are copyright the authors of the recaptcha-client_ package.\n\n.. _hardcoded: https://code.google.com/p/recaptcha/source/browse/trunk/recaptcha-plugins/python/recaptcha/client/captcha.py#76\n.. _recaptcha-client: https://pypi.python.org/pypi/recaptcha-client/1.0.6\n\n.. inheritance-diagram:: RecaptchaResponseError RecaptchaResponse RecaptchaResponseProtocol\n    :parts: 1\n'
import logging, urllib
from OpenSSL.crypto import FILETYPE_PEM
from OpenSSL.crypto import load_certificate
from twisted import version as _twistedversion
from twisted.internet import defer
from twisted.internet import protocol
from twisted.internet import reactor
from twisted.python import failure
from twisted.python.versions import Version
from twisted.web import client
from twisted.web.http_headers import Headers
from twisted.web.iweb import IBodyProducer
from zope.interface import implements
from bridgedb.crypto import SSLVerifyingContextFactory
API_SSL_SERVER = API_SERVER = 'https://www.google.com/recaptcha/api'
API_SSL_VERIFY_URL = '%s/verify' % API_SSL_SERVER
GOOGLE_INTERNET_AUTHORITY_CA_CERT = load_certificate(FILETYPE_PEM, bytes('-----BEGIN CERTIFICATE-----\nMIICsDCCAhmgAwIBAgIDFXfhMA0GCSqGSIb3DQEBBQUAME4xCzAJBgNVBAYTAlVT\nMRAwDgYDVQQKEwdFcXVpZmF4MS0wKwYDVQQLEyRFcXVpZmF4IFNlY3VyZSBDZXJ0\naWZpY2F0ZSBBdXRob3JpdHkwHhcNMTIxMjEyMTU1ODUwWhcNMTMxMjMxMTU1ODUw\nWjBGMQswCQYDVQQGEwJVUzETMBEGA1UEChMKR29vZ2xlIEluYzEiMCAGA1UEAxMZ\nR29vZ2xlIEludGVybmV0IEF1dGhvcml0eTCBnzANBgkqhkiG9w0BAQEFAAOBjQAw\ngYkCgYEAye23pIucV+eEPkB9hPSP0XFjU5nneXQUr0SZMyCSjXvlKAy6rWxJfoNf\nNFlOCnowzdDXxFdF7dWq1nMmzq0yE7jXDx07393cCDaob1FEm8rWIFJztyaHNWrb\nqeXUWaUr/GcZOfqTGBhs3t0lig4zFEfC7wFQeeT9adGnwKziV28CAwEAAaOBozCB\noDAfBgNVHSMEGDAWgBRI5mj5K9KylddH2CMgEE8zmJCf1DAdBgNVHQ4EFgQUv8Aw\n6/VDET5nup6R+/xq2uNrEiQwEgYDVR0TAQH/BAgwBgEB/wIBADAOBgNVHQ8BAf8E\nBAMCAQYwOgYDVR0fBDMwMTAvoC2gK4YpaHR0cDovL2NybC5nZW90cnVzdC5jb20v\nY3Jscy9zZWN1cmVjYS5jcmwwDQYJKoZIhvcNAQEFBQADgYEAvprjecFG+iJsxzEF\nZUNgujFQodUovxOWZshcnDW7fZ7mTlk3zpeVJrGPZzhaDhvuJjIfKqHweFB7gwB+\nARlIjNvrPq86fpVg0NOTawALkSqOUMl3MynBQO+spR7EHcRbADQ/JemfTEh2Ycfl\nvZqhEFBfurZkX0eTANq98ZvVfpg=\n-----END CERTIFICATE-----'))
_connectionPoolAvailable = _twistedversion >= Version('twisted', 12, 1, 0)
if _connectionPoolAvailable:
    logging.info('Using HTTPConnectionPool for reCaptcha API server.')
    _pool = client.HTTPConnectionPool(reactor, persistent=False)
    _pool.maxPersistentPerHost = 5
    _pool.cachedConnectionTimeout = 30
    _agent = client.Agent(reactor, pool=_pool)
else:
    logging.warn('Twisted-%s is too old for HTTPConnectionPool! Disabling...' % _twistedversion.short())
    _pool = None
    _agent = client.Agent(reactor)
if _twistedversion >= Version('twisted', 14, 0, 0):
    from twisted.internet._sslverify import OpenSSLCertificateAuthorities

    class RecaptchaOpenSSLCertificateAuthorities(OpenSSLCertificateAuthorities):
        """The trusted CAs for connecting to reCAPTCHA servers."""
        caCerts = [
         GOOGLE_INTERNET_AUTHORITY_CA_CERT]

        def __init__(self):
            super(RecaptchaOpenSSLCertificateAuthorities, self).__init__(self.caCerts)


    class RecaptchaPolicyForHTTPS(client.BrowserLikePolicyForHTTPS):
        _trustRoot = RecaptchaOpenSSLCertificateAuthorities()

        def __init__(self):
            super(RecaptchaPolicyForHTTPS, self).__init__(trustRoot=self._trustRoot)


def _setAgent(agent):
    """Set the global :attr:`agent`.

    :param agent: An :api:`twisted.web.client.Agent` for issuing requests.
    """
    global _agent
    _agent = agent


def _getAgent(reactor=reactor, url=API_SSL_VERIFY_URL, connectTimeout=30, **kwargs):
    """Create a :api:`twisted.web.client.Agent` which will verify the
    certificate chain and hostname for the given **url**.

    :param reactor: A provider of the
        :api:`twisted.internet.interface.IReactorTCP` interface.
    :param str url: The full URL which will be requested with the
        ``Agent``. (default: :attr:`API_SSL_VERIFY_URL`)
    :param pool: An :api:`twisted.web.client.HTTPConnectionPool`
        instance. (default: :attr:`_pool`)
    :type connectTimeout: None or int
    :param connectTimeout: If not ``None``, the timeout passed to
        :api:`twisted.internet.reactor.connectTCP` or
        :api:`twisted.internet.reactor.connectSSL` for specifying the
        connection timeout. (default: ``30``)
    """
    if _twistedversion >= Version('twisted', 14, 0, 0):
        contextFactory = RecaptchaPolicyForHTTPS()
    else:
        contextFactory = SSLVerifyingContextFactory(url)
    if _connectionPoolAvailable:
        return client.Agent(reactor, contextFactory=contextFactory, connectTimeout=connectTimeout, pool=_pool, **kwargs)
    else:
        return client.Agent(reactor, contextFactory=contextFactory, connectTimeout=connectTimeout, **kwargs)


_setAgent(_getAgent())

class RecaptchaResponseError(ValueError):
    """There was an error with the reCaptcha API server's response."""


class RecaptchaResponse(object):
    """Taken from `recaptcha.client.captcha.RecaptchaResponse`__.

    .. __: https://code.google.com/p/recaptcha/source/browse/trunk/recaptcha-plugins/python/recaptcha/client/captcha.py#7
    """

    def __init__(self, is_valid, error_code=None):
        self.is_valid = is_valid
        self.error_code = error_code


class RecaptchaResponseProtocol(protocol.Protocol):
    """HTML parser which creates a :class:`RecaptchaResponse` from the body of
    the reCaptcha API server's response.
    """

    def __init__(self, finished):
        """Create a protocol for creating
        :class:`RecaptchaResponses <bridgedb.txrecaptcha.RecaptchaResponse>`.

        :type finished: :api:`twisted.internet.defer.Deferred`
        :param finished: A deferred which will have its ``callback()`` called
             with a :class:`RecaptchaResponse`.
        """
        self.finished = finished
        self.remaining = 10240
        self.response = ''

    def dataReceived(self, data):
        """Called when some **data** is received from the connection."""
        if self.remaining:
            received = data[:self.remaining]
            self.response += received
            self.remaining -= len(received)

    def connectionLost(self, reason):
        """Called when the connection was closed.

        :type reason: :api:`twisted.python.failure.Failure`
        :param reason: A string explaning why the connection was closed,
            wrapped in a ``Failure`` instance.
        """
        valid = False
        error = reason.getErrorMessage()
        try:
            valid, error = self.response.strip().split('\n', 1)
        except ValueError:
            error = "Couldn't parse response from reCaptcha API server"

        valid = bool(valid == 'true')
        result = RecaptchaResponse(is_valid=valid, error_code=error)
        logging.debug('ReCaptcha API server response: %s(is_valid=%s, error_code=%s)' % (
         result.__class__.__name__, valid, error))
        self.finished.callback(result)


class _BodyProducer(object):
    """I write a string into the HTML body of an open request."""
    implements(IBodyProducer)

    def __init__(self, body):
        self.body = body
        self.length = len(body)

    def startProducing(self, consumer):
        """Start writing the HTML body."""
        consumer.write(self.body)
        return defer.succeed(None)

    def pauseProducing(self):
        pass

    def stopProducing(self):
        pass

    def resumeProducing(self):
        pass


def _cbRequest(response):
    """Callback for a :api:`twisted.web.client.Agent.request` which delivers
    the result to a :class:`RecaptchaResponseProtocol`.

    :returns: A :api:`twisted.internet.defer.Deferred` which will callback
    with a ``recaptcha.RecaptchaResponse`` for the request.
    """
    finished = defer.Deferred()
    response.deliverBody(RecaptchaResponseProtocol(finished))
    return finished


def _ebRequest(fail):
    """Errback for a :api:`twisted.web.client.Agent.request`.

    :param fail: A :api:`twisted.python.failure.Failure` which occurred during
        the request.
    """
    logging.debug('txrecaptcha._ebRequest() called with %r' % fail)
    error = fail.getErrorMessage() or 'possible problem in _ebRequest()'
    return RecaptchaResponse(is_valid=False, error_code=error)


def _encodeIfNecessary(string):
    """Encode unicode objects in utf-8 if necessary."""
    if isinstance(string, unicode):
        return string.encode('utf-8')
    return string


def submit(recaptcha_challenge_field, recaptcha_response_field, private_key, remoteip, agent=_agent):
    """Submits a reCaptcha request for verification. This function is a patched
    version of the ``recaptcha.client.captcha.submit()`` function in
    reCaptcha's Python API.

    It does two things differently:
        1. It uses Twisted for everything.
        2. It uses SSL/TLS for everything.

    This function returns a :api:`twisted.internet.defer.Deferred`. If you
    need a ``recaptcha.client.captcha.RecaptchaResponse`` to be returned, use
    the :func:`submit` function, which is an ``@inlineCallbacks`` wrapper for
    this function.

    :param str recaptcha_challenge_field: The value of the HTTP POST
        ``recaptcha_challenge_field`` argument from the form.
    :param str recaptcha_response_field: The value of the HTTP POST
        ``recaptcha_response_field`` argument from the form.
    :param str private_key: The reCAPTCHA API private key.
    :param str remoteip: An IP address to give to the reCaptcha API server.
    :rtype: :api:`twisted.internet.defer.Deferred`
    :returns: A ``Deferred`` which will callback with a
        ``recaptcha.RecaptchaResponse`` for the request.
    """
    if not (recaptcha_response_field and len(recaptcha_response_field) and recaptcha_challenge_field and len(recaptcha_challenge_field)):
        d = defer.Deferred()
        d.addBoth(_ebRequest)
        d.errback(failure.Failure(ValueError('incorrect-captcha-sol')))
        return d
    params = urllib.urlencode({'privatekey': _encodeIfNecessary(private_key), 
       'remoteip': _encodeIfNecessary(remoteip), 
       'challenge': _encodeIfNecessary(recaptcha_challenge_field), 
       'response': _encodeIfNecessary(recaptcha_response_field)})
    body = _BodyProducer(params)
    headers = Headers({'Content-type': ['application/x-www-form-urlencoded'], 'User-agent': [
                    'reCAPTCHA Python']})
    d = agent.request('POST', API_SSL_VERIFY_URL, headers, body)
    d.addCallbacks(_cbRequest, _ebRequest)
    return d