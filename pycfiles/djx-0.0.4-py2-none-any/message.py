# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/gunicorn/gunicorn/http/message.py
# Compiled at: 2019-02-14 00:35:18
import re, socket
from errno import ENOTCONN
from gunicorn._compat import bytes_to_str
from gunicorn.http.unreader import SocketUnreader
from gunicorn.http.body import ChunkedReader, LengthReader, EOFReader, Body
from gunicorn.http.errors import InvalidHeader, InvalidHeaderName, NoMoreData, InvalidRequestLine, InvalidRequestMethod, InvalidHTTPVersion, LimitRequestLine, LimitRequestHeaders
from gunicorn.http.errors import InvalidProxyLine, ForbiddenProxyRequest
from gunicorn.http.errors import InvalidSchemeHeaders
from gunicorn.six import BytesIO, string_types
from gunicorn.util import split_request_uri
MAX_REQUEST_LINE = 8190
MAX_HEADERS = 32768
DEFAULT_MAX_HEADERFIELD_SIZE = 8190
HEADER_RE = re.compile('[\\x00-\\x1F\\x7F()<>@,;:\\[\\]={} \\t\\\\\\"]')
METH_RE = re.compile('[A-Z0-9$-_.]{3,20}')
VERSION_RE = re.compile('HTTP/(\\d+)\\.(\\d+)')

class Message(object):

    def __init__(self, cfg, unreader):
        self.cfg = cfg
        self.unreader = unreader
        self.version = None
        self.headers = []
        self.trailers = []
        self.body = None
        self.scheme = 'https' if cfg.is_ssl else 'http'
        self.limit_request_fields = cfg.limit_request_fields
        if self.limit_request_fields <= 0 or self.limit_request_fields > MAX_HEADERS:
            self.limit_request_fields = MAX_HEADERS
        self.limit_request_field_size = cfg.limit_request_field_size
        if self.limit_request_field_size < 0:
            self.limit_request_field_size = DEFAULT_MAX_HEADERFIELD_SIZE
        max_header_field_size = self.limit_request_field_size or DEFAULT_MAX_HEADERFIELD_SIZE
        self.max_buffer_headers = self.limit_request_fields * (max_header_field_size + 2) + 4
        unused = self.parse(self.unreader)
        self.unreader.unread(unused)
        self.set_body_reader()
        return

    def parse(self, unreader):
        raise NotImplementedError()

    def parse_headers(self, data):
        cfg = self.cfg
        headers = []
        lines = [ bytes_to_str(line) + '\r\n' for line in data.split('\r\n') ]
        scheme_header = False
        secure_scheme_headers = {}
        if '*' in cfg.forwarded_allow_ips:
            secure_scheme_headers = cfg.secure_scheme_headers
        else:
            if isinstance(self.unreader, SocketUnreader):
                remote_addr = self.unreader.sock.getpeername()
                if isinstance(remote_addr, tuple):
                    remote_host = remote_addr[0]
                    if remote_host in cfg.forwarded_allow_ips:
                        secure_scheme_headers = cfg.secure_scheme_headers
                elif isinstance(remote_addr, string_types):
                    secure_scheme_headers = cfg.secure_scheme_headers
            while lines:
                if len(headers) >= self.limit_request_fields:
                    raise LimitRequestHeaders('limit request headers fields')
                curr = lines.pop(0)
                header_length = len(curr)
                if curr.find(':') < 0:
                    raise InvalidHeader(curr.strip())
                name, value = curr.split(':', 1)
                name = name.rstrip(' \t').upper()
                if HEADER_RE.search(name):
                    raise InvalidHeaderName(name)
                name, value = name.strip(), [value.lstrip()]
                while lines and lines[0].startswith((' ', '\t')):
                    curr = lines.pop(0)
                    header_length += len(curr)
                    if header_length > self.limit_request_field_size > 0:
                        raise LimitRequestHeaders('limit request headers ' + 'fields size')
                    value.append(curr)

                value = ('').join(value).rstrip()
                if header_length > self.limit_request_field_size > 0:
                    raise LimitRequestHeaders('limit request headers fields size')
                if name in secure_scheme_headers:
                    secure = value == secure_scheme_headers[name]
                    scheme = 'https' if secure else 'http'
                    if scheme_header:
                        if scheme != self.scheme:
                            raise InvalidSchemeHeaders()
                    else:
                        scheme_header = True
                        self.scheme = scheme
                headers.append((name, value))

        return headers

    def set_body_reader(self):
        chunked = False
        content_length = None
        for name, value in self.headers:
            if name == 'CONTENT-LENGTH':
                content_length = value
            elif name == 'TRANSFER-ENCODING':
                chunked = value.lower() == 'chunked'
            elif name == 'SEC-WEBSOCKET-KEY1':
                content_length = 8

        if chunked:
            self.body = Body(ChunkedReader(self, self.unreader))
        elif content_length is not None:
            try:
                content_length = int(content_length)
            except ValueError:
                raise InvalidHeader('CONTENT-LENGTH', req=self)

            if content_length < 0:
                raise InvalidHeader('CONTENT-LENGTH', req=self)
            self.body = Body(LengthReader(self.unreader, content_length))
        else:
            self.body = Body(EOFReader(self.unreader))
        return

    def should_close(self):
        for h, v in self.headers:
            if h == 'CONNECTION':
                v = v.lower().strip()
                if v == 'close':
                    return True
                if v == 'keep-alive':
                    return False
                break

        return self.version <= (1, 0)


