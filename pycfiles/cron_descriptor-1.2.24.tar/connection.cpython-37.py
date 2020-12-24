# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /private/var/folders/pb/598z8h910dvf2wrvwnbyl_2m0000gn/T/pip-install-65c3rg8f/urllib3/urllib3/connection.py
# Compiled at: 2019-11-10 08:27:46
# Size of source mod 2**32: 15170 bytes
from __future__ import absolute_import
import datetime, logging, os, socket
from socket import error as SocketError, timeout as SocketTimeout
import warnings
from .packages import six
import packages.six.moves.http_client as _HTTPConnection
from packages.six.moves.http_client import HTTPException
try:
    import ssl
    BaseSSLError = ssl.SSLError
except (ImportError, AttributeError):
    ssl = None

    class BaseSSLError(BaseException):
        pass


try:
    ConnectionError = ConnectionError
except NameError:

    class ConnectionError(Exception):
        pass


from .exceptions import NewConnectionError, ConnectTimeoutError, SubjectAltNameWarning, SystemTimeWarning
from packages.ssl_match_hostname import match_hostname, CertificateError
from util.ssl_ import resolve_cert_reqs, resolve_ssl_version, assert_fingerprint, create_urllib3_context, ssl_wrap_socket
from .util import connection
from ._collections import HTTPHeaderDict
log = logging.getLogger(__name__)
port_by_scheme = {'http':80, 
 'https':443}
RECENT_DATE = datetime.date(2019, 1, 1)

class DummyConnection(object):
    """DummyConnection"""
    pass


class HTTPConnection(_HTTPConnection, object):
    """HTTPConnection"""
    default_port = port_by_scheme['http']
    default_socket_options = [
     (
      socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)]
    is_verified = False

    def __init__(self, *args, **kw):
        if not six.PY2:
            kw.pop('strict', None)
        self.source_address = kw.get('source_address')
        self.socket_options = kw.pop('socket_options', self.default_socket_options)
        (_HTTPConnection.__init__)(self, *args, **kw)

    @property
    def host(self):
        """
        Getter method to remove any trailing dots that indicate the hostname is an FQDN.

        In general, SSL certificates don't include the trailing dot indicating a
        fully-qualified domain name, and thus, they don't validate properly when
        checked against a domain name that includes the dot. In addition, some
        servers may not expect to receive the trailing dot when provided.

        However, the hostname with trailing dot is critical to DNS resolution; doing a
        lookup with the trailing dot will properly only resolve the appropriate FQDN,
        whereas a lookup without a trailing dot will search the system's search domain
        list. Thus, it's important to keep the original host around for use only in
        those cases where it's appropriate (i.e., when doing DNS lookup to establish the
        actual TCP connection across which we're going to send HTTP requests).
        """
        return self._dns_host.rstrip('.')

    @host.setter
    def host(self, value):
        """
        Setter for the `host` property.

        We assume that only urllib3 uses the _dns_host attribute; httplib itself
        only uses `host`, and it seems reasonable that other libraries follow suit.
        """
        self._dns_host = value

    def _new_conn(self):
        """ Establish a socket connection and set nodelay settings on it.

        :return: New socket connection.
        """
        extra_kw = {}
        if self.source_address:
            extra_kw['source_address'] = self.source_address
        if self.socket_options:
            extra_kw['socket_options'] = self.socket_options
        try:
            conn = (connection.create_connection)(
             (
              self._dns_host, self.port), (self.timeout), **extra_kw)
        except SocketTimeout:
            raise ConnectTimeoutError(self, 'Connection to %s timed out. (connect timeout=%s)' % (
             self.host, self.timeout))
        except SocketError as e:
            try:
                raise NewConnectionError(self, 'Failed to establish a new connection: %s' % e)
            finally:
                e = None
                del e

        return conn

    def _prepare_conn(self, conn):
        self.sock = conn
        if getattr(self, '_tunnel_host', None):
            self._tunnel()
            self.auto_open = 0

    def connect(self):
        conn = self._new_conn()
        self._prepare_conn(conn)

    def request_chunked(self, method, url, body=None, headers=None):
        """
        Alternative to the common request method, which sends the
        body with chunked encoding and not as one block
        """
        headers = HTTPHeaderDict(headers if headers is not None else {})
        skip_accept_encoding = 'accept-encoding' in headers
        skip_host = 'host' in headers
        self.putrequest(method,
          url, skip_accept_encoding=skip_accept_encoding, skip_host=skip_host)
        for header, value in headers.items():
            self.putheader(header, value)

        if 'transfer-encoding' not in headers:
            self.putheader('Transfer-Encoding', 'chunked')
        self.endheaders()
        if body is not None:
            stringish_types = six.string_types + (bytes,)
            if isinstance(body, stringish_types):
                body = (
                 body,)
            for chunk in body:
                if not chunk:
                    continue
                if not isinstance(chunk, bytes):
                    chunk = chunk.encode('utf8')
                len_str = hex(len(chunk))[2:]
                self.send(len_str.encode('utf-8'))
                self.send('\r\n')
                self.send(chunk)
                self.send('\r\n')

        self.send('0\r\n\r\n')


