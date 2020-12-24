# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/gunicorn/gunicorn/http/wsgi.py
# Compiled at: 2019-02-14 00:35:18
import io, logging, os, re, sys
from gunicorn._compat import unquote_to_wsgi_str
from gunicorn.http.message import HEADER_RE
from gunicorn.http.errors import InvalidHeader, InvalidHeaderName
from gunicorn.six import string_types, binary_type, reraise
from gunicorn import SERVER_SOFTWARE
import gunicorn.util as util
try:
    from os import sendfile
except ImportError:
    try:
        from ._sendfile import sendfile
    except ImportError:
        sendfile = None

BLKSIZE = 1073741823
HEADER_VALUE_RE = re.compile('[\\x00-\\x1F\\x7F]')
log = logging.getLogger(__name__)

class FileWrapper(object):

    def __init__(self, filelike, blksize=8192):
        self.filelike = filelike
        self.blksize = blksize
        if hasattr(filelike, 'close'):
            self.close = filelike.close

    def __getitem__(self, key):
        data = self.filelike.read(self.blksize)
        if data:
            return data
        raise IndexError


class WSGIErrorsWrapper(io.RawIOBase):

    def __init__(self, cfg):
        errorlog = logging.getLogger('gunicorn.error')
        handlers = errorlog.handlers
        self.streams = []
        if cfg.errorlog == '-':
            self.streams.append(sys.stderr)
            handlers = handlers[1:]
        for h in handlers:
            if hasattr(h, 'stream'):
                self.streams.append(h.stream)

    def write(self, data):
        for stream in self.streams:
            try:
                stream.write(data)
            except UnicodeError:
                stream.write(data.encode('UTF-8'))

            stream.flush()


def base_environ(cfg):
    return {'wsgi.errors': WSGIErrorsWrapper(cfg), 
       'wsgi.version': (1, 0), 
       'wsgi.multithread': False, 
       'wsgi.multiprocess': cfg.workers > 1, 
       'wsgi.run_once': False, 
       'wsgi.file_wrapper': FileWrapper, 
       'SERVER_SOFTWARE': SERVER_SOFTWARE}


def default_environ(req, sock, cfg):
    env = base_environ(cfg)
    env.update({'wsgi.input': req.body, 
       'gunicorn.socket': sock, 
       'REQUEST_METHOD': req.method, 
       'QUERY_STRING': req.query, 
       'RAW_URI': req.uri, 
       'SERVER_PROTOCOL': 'HTTP/%s' % ('.').join([ str(v) for v in req.version ])})
    return env


def proxy_environ(req):
    info = req.proxy_protocol_info
    if not info:
        return {}
    return {'PROXY_PROTOCOL': info['proxy_protocol'], 
       'REMOTE_ADDR': info['client_addr'], 
       'REMOTE_PORT': str(info['client_port']), 
       'PROXY_ADDR': info['proxy_addr'], 
       'PROXY_PORT': str(info['proxy_port'])}


def create(req, sock, client, server, cfg):
    resp = Response(req, sock, cfg)
    environ = default_environ(req, sock, cfg)
    host = None
    script_name = os.environ.get('SCRIPT_NAME', '')
    for hdr_name, hdr_value in req.headers:
        if hdr_name == 'EXPECT':
            if hdr_value.lower() == '100-continue':
                sock.send('HTTP/1.1 100 Continue\r\n\r\n')
        elif hdr_name == 'HOST':
            host = hdr_value
        elif hdr_name == 'SCRIPT_NAME':
            script_name = hdr_value
        elif hdr_name == 'CONTENT-TYPE':
            environ['CONTENT_TYPE'] = hdr_value
            continue
        elif hdr_name == 'CONTENT-LENGTH':
            environ['CONTENT_LENGTH'] = hdr_value
            continue
        key = 'HTTP_' + hdr_name.replace('-', '_')
        if key in environ:
            hdr_value = '%s,%s' % (environ[key], hdr_value)
        environ[key] = hdr_value

    environ['wsgi.url_scheme'] = req.scheme
    if isinstance(client, string_types):
        environ['REMOTE_ADDR'] = client
    elif isinstance(client, binary_type):
        environ['REMOTE_ADDR'] = client.decode()
    else:
        environ['REMOTE_ADDR'] = client[0]
        environ['REMOTE_PORT'] = str(client[1])
    if isinstance(server, string_types):
        server = server.split(':')
        if len(server) == 1:
            if host:
                server = host.split(':')
                if len(server) == 1:
                    if req.scheme == 'http':
                        server.append(80)
                    elif req.scheme == 'https':
                        server.append(443)
                    else:
                        server.append('')
            else:
                server.append('')
    environ['SERVER_NAME'] = server[0]
    environ['SERVER_PORT'] = str(server[1])
    path_info = req.path
    if script_name:
        path_info = path_info.split(script_name, 1)[1]
    environ['PATH_INFO'] = unquote_to_wsgi_str(path_info)
    environ['SCRIPT_NAME'] = script_name
    environ.update(proxy_environ(req))
    return (resp, environ)