class Request(Message):

    def __init__(self, cfg, unreader, req_number=1):
        self.method = None
        self.uri = None
        self.path = None
        self.query = None
        self.fragment = None
        self.limit_request_line = cfg.limit_request_line
        if self.limit_request_line < 0 or self.limit_request_line >= MAX_REQUEST_LINE:
            self.limit_request_line = MAX_REQUEST_LINE
        self.req_number = req_number
        self.proxy_protocol_info = None
        super(Request, self).__init__(cfg, unreader)
        return

    def get_data(self, unreader, buf, stop=False):
        data = unreader.read()
        if not data:
            if stop:
                raise StopIteration()
            raise NoMoreData(buf.getvalue())
        buf.write(data)

    def parse(self, unreader):
        buf = BytesIO()
        self.get_data(unreader, buf, stop=True)
        line, rbuf = self.read_line(unreader, buf, self.limit_request_line)
        if self.proxy_protocol(bytes_to_str(line)):
            buf = BytesIO()
            buf.write(rbuf)
            line, rbuf = self.read_line(unreader, buf, self.limit_request_line)
        self.parse_request_line(line)
        buf = BytesIO()
        buf.write(rbuf)
        data = buf.getvalue()
        idx = data.find('\r\n\r\n')
        done = data[:2] == '\r\n'
        while True:
            idx = data.find('\r\n\r\n')
            done = data[:2] == '\r\n'
            if idx < 0 and not done:
                self.get_data(unreader, buf)
                data = buf.getvalue()
                if len(data) > self.max_buffer_headers:
                    raise LimitRequestHeaders('max buffer headers')
            else:
                break

        if done:
            self.unreader.unread(data[2:])
            return ''
        else:
            self.headers = self.parse_headers(data[:idx])
            ret = data[idx + 4:]
            buf = None
            return ret

    def read_line(self, unreader, buf, limit=0):
        data = buf.getvalue()
        while True:
            idx = data.find('\r\n')
            if idx >= 0:
                if idx > limit > 0:
                    raise LimitRequestLine(idx, limit)
                break
            elif len(data) - 2 > limit > 0:
                raise LimitRequestLine(len(data), limit)
            self.get_data(unreader, buf)
            data = buf.getvalue()

        return (data[:idx],
         data[idx + 2:])

    def proxy_protocol(self, line):
        """        Detect, check and parse proxy protocol.

        :raises: ForbiddenProxyRequest, InvalidProxyLine.
        :return: True for proxy protocol line else False
        """
        if not self.cfg.proxy_protocol:
            return False
        if self.req_number != 1:
            return False
        if not line.startswith('PROXY'):
            return False
        self.proxy_protocol_access_check()
        self.parse_proxy_protocol(line)
        return True

    def proxy_protocol_access_check(self):
        if isinstance(self.unreader, SocketUnreader):
            try:
                remote_host = self.unreader.sock.getpeername()[0]
            except socket.error as e:
                if e.args[0] == ENOTCONN:
                    raise ForbiddenProxyRequest('UNKNOW')
                raise

            if '*' not in self.cfg.proxy_allow_ips and remote_host not in self.cfg.proxy_allow_ips:
                raise ForbiddenProxyRequest(remote_host)

    def parse_proxy_protocol(self, line):
        bits = line.split()
        if len(bits) != 6:
            raise InvalidProxyLine(line)
        proto = bits[1]
        s_addr = bits[2]
        d_addr = bits[3]
        if proto not in ('TCP4', 'TCP6'):
            raise InvalidProxyLine("protocol '%s' not supported" % proto)
        if proto == 'TCP4':
            try:
                socket.inet_pton(socket.AF_INET, s_addr)
                socket.inet_pton(socket.AF_INET, d_addr)
            except socket.error:
                raise InvalidProxyLine(line)

        else:
            if proto == 'TCP6':
                try:
                    socket.inet_pton(socket.AF_INET6, s_addr)
                    socket.inet_pton(socket.AF_INET6, d_addr)
                except socket.error:
                    raise InvalidProxyLine(line)

            try:
                s_port = int(bits[4])
                d_port = int(bits[5])
            except ValueError:
                raise InvalidProxyLine('invalid port %s' % line)

        if not (0 <= s_port <= 65535 and 0 <= d_port <= 65535):
            raise InvalidProxyLine('invalid port %s' % line)
        self.proxy_protocol_info = {'proxy_protocol': proto, 
           'client_addr': s_addr, 
           'client_port': s_port, 
           'proxy_addr': d_addr, 
           'proxy_port': d_port}

    def parse_request_line(self, line_bytes):
        bits = [ bytes_to_str(bit) for bit in line_bytes.split(None, 2) ]
        if len(bits) != 3:
            raise InvalidRequestLine(bytes_to_str(line_bytes))
        if not METH_RE.match(bits[0]):
            raise InvalidRequestMethod(bits[0])
        self.method = bits[0].upper()
        self.uri = bits[1]
        try:
            parts = split_request_uri(self.uri)
        except ValueError:
            raise InvalidRequestLine(bytes_to_str(line_bytes))

        self.path = parts.path or ''
        self.query = parts.query or ''
        self.fragment = parts.fragment or ''
        match = VERSION_RE.match(bits[2])
        if match is None:
            raise InvalidHTTPVersion(bits[2])
        self.version = (
         int(match.group(1)), int(match.group(2)))
        return

    def set_body_reader(self):
        super(Request, self).set_body_reader()
        if isinstance(self.body.reader, EOFReader):
            self.body = Body(LengthReader(self.unreader, 0))