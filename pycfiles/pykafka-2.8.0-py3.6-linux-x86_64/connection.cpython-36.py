# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pykafka/connection.py
# Compiled at: 2018-05-29 17:13:24
# Size of source mod 2**32: 9081 bytes
from __future__ import division
__license__ = '\nCopyright 2015 Parse.ly, Inc.\n\nLicensed under the Apache License, Version 2.0 (the "License");\nyou may not use this file except in compliance with the License.\nYou may obtain a copy of the License at\n\n    http://www.apache.org/licenses/LICENSE-2.0\n\nUnless required by applicable law or agreed to in writing, software\ndistributed under the License is distributed on an "AS IS" BASIS,\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\nSee the License for the specific language governing permissions and\nlimitations under the License.\n'
__all__ = ['SslConfig', 'BrokerConnection']
from functools import partial
import logging, ssl, struct, time
from .exceptions import SocketDisconnectedError
from .utils.socket import recvall_into
from .utils.compat import buffer
log = logging.getLogger(__name__)

class SslConfig(object):
    __doc__ = "Config object for SSL connections\n\n    This aims to pick optimal defaults for the majority of use cases.  If you\n    have special requirements (eg. you want to enable hostname checking), you\n    may monkey-patch `self._wrap_socket` (see `_legacy_wrap_socket()` for an\n    example) before passing the `SslConfig` to `KafkaClient` init, like so:\n\n        config = SslConfig(cafile='/your/ca/file')\n        config._wrap_socket = config._legacy_wrap_socket()\n        client = KafkaClient('localhost:<ssl-port>', ssl_config=config)\n\n    Alternatively, completely supplanting this class with your own is also\n    simple: if you are not going to be using the `pykafka.rdkafka` classes,\n    only a method `wrap_socket()` is expected (so you can eg. simply pass in\n    a plain `ssl.SSLContext` instance instead).  The `pykafka.rdkafka`\n    classes require four further attributes: `cafile`, `certfile`, `keyfile`,\n    and `password` (the `SslConfig.__init__` docstring explains their meaning)\n    "

    def __init__(self, cafile, certfile=None, keyfile=None, password=None):
        """Specify certificates for SSL connection

        :param cafile: Path to trusted CA certificate
        :type cafile: str
        :param certfile: Path to client certificate
        :type certfile: str
        :param keyfile: Path to client private-key file
        :type keyfile: str
        :param password: Password for private key
        :type password: bytes
        """
        self.cafile = cafile
        self.certfile = certfile
        self.keyfile = keyfile
        self.password = password
        self._wrap_socket = None

    def wrap_socket(self, sock):
        """Wrap a socket in an SSL context (see `ssl.wrap_socket`)

        :param socket: Plain socket
        :type socket: :class:`socket.socket`
        """
        if self._wrap_socket is None:
            if hasattr(ssl, 'SSLContext'):
                ssl_context = ssl.create_default_context(cafile=(self.cafile))
                ssl_context.check_hostname = False
                if self.certfile is not None:
                    ssl_context.load_cert_chain(certfile=(self.certfile), keyfile=(self.keyfile),
                      password=(self.password))
                self._wrap_socket = ssl_context.wrap_socket
            else:
                self._wrap_socket = self._legacy_wrap_socket()
        return self._wrap_socket(sock)

    def _legacy_wrap_socket(self):
        """Create socket-wrapper on a pre-2.7.9 Python interpreter"""
        log.warning('SSL: using legacy fallback, which may use sub-optimal defaults. Check that this satisfies your needs.')
        return partial((ssl.wrap_socket), keyfile=(self.keyfile),
          certfile=(self.certfile),
          cert_reqs=(ssl.CERT_REQUIRED),
          ssl_version=(ssl.PROTOCOL_TLSv1),
          ca_certs=(self.cafile))


class BrokerConnection(object):
    __doc__ = '\n    BrokerConnection thinly wraps a `socket.create_connection` call\n    and handles the sending and receiving of data that conform to the\n    kafka binary protocol over that socket.\n    '

    def __init__(self, host, port, handler, buffer_size=1048576, source_host='', source_port=0, ssl_config=None):
        """Initialize a socket connection to Kafka.

        :param host: The host to which to connect
        :type host: str
        :param port: The port on the host to which to connect.  Assumed to be
            an ssl-endpoint if (and only if) `ssl_config` is also provided
        :type port: int
        :param handler: The :class:`pykafka.handlers.Handler` instance to use when
            creating a connection
        :type handler: :class:`pykafka.handlers.Handler`
        :param buffer_size: The size (in bytes) of the buffer in which to
            hold response data.
        :type buffer_size: int
        :param source_host: The host portion of the source address for
            the socket connection
        :type source_host: str
        :param source_port: The port portion of the source address for
            the socket connection
        :type source_port: int
        :param ssl_config: Config object for SSL connection
        :type ssl_config: :class:`pykafka.connection.SslConfig`
        """
        self._buff = bytearray(buffer_size)
        self.host = host
        self.port = port
        self._handler = handler
        self._socket = None
        self.source_host = source_host
        self.source_port = source_port
        self._wrap_socket = ssl_config.wrap_socket if ssl_config else (lambda x: x)

    def __del__(self):
        """Close this connection when the object is deleted."""
        self.disconnect()

    @property
    def connected(self):
        """Returns true if the socket connection is open."""
        return self._socket is not None

    def connect(self, timeout, attempts=1):
        """Connect to the broker, retrying if specified."""
        log.debug('Connecting to %s:%s', self.host, self.port)
        for attempt in range(0, attempts):
            try:
                self._socket = self._wrap_socket(self._handler.Socket.create_connection((
                 self.host, self.port), timeout / 1000, (
                 self.source_host, self.source_port)))
                log.debug('Successfully connected to %s:%s', self.host, self.port)
                return
            except (self._handler.SockErr, self._handler.GaiError) as err:
                log.info('Attempt %s: failed to connect to %s:%s', attempt, self.host, self.port)
                log.info(err)
                if attempts > 1:
                    log.info('Retrying in 300ms.')
                    time.sleep(0.3)
                continue

        raise SocketDisconnectedError('<broker {}:{}>'.format(self.host, self.port))

    def disconnect(self):
        """Disconnect from the broker."""
        if self._socket is None:
            return
        try:
            try:
                self._socket.close()
            except IOError:
                pass

        finally:
            self._socket = None

    def reconnect(self):
        """Disconnect from the broker, then reconnect"""
        self.disconnect()
        self.connect(10000)

    def request(self, request):
        """Send a request over the socket connection"""
        bytes_ = request.get_bytes()
        if not self._socket:
            raise SocketDisconnectedError('<broker {}:{}>'.format(self.host, self.port))
        try:
            self._socket.sendall(bytes_)
        except self._handler.SockErr as e:
            log.error('Failed to send data, error: %s' % repr(e))
            self.disconnect()
            raise SocketDisconnectedError('<broker {}:{}>'.format(self.host, self.port))

    def response(self):
        """Wait for a response from the broker"""
        size = bytes()
        expected_len = 4
        while len(size) != expected_len:
            try:
                r = self._socket.recv(expected_len - len(size))
            except IOError:
                r = None

            if r is None or len(r) == 0:
                self.disconnect()
                raise SocketDisconnectedError('<broker {}:{}>'.format(self.host, self.port))
            size += r

        size = struct.unpack('!i', size)[0]
        try:
            recvall_into(self._socket, self._buff, size)
        except SocketDisconnectedError:
            self.disconnect()
            raise SocketDisconnectedError('<broker {}:{}>'.format(self.host, self.port))

        return buffer(self._buff[4:4 + size])