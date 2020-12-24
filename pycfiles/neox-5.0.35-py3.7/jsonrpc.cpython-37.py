# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/neox/commons/jsonrpc.py
# Compiled at: 2020-02-26 23:29:02
# Size of source mod 2**32: 12054 bytes
import sys, ssl
from decimal import Decimal
import datetime, socket, gzip, hashlib, base64, threading, errno
from functools import partial
from contextlib import contextmanager
import string, ssl
from xmlrpc import client
from functools import reduce
try:
    import simplejson as json
except ImportError:
    import json

try:
    import http.client as httplib
except:
    import http.client

import io
__all__ = [
 'ResponseError', 'Fault', 'ProtocolError', 'Transport',
 'ServerProxy', 'ServerPool']
PYTHON_VERSION = str(sys.version_info[0])
CONNECT_TIMEOUT = 5
DEFAULT_TIMEOUT = None

class ResponseError(client.ResponseError):
    pass


class Fault(client.Fault):

    def __init__(self, faultCode, faultString='', **extra):
        (super(Fault, self).__init__)(faultCode, faultString, **extra)
        self.args = faultString

    def __repr__(self):
        return '<Fault %s: %s>' % (
         repr(self.faultCode), repr(self.faultString))


class ProtocolError(client.ProtocolError):
    pass


def object_hook(dct):
    if '__class__' in dct:
        if dct['__class__'] == 'datetime':
            return datetime.datetime(dct['year'], dct['month'], dct['day'], dct['hour'], dct['minute'], dct['second'], dct['microsecond'])
        if dct['__class__'] == 'date':
            return datetime.date(dct['year'], dct['month'], dct['day'])
        if dct['__class__'] == 'time':
            return datetime.time(dct['hour'], dct['minute'], dct['second'], dct['microsecond'])
        if dct['__class__'] == 'timedelta':
            return datetime.timedelta(seconds=(dct['seconds']))
        if dct['__class__'] == 'bytes':
            cast = bytearray if bytes == str else bytes
            return cast(base64.decodestring(dct['base64']))
        if dct['__class__'] == 'Decimal':
            return Decimal(dct['decimal'])
    return dct


class JSONEncoder(json.JSONEncoder):

    def __init__(self, *args, **kwargs):
        (super(JSONEncoder, self).__init__)(*args, **kwargs)
        self.use_decimal = False

    def default(self, obj):
        if isinstance(obj, datetime.date):
            if isinstance(obj, datetime.datetime):
                return {'__class__':'datetime', 
                 'year':obj.year, 
                 'month':obj.month, 
                 'day':obj.day, 
                 'hour':obj.hour, 
                 'minute':obj.minute, 
                 'second':obj.second, 
                 'microsecond':obj.microsecond}
            return {'__class__':'date',  'year':obj.year, 
             'month':obj.month, 
             'day':obj.day}
        if isinstance(obj, datetime.time):
            return {'__class__':'time', 
             'hour':obj.hour, 
             'minute':obj.minute, 
             'second':obj.second, 
             'microsecond':obj.microsecond}
        if isinstance(obj, datetime.timedelta):
            return {'__class__':'timedelta', 
             'seconds':obj.total_seconds()}
        if isinstance(obj, memoryview):
            return {'__class__':'buffer', 
             'base64':base64.encodestring(obj)}
        if isinstance(obj, Decimal):
            return {'__class__':'Decimal', 
             'decimal':str(obj)}
        return super(JSONEncoder, self).default(obj)


class JSONParser(object):

    def __init__(self, target):
        self._JSONParser__targer = target

    def feed(self, data):
        self._JSONParser__targer.feed(data)

    def close(self):
        pass


class JSONUnmarshaller(object):

    def __init__(self):
        self.data = []

    def feed(self, data):
        self.data.append(data)

    def close(self):
        data = self.data[0].decode('utf-8')
        return json.loads(data, object_hook=object_hook)


