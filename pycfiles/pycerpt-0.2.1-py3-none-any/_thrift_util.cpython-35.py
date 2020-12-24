# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/cerebro/_thrift_util.py
# Compiled at: 2018-03-08 20:03:41
# Size of source mod 2**32: 10188 bytes
__doc__ = ' Utilities for using thrift, including SASl support. '
from __future__ import absolute_import
import getpass
from io import BytesIO as BufferIO
import struct
from thriftpy.thrift import TClient
from thriftpy.protocol.binary import TBinaryProtocol
from thriftpy.transport import TSocket, TTransportException, TTransportBase
from thriftpy.transport.buffered import TBufferedTransport
from thriftpy.transport import readall
from cerebro._pure_sasl_client import SASLClient
from cerebro._util import get_logger_and_init_null
from cerebro._util import to_bytes
PlannerClient = TClient
WorkerClient = TClient
SOCKET_READ_ZERO = 'TSocket read 0 bytes'
KERBEROS_NOT_ENABLED_MSG = 'Unsupported mechanism type GSSAPI'
log = get_logger_and_init_null(__name__)

def create_socket(host, port, timeout, use_ssl, ca_cert):
    sock = get_socket(host, port, use_ssl, ca_cert)
    if timeout is not None:
        timeout = timeout * 1000.0
    try:
        sock.set_timeout(timeout)
    except AttributeError:
        sock.socket_timeout = timeout
        sock.connect_timeout = timeout

    return sock


def get_socket(host, port, use_ssl, ca_cert):
    log.debug('get_socket: host=%s port=%s use_ssl=%s ca_cert=%s', host, port, use_ssl, ca_cert)
    if not use_ssl:
        return TSocket(host, port)
    from thriftpy.transport.sslsocket import TSSLSocket
    if ca_cert is None:
        return TSSLSocket(host, port, validate=False)
    return TSSLSocket(host, port, validate=True, cafile=ca_cert)


def get_transport(socket, host, auth_mechanism='NOSASL', service_name=None, user=None, password=None, token=None, host_override=None):
    """
    Creates a new Thrift Transport using the specified auth_mechanism.
    Supported auth_mechanisms are:
    -  None or 'NOSASL' - returns simple buffered transport (default)
    - 'PLAIN'  - returns a SASL transport with the PLAIN mechanism
    - 'GSSAPI' - returns a SASL transport with the GSSAPI mechanism
    - 'DIGEST-MD5' - returns a SASL transport with the DIGEST-MD5 mechanism
    """
    log.debug('get_transport: socket=%s host=%s service_name=%s auth_mechanism=%s user=%s password=fuggetaboutit host_override=%s', socket, host, service_name, auth_mechanism, user, host_override)
    if auth_mechanism == 'NOSASL':
        return TBufferedTransport(socket)
    if auth_mechanism in ('LDAP', 'PLAIN'):
        if user is None:
            user = getpass.getuser()
            log.debug('get_transport: user=%s', user)
        if password is None:
            if auth_mechanism == 'LDAP':
                password = ''
            else:
                password = 'password'
            log.debug('get_transport: password=%s', password)
    elif auth_mechanism in ('DIGEST-MD5', ):
        user = token
        service_name = 'cerebro'
        password = 'cerebro'
    if host_override:
        host = host_override

    def sasl_factory():
        return SASLClient(host, username=user, password=password, service=service_name)

    return TSaslClientTransport(sasl_factory, auth_mechanism, socket)


class TSaslClientTransport(TTransportBase):
    START = 1
    OK = 2
    BAD = 3
    ERROR = 4
    COMPLETE = 5

    def __init__(self, sasl_client_factory, mechanism, trans):
        """
        @param sasl_client_factory: a callable that returns a new sasl.Client object
        @param mechanism: the SASL mechanism (e.g. "GSSAPI")
        @param trans: the underlying transport over which to communicate.
        """
        self._trans = trans
        self.sasl_client_factory = sasl_client_factory
        self.sasl = None
        self.mechanism = mechanism
        self._TSaslClientTransport__wbuf = BufferIO()
        self._TSaslClientTransport__rbuf = BufferIO()
        self.opened = False
        self.encode = None

    def isOpen(self):
        return self._trans.isOpen()

    def is_open(self):
        return self.isOpen()

    def open(self):
        if not self._trans.is_open():
            self._trans.open()
        if self.sasl is not None:
            raise TTransportException(type=TTransportException.NOT_OPEN, message='Already open!')
        self.sasl = self.sasl_client_factory()
        self.sasl.choose_mechanism([self.mechanism], allow_anonymous=False)
        initial_response = self.sasl.process()
        self._send_message(self.START, self.mechanism)
        if initial_response:
            self._send_message(self.OK, initial_response)
        while True:
            status, payload = self._recv_sasl_message()
            if status not in (self.OK, self.COMPLETE):
                raise TTransportException(type=TTransportException.NOT_OPEN, message='Bad status: %d (%s)' % (status, payload))
            if status == self.COMPLETE:
                break
            response = self.sasl.process(payload)
            self._send_message(self.OK, response)

    def _send_message(self, status, body):
        body_bytes = to_bytes(body)
        header = struct.pack('>BI', status, len(body_bytes))
        self._trans.write(header + body_bytes)
        self._trans.flush()

    def _recv_sasl_message(self):
        header = readall(self._trans.read, 5)
        status, length = struct.unpack('>BI', header)
        if length > 0:
            return (status, readall(self._trans.read, length))
        return (status, '')

    def write(self, data):
        self._TSaslClientTransport__wbuf.write(data)

    def flush(self):
        buffer = self._TSaslClientTransport__wbuf.getvalue()
        self._flushPlain(buffer)
        self._trans.flush()
        self._TSaslClientTransport__wbuf = BufferIO()

    def _flushEncoded(self, buffer):
        success, encoded = self.sasl.encode(buffer)
        if not success:
            raise TTransportException(type=TTransportException.UNKNOWN, message=self.sasl.getError())
        self._trans.write(encoded)

    def _flushPlain(self, buffer):
        self._trans.write(struct.pack('>I', len(buffer)) + buffer)

    def _read(self, sz):
        ret = self._TSaslClientTransport__rbuf.read(sz)
        if len(ret) == sz:
            return ret
        self._read_frame()
        return ret + self._TSaslClientTransport__rbuf.read(sz - len(ret))

    def _read_frame(self):
        header = readall(self._trans.read, 4)
        length, = struct.unpack('>I', header)
        if self.encode:
            encoded = header + readall(self._trans.read, length)
            success, decoded = self.sasl.decode(encoded)
            if not success:
                raise TTransportException(type=TTransportException.UNKNOWN, message=self.sasl.getError())
        else:
            decoded = readall(self._trans.read, length)
        if length != len(decoded):
            raise TTransportException(type=TTransportException.NOT_OPEN, message='Short read. Expecting to read %d byte but only read %d bytes.' % (
             length, len(decoded)))
        self._TSaslClientTransport__rbuf = BufferIO(decoded)

    def close(self):
        self._trans.close()
        self.sasl = None

    @property
    def cstringio_buf(self):
        return self._TSaslClientTransport__rbuf

    def cstringio_refill(self, prefix, reqlen):
        while len(prefix) < reqlen:
            self._read_frame()
            prefix += self._TSaslClientTransport__rbuf.getvalue()

        self._TSaslClientTransport__rbuf = BufferIO(prefix)
        return self._TSaslClientTransport__rbuf