class Response(object):

    def __init__(self, req, sock, cfg):
        self.req = req
        self.sock = sock
        self.version = SERVER_SOFTWARE
        self.status = None
        self.chunked = False
        self.must_close = False
        self.headers = []
        self.headers_sent = False
        self.response_length = None
        self.sent = 0
        self.upgrade = False
        self.cfg = cfg
        return

    def force_close(self):
        self.must_close = True

    def should_close(self):
        if self.must_close or self.req.should_close():
            return True
        if self.response_length is not None or self.chunked:
            return False
        if self.req.method == 'HEAD':
            return False
        else:
            if self.status_code < 200 or self.status_code in (204, 304):
                return False
            return True

    def start_response(self, status, headers, exc_info=None):
        if exc_info:
            try:
                if self.status and self.headers_sent:
                    reraise(exc_info[0], exc_info[1], exc_info[2])
            finally:
                exc_info = None

        else:
            if self.status is not None:
                raise AssertionError('Response headers already set!')
            self.status = status
            try:
                self.status_code = int(self.status.split()[0])
            except ValueError:
                self.status_code = None

        self.process_headers(headers)
        self.chunked = self.is_chunked()
        return self.write

    def process_headers(self, headers):
        for name, value in headers:
            if not isinstance(name, string_types):
                raise TypeError('%r is not a string' % name)
            if HEADER_RE.search(name):
                raise InvalidHeaderName('%r' % name)
            if HEADER_VALUE_RE.search(value):
                raise InvalidHeader('%r' % value)
            value = str(value).strip()
            lname = name.lower().strip()
            if lname == 'content-length':
                self.response_length = int(value)
            elif util.is_hoppish(name):
                if lname == 'connection':
                    if value.lower().strip() == 'upgrade':
                        self.upgrade = True
                elif lname == 'upgrade':
                    if value.lower().strip() == 'websocket':
                        self.headers.append((name.strip(), value))
                continue
            self.headers.append((name.strip(), value))

    def is_chunked(self):
        if self.response_length is not None:
            return False
        else:
            if self.req.version <= (1, 0):
                return False
            if self.req.method == 'HEAD':
                return False
            if self.status_code in (204, 304):
                return False
            return True

    def default_headers(self):
        if self.upgrade:
            connection = 'upgrade'
        elif self.should_close():
            connection = 'close'
        else:
            connection = 'keep-alive'
        headers = [
         'HTTP/%s.%s %s\r\n' % (self.req.version[0],
          self.req.version[1], self.status),
         'Server: %s\r\n' % self.version,
         'Date: %s\r\n' % util.http_date(),
         'Connection: %s\r\n' % connection]
        if self.chunked:
            headers.append('Transfer-Encoding: chunked\r\n')
        return headers

    def send_headers(self):
        if self.headers_sent:
            return
        tosend = self.default_headers()
        tosend.extend([ '%s: %s\r\n' % (k, v) for k, v in self.headers ])
        header_str = '%s\r\n' % ('').join(tosend)
        util.write(self.sock, util.to_bytestring(header_str, 'ascii'))
        self.headers_sent = True

    def write(self, arg):
        self.send_headers()
        if not isinstance(arg, binary_type):
            raise TypeError('%r is not a byte' % arg)
        arglen = len(arg)
        tosend = arglen
        if self.response_length is not None:
            if self.sent >= self.response_length:
                return
            tosend = min(self.response_length - self.sent, tosend)
            if tosend < arglen:
                arg = arg[:tosend]
        if self.chunked and tosend == 0:
            return
        else:
            self.sent += tosend
            util.write(self.sock, arg, self.chunked)
            return

    def can_sendfile(self):
        return self.cfg.sendfile is not False and sendfile is not None

    def sendfile(self, respiter):
        if self.cfg.is_ssl or not self.can_sendfile():
            return False
        if not util.has_fileno(respiter.filelike):
            return False
        else:
            fileno = respiter.filelike.fileno()
            try:
                offset = os.lseek(fileno, 0, os.SEEK_CUR)
                if self.response_length is None:
                    filesize = os.fstat(fileno).st_size
                    if filesize == 0:
                        return False
                    nbytes = filesize - offset
                else:
                    nbytes = self.response_length
            except (OSError, io.UnsupportedOperation):
                return False

            self.send_headers()
            if self.is_chunked():
                chunk_size = '%X\r\n' % nbytes
                self.sock.sendall(chunk_size.encode('utf-8'))
            sockno = self.sock.fileno()
            sent = 0
            while sent != nbytes:
                count = min(nbytes - sent, BLKSIZE)
                sent += sendfile(sockno, fileno, offset + sent, count)

            if self.is_chunked():
                self.sock.sendall('\r\n')
            os.lseek(fileno, offset, os.SEEK_SET)
            return True

    def write_file(self, respiter):
        if not self.sendfile(respiter):
            for item in respiter:
                self.write(item)

    def close(self):
        if not self.headers_sent:
            self.send_headers()
        if self.chunked:
            util.write_chunk(self.sock, '')