class Transport(client.SafeTransport, client.Transport):
    accept_gzip_encoding = True
    encode_threshold = 1400

    def __init__(self, fingerprints=None, ca_certs=None, session=None):
        client.Transport.__init__(self)
        self._connection = (None, None)
        self._Transport__fingerprints = fingerprints
        self._Transport__ca_certs = ca_certs
        self.session = session

    def getparser(self):
        target = JSONUnmarshaller()
        parser = JSONParser(target)
        return (parser, target)

    def get_host_info(self, host):
        host, extra_headers, x509 = client.Transport.get_host_info(self, host)
        if extra_headers is None:
            extra_headers = []
        if self.session:
            auth = base64.encodestring(self.session)
            auth = string.join(string.split(auth), '')
            extra_headers.append((
             'Authorization', 'Session ' + auth))
        extra_headers.append(('Connection', 'keep-alive'))
        extra_headers.append(('Content-Type', 'text/json'))
        return (host, extra_headers, x509)

    def send_content(self, connection, request_body):
        if self.encode_threshold is not None:
            if self.encode_threshold < len(request_body):
                if gzip:
                    connection.putheader('Content-Encoding', 'gzip')
                    request_body = gzip.compress(request_body)
        connection.putheader('Content-Length', str(len(request_body)))
        connection.endheaders()
        if request_body:
            if PYTHON_VERSION == '3':
                request_body = bytes(request_body, 'UTF-8')
            connection.send(request_body)

    def make_connection(self, host):
        if self._connection:
            if host == self._connection[0]:
                return self._connection[1]
            else:
                host, self._extra_headers, x509 = self.get_host_info(host)
                ca_certs = self._Transport__ca_certs
                cert_reqs = ssl.CERT_REQUIRED if ca_certs else ssl.CERT_NONE

                class HTTPSConnection(http.client.HTTPSConnection):

                    def connect(self):
                        sock = socket.create_connection((self.host, self.port), self.timeout)
                        if self._tunnel_host:
                            self.sock = sock
                            self._tunnel()
                        self.sock = ssl.wrap_socket(sock, (self.key_file), (self.cert_file),
                          ca_certs=ca_certs, cert_reqs=cert_reqs)

                def http_connection():
                    self._connection = (
                     host,
                     http.client.HTTPConnection(host, timeout=CONNECT_TIMEOUT))
                    self._connection[1].connect()
                    sock = self._connection[1].sock
                    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                    sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)

                def https_connection():
                    self._connection = (
                     host,
                     HTTPSConnection(host, timeout=CONNECT_TIMEOUT))
                    try:
                        self._connection[1].connect()
                        sock = self._connection[1].sock
                        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                        sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
                        try:
                            peercert = sock.getpeercert(True)
                        except socket.error:
                            peercert = None

                        def format_hash(value):
                            return reduce(lambda x, y: x + y[1].upper() + (y[0] % 2 and y[0] + 1 < len(value) and ':' or ''), enumerate(value), '')

                        return format_hash(hashlib.sha1(peercert).hexdigest())
                    except ssl.SSLError:
                        http_connection()

                fingerprint = ''
                if self._Transport__fingerprints is not None:
                    if host in self._Transport__fingerprints:
                        if self._Transport__fingerprints[host]:
                            fingerprint = https_connection()
                    else:
                        http_connection()
                else:
                    fingerprint = https_connection()
            if self._Transport__fingerprints is not None:
                if host in self._Transport__fingerprints and self._Transport__fingerprints[host]:
                    if self._Transport__fingerprints[host] != fingerprint:
                        self.close()
                        raise ssl.SSLError('BadFingerprint')
        else:
            self._Transport__fingerprints[host] = fingerprint
        self._connection[1].timeout = DEFAULT_TIMEOUT
        self._connection[1].sock.settimeout(DEFAULT_TIMEOUT)
        return self._connection[1]


class ServerProxy(client.ServerProxy):
    _ServerProxy__id = 0

    def __init__(self, host, port, database='', verbose=0, fingerprints=None, ca_certs=None, session=None):
        self._ServerProxy__host = '%s:%s' % (host, port)
        if database:
            self._ServerProxy__handler = '/%s/' % database
        else:
            self._ServerProxy__handler = '/'
        self._ServerProxy__transport = Transport(fingerprints, ca_certs, session)
        self._ServerProxy__verbose = verbose

    def __request(self, methodname, params):
        self._ServerProxy__id += 1
        id_ = self._ServerProxy__id
        request = json.dumps({'id':id_, 
         'method':methodname, 
         'params':params},
          cls=JSONEncoder)
        try:
            response = self._ServerProxy__transport.request((self._ServerProxy__host),
              (self._ServerProxy__handler),
              request,
              verbose=(self._ServerProxy__verbose))
        except (socket.error, http.client.HTTPException) as v:
            try:
                if isinstance(v, socket.error):
                    if v.args[0] == errno.EPIPE:
                        raise
                self._ServerProxy__transport.close()
                response = self._ServerProxy__transport.request((self._ServerProxy__host),
                  (self._ServerProxy__handler),
                  request,
                  verbose=(self._ServerProxy__verbose))
            finally:
                v = None
                del v

        except:
            self._ServerProxy__transport.close()
            raise

        if response['id'] != id_:
            raise ResponseError('Invalid response id (%s) excpected %s' % (
             response['id'], id_))
        if response.get('error'):
            raise Fault(*response['error'])
        return response['result']

    def close(self):
        self._ServerProxy__transport.close()

    @property
    def ssl(self):
        return isinstance(self._ServerProxy__transport.make_connection(self._ServerProxy__host), http.client.HTTPSConnection)


class ServerPool(object):

    def __init__(self, *args, **kwargs):
        self.ServerProxy = partial(ServerProxy, *args, **kwargs)
        self._lock = threading.Lock()
        self._pool = []
        self._used = {}
        self.session = None

    def getconn(self):
        with self._lock:
            if self._pool:
                conn = self._pool.pop()
            else:
                conn = self.ServerProxy()
            self._used[id(conn)] = conn
            return conn

    def putconn(self, conn):
        with self._lock:
            self._pool.append(conn)
            del self._used[id(conn)]

    def close(self):
        with self._lock:
            for conn in self._pool + list(self._used.values()):
                conn.close()

    @property
    def ssl(self):
        for conn in self._pool + list(self._used.values()):
            return conn.ssl

        return False

    @contextmanager
    def __call__(self):
        conn = self.getconn()
        yield conn
        self.putconn(conn)


if __name__ == '__main__':
    connection = ServerProxy('127.0.0.1', '8000', 'DEMO41')
    result = connection.common.server.version()
    print(result)
    conn = connection()
    res = connection.common.db.login('admin', 'aa')
    print(res)
    tx = connection.common.model.res.user.get_preferences(res[0], res[1], True, {})