class HTTPSConnection(HTTPConnection):
    default_port = port_by_scheme['https']
    ssl_version = None

    def __init__(self, host, port=None, key_file=None, cert_file=None, key_password=None, strict=None, timeout=socket._GLOBAL_DEFAULT_TIMEOUT, ssl_context=None, server_hostname=None, **kw):
        (HTTPConnection.__init__)(self, host, port, strict=strict, timeout=timeout, **kw)
        self.key_file = key_file
        self.cert_file = cert_file
        self.key_password = key_password
        self.ssl_context = ssl_context
        self.server_hostname = server_hostname
        self._protocol = 'https'

    def connect(self):
        conn = self._new_conn()
        self._prepare_conn(conn)
        default_ssl_context = False
        if self.ssl_context is None:
            default_ssl_context = True
            self.ssl_context = create_urllib3_context(ssl_version=(resolve_ssl_version(self.ssl_version)),
              cert_reqs=(resolve_cert_reqs(self.cert_reqs)))
        context = self.ssl_context
        if not self.ca_certs:
            if not self.ca_cert_dir:
                if default_ssl_context:
                    if hasattr(context, 'load_default_certs'):
                        context.load_default_certs()
        self.sock = ssl_wrap_socket(sock=conn,
          keyfile=(self.key_file),
          certfile=(self.cert_file),
          key_password=(self.key_password),
          ssl_context=(self.ssl_context),
          server_hostname=(self.server_hostname))


class VerifiedHTTPSConnection(HTTPSConnection):
    """VerifiedHTTPSConnection"""
    cert_reqs = None
    ca_certs = None
    ca_cert_dir = None
    ssl_version = None
    assert_fingerprint = None

    def set_cert(self, key_file=None, cert_file=None, cert_reqs=None, key_password=None, ca_certs=None, assert_hostname=None, assert_fingerprint=None, ca_cert_dir=None):
        """
        This method should only be called once, before the connection is used.
        """
        if cert_reqs is None:
            if self.ssl_context is not None:
                cert_reqs = self.ssl_context.verify_mode
            else:
                cert_reqs = resolve_cert_reqs(None)
        self.key_file = key_file
        self.cert_file = cert_file
        self.cert_reqs = cert_reqs
        self.key_password = key_password
        self.assert_hostname = assert_hostname
        self.assert_fingerprint = assert_fingerprint
        self.ca_certs = ca_certs and os.path.expanduser(ca_certs)
        self.ca_cert_dir = ca_cert_dir and os.path.expanduser(ca_cert_dir)

    def connect(self):
        conn = self._new_conn()
        hostname = self.host
        if getattr(self, '_tunnel_host', None):
            self.sock = conn
            self._tunnel()
            self.auto_open = 0
            hostname = self._tunnel_host
        server_hostname = hostname
        if self.server_hostname is not None:
            server_hostname = self.server_hostname
        is_time_off = datetime.date.today() < RECENT_DATE
        if is_time_off:
            warnings.warn('System time is way off (before {0}). This will probably lead to SSL verification errors'.format(RECENT_DATE), SystemTimeWarning)
        default_ssl_context = False
        if self.ssl_context is None:
            default_ssl_context = True
            self.ssl_context = create_urllib3_context(ssl_version=(resolve_ssl_version(self.ssl_version)),
              cert_reqs=(resolve_cert_reqs(self.cert_reqs)))
        context = self.ssl_context
        context.verify_mode = resolve_cert_reqs(self.cert_reqs)
        if not self.ca_certs:
            if not self.ca_cert_dir:
                if default_ssl_context:
                    if hasattr(context, 'load_default_certs'):
                        context.load_default_certs()
        self.sock = ssl_wrap_socket(sock=conn,
          keyfile=(self.key_file),
          certfile=(self.cert_file),
          key_password=(self.key_password),
          ca_certs=(self.ca_certs),
          ca_cert_dir=(self.ca_cert_dir),
          server_hostname=server_hostname,
          ssl_context=context)
        if self.assert_fingerprint:
            assert_fingerprint(self.sock.getpeercert(binary_form=True), self.assert_fingerprint)
        elif context.verify_mode != ssl.CERT_NONE:
            if not getattr(context, 'check_hostname', False):
                if self.assert_hostname is not False:
                    cert = self.sock.getpeercert()
                    if not cert.get('subjectAltName', ()):
                        warnings.warn('Certificate for {0} has no `subjectAltName`, falling back to check for a `commonName` for now. This feature is being removed by major browsers and deprecated by RFC 2818. (See https://github.com/shazow/urllib3/issues/497 for details.)'.format(hostname), SubjectAltNameWarning)
                    _match_hostname(cert, self.assert_hostname or )
        self.is_verified = context.verify_mode == ssl.CERT_REQUIRED or 


def _match_hostname(cert, asserted_hostname):
    try:
        match_hostname(cert, asserted_hostname)
    except CertificateError as e:
        try:
            log.warning('Certificate did not match expected hostname: %s. Certificate: %s', asserted_hostname, cert)
            e._peer_cert = cert
            raise
        finally:
            e = None
            del e


if ssl:
    UnverifiedHTTPSConnection = HTTPSConnection
    HTTPSConnection = VerifiedHTTPSConnection
else:
    HTTPSConnection = DummyConnection