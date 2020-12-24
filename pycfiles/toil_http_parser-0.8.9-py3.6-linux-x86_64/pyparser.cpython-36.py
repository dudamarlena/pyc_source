# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/toil_http_parser/pyparser.py
# Compiled at: 2020-04-09 00:11:53
# Size of source mod 2**32: 15347 bytes
import os, re, sys
if sys.version_info >= (3, ):
    import urllib.parse as urlparse
else:
    import urlparse
import zlib
from toil_http_parser.util import b, bytes_to_str, IOrderedDict, StringIO, unquote, MAXSIZE
METHOD_RE = re.compile('[A-Z0-9$-_.]{3,20}')
VERSION_RE = re.compile('HTTP/(\\d+).(\\d+)')
STATUS_RE = re.compile('(\\d{3})\\s*(\\w*)')
HEADER_RE = re.compile('[\x00-\x1f\x7f()<>@,;:\\[\\]={} \t\\\\"]')
BAD_FIRST_LINE = 0
INVALID_HEADER = 1
INVALID_CHUNK = 2

class InvalidRequestLine(Exception):
    __doc__ = ' error raised when first line is invalid '


class InvalidHeader(Exception):
    __doc__ = ' error raised on invalid header '


class InvalidChunkSize(Exception):
    __doc__ = ' error raised when we parse an invalid chunk size '


class HttpParser(object):

    def __init__(self, kind=2, decompress=False):
        self.kind = kind
        self.decompress = decompress
        self.errno = None
        self.errstr = ''
        self._buf = []
        self._version = None
        self._method = None
        self._status_code = None
        self._status = None
        self._reason = None
        self._url = None
        self._path = None
        self._query_string = None
        self._fragment = None
        self._headers = IOrderedDict()
        self._environ = dict()
        self._chunked = False
        self._body = []
        self._trailers = None
        self._partial_body = False
        self._clen = None
        self._clen_rest = None
        self._HttpParser__on_firstline = False
        self._HttpParser__on_headers_complete = False
        self._HttpParser__on_message_begin = False
        self._HttpParser__on_message_complete = False
        self._HttpParser__decompress_obj = None
        self._HttpParser__decompress_first_try = True

    def get_version(self):
        return self._version

    def get_method(self):
        return self._method

    def get_status_code(self):
        return self._status_code

    def get_url(self):
        return self._url

    def get_path(self):
        return self._path

    def get_query_string(self):
        return self._query_string

    def get_fragment(self):
        return self._fragment

    def get_headers(self):
        return self._headers

    def get_wsgi_environ(self):
        if not self._HttpParser__on_headers_complete:
            return
        else:
            environ = self._environ.copy()
            for key in ('CONTENT_LENGTH', 'CONTENT_TYPE', 'SCRIPT_NAME'):
                hkey = 'HTTP_%s' % key
                if hkey in environ:
                    environ[key] = environ.pop(hkey)

            script_name = environ.get('SCRIPT_NAME', os.environ.get('SCRIPT_NAME', ''))
            if script_name:
                path_info = self._path.split(script_name, 1)[1]
                environ.update({'PATH_INFO':unquote(path_info), 
                 'SCRIPT_NAME':script_name})
            else:
                environ['SCRIPT_NAME'] = ''
            if environ.get('HTTP_X_FORWARDED_PROTOCOL', '').lower() == 'ssl':
                environ['wsgi.url_scheme'] = 'https'
            else:
                if environ.get('HTTP_X_FORWARDED_SSL', '').lower() == 'on':
                    environ['wsgi.url_scheme'] = 'https'
                else:
                    environ['wsgi.url_scheme'] = 'http'
            return environ

    def recv_body(self):
        """ return last chunk of the parsed body"""
        body = b('').join(self._body)
        self._body = []
        self._partial_body = False
        return body

    def recv_body_into(self, barray):
        """ Receive the last chunk of the parsed body and store the data
        in a buffer rather than creating a new string. """
        l = len(barray)
        body = b('').join(self._body)
        m = min(len(body), l)
        data, rest = body[:m], body[m:]
        barray[0:m] = data
        if not rest:
            self._body = []
            self._partial_body = False
        else:
            self._body = [
             rest]
        return m

    def is_upgrade(self):
        """ Do we get upgrade header in the request. Useful for
        websockets """
        return self._headers.get('connection', '').lower() == 'upgrade'

    def is_headers_complete(self):
        """ return True if all headers have been parsed. """
        return self._HttpParser__on_headers_complete

    def is_partial_body(self):
        """ return True if a chunk of body have been parsed """
        return self._partial_body

    def is_message_begin(self):
        """ return True if the parsing start """
        return self._HttpParser__on_message_begin

    def is_message_complete(self):
        """ return True if the parsing is done (we get EOF) """
        return self._HttpParser__on_message_complete

    def is_chunked(self):
        """ return True if Transfer-Encoding header value is chunked"""
        return self._chunked

    def should_keep_alive(self):
        """ return True if the connection should be kept alive
        """
        hconn = self._headers.get('connection', '').lower()
        if hconn == 'close':
            return False
        else:
            if hconn == 'keep-alive':
                return True
            return self._version == (1, 1)

    def execute(self, data, length):
        if length == 0:
            self._HttpParser__on_message_complete = True
            return length
        nb_parsed = 0
        while True:
            if not self._HttpParser__on_firstline:
                idx = data.find(b('\r\n'))
                if idx < 0:
                    self._buf.append(data)
                    return len(data)
                self._HttpParser__on_firstline = True
                self._buf.append(data[:idx])
                first_line = bytes_to_str(b('').join(self._buf))
                nb_parsed = nb_parsed + idx + 2
                rest = data[idx + 2:]
                data = b('')
                if self._parse_firstline(first_line):
                    self._buf = [
                     rest]
                else:
                    return nb_parsed
            elif not self._HttpParser__on_headers_complete:
                if data:
                    self._buf.append(data)
                    data = b('')
                try:
                    to_parse = b('').join(self._buf)
                    ret = self._parse_headers(to_parse)
                    if type(ret) is bool:
                        if not ret:
                            return length
                    nb_parsed = nb_parsed + (len(to_parse) - ret)
                except InvalidHeader as e:
                    self.errno = INVALID_HEADER
                    self.errstr = str(e)
                    return nb_parsed

            else:
                if not self._HttpParser__on_message_complete:
                    if not self._HttpParser__on_message_begin:
                        self._HttpParser__on_message_begin = True
                    else:
                        if data:
                            self._buf.append(data)
                            data = b('')
                        else:
                            ret = self._parse_body()
                            if ret is None:
                                return length
                            if ret < 0:
                                return ret
                        if ret == 0:
                            self._HttpParser__on_message_complete = True
                            return length
                    nb_parsed = max(length, ret)
                else:
                    return 0

    def _parse_firstline(self, line):
        try:
            if self.kind == 2:
                try:
                    self._parse_request_line(line)
                except InvalidRequestLine:
                    self._parse_response_line(line)

            else:
                if self.kind == 1:
                    self._parse_response_line(line)
                else:
                    if self.kind == 0:
                        self._parse_request_line(line)
        except InvalidRequestLine as e:
            self.errno = BAD_FIRST_LINE
            self.errstr = str(e)
            return False

        return True

    def _parse_response_line(self, line):
        bits = line.split(None, 1)
        if len(bits) != 2:
            raise InvalidRequestLine(line)
        matchv = VERSION_RE.match(bits[0])
        if matchv is None:
            raise InvalidRequestLine('Invalid HTTP version: %s' % bits[0])
        self._version = (
         int(matchv.group(1)), int(matchv.group(2)))
        matchs = STATUS_RE.match(bits[1])
        if matchs is None:
            raise InvalidRequestLine('Invalid status %' % bits[1])
        self._status = bits[1]
        self._status_code = int(matchs.group(1))
        self._reason = matchs.group(2)

    def _parse_request_line(self, line):
        bits = line.split(None, 2)
        if len(bits) != 3:
            raise InvalidRequestLine(line)
        if not METHOD_RE.match(bits[0]):
            raise InvalidRequestLine('invalid Method: %s' % bits[0])
        self._method = bits[0].upper()
        self._url = bits[1]
        parts = urlparse.urlsplit(bits[1])
        self._path = parts.path or ''
        self._query_string = parts.query or ''
        self._fragment = parts.fragment or ''
        match = VERSION_RE.match(bits[2])
        if match is None:
            raise InvalidRequestLine('Invalid HTTP version: %s' % bits[2])
        self._version = (
         int(match.group(1)), int(match.group(2)))
        if hasattr(self, '_environ'):
            self._environ.update({'PATH_INFO':self._path, 
             'QUERY_STRING':self._query_string, 
             'RAW_URI':self._url, 
             'REQUEST_METHOD':self._method, 
             'SERVER_PROTOCOL':bits[2]})

    def _parse_headers(self, data):
        idx = data.find(b('\r\n\r\n'))
        if idx < 0:
            if self._status_code == 204 and data == b('\r\n'):
                self._buf = []
                self._HttpParser__on_headers_complete = True
                return 0
            else:
                return False
        lines = [bytes_to_str(line) + '\r\n' for line in data[:idx].split(b('\r\n'))]
        while len(lines):
            curr = lines.pop(0)
            if curr.find(':') < 0:
                raise InvalidHeader('invalid line %s' % curr.strip())
            name, value = curr.split(':', 1)
            name = name.rstrip(' \t').upper()
            if HEADER_RE.search(name):
                raise InvalidHeader('invalid header name %s' % name)
            if value.endswith('\r\n'):
                value = value[:-2]
            name, value = name.strip(), [value.lstrip()]
            while len(lines) and lines[0].startswith((' ', '\t')):
                curr = lines.pop(0)
                if curr.endswith('\r\n'):
                    curr = curr[:-2]
                value.append(curr)

            value = ''.join(value).rstrip()
            if name in self._headers:
                value = '%s, %s' % (self._headers[name], value)
            self._headers[name] = value
            key = 'HTTP_%s' % name.upper().replace('-', '_')
            self._environ[key] = value

        clen = self._headers.get('content-length')
        te = self._headers.get('transfer-encoding', '').lower()
        if clen is not None:
            try:
                self._clen_rest = self._clen = int(clen)
            except ValueError:
                pass

        else:
            self._chunked = te == 'chunked'
            if not self._chunked:
                self._clen_rest = MAXSIZE
            encoding = self._headers.get('content-encoding')
            if self.decompress:
                if encoding == 'gzip':
                    self._HttpParser__decompress_obj = zlib.decompressobj(16 + zlib.MAX_WBITS)
                    self._HttpParser__decompress_first_try = False
                elif encoding == 'deflate':
                    self._HttpParser__decompress_obj = zlib.decompressobj()
            rest = data[idx + 4:]
            self._buf = [rest]
            self._HttpParser__on_headers_complete = True
            return len(rest)

    def _parse_body(self):
        if self._status_code == 204:
            if len(self._buf) == 0:
                self._HttpParser__on_message_complete = True
                return
            else:
                if not self._chunked:
                    body_part = b('').join(self._buf)
                    self._clen_rest -= len(body_part)
                    if self._HttpParser__decompress_obj is not None:
                        body_part = self._HttpParser__decompress_first_try or self._HttpParser__decompress_obj.decompress(body_part)
                else:
                    try:
                        body_part = self._HttpParser__decompress_obj.decompress(body_part)
                    except zlib.error:
                        self._HttpParser__decompress_obj.decompressobj = zlib.decompressobj(-zlib.MAX_WBITS)
                        body_part = self._HttpParser__decompress_obj.decompress(body_part)

                    self._HttpParser__decompress_first_try = False
                self._partial_body = True
                self._body.append(body_part)
                self._buf = []
                if self._clen_rest <= 0:
                    self._HttpParser__on_message_complete = True
            return
        else:
            data = b('').join(self._buf)
            try:
                size, rest = self._parse_chunk_size(data)
            except InvalidChunkSize as e:
                self.errno = INVALID_CHUNK
                self.errstr = 'invalid chunk size [%s]' % str(e)
                return -1

            if size == 0:
                return size
            if size is None or len(rest) < size:
                return
            body_part, rest = rest[:size], rest[size:]
            if len(rest) < 2:
                self.errno = INVALID_CHUNK
                self.errstr = 'chunk missing terminator [%s]' % data
                return -1
            if self._HttpParser__decompress_obj is not None:
                body_part = self._HttpParser__decompress_obj.decompress(body_part)
            self._partial_body = True
            self._body.append(body_part)
            self._buf = [
             rest[2:]]
            return len(rest)

    def _parse_chunk_size(self, data):
        idx = data.find(b('\r\n'))
        if idx < 0:
            return (None, None)
        else:
            line, rest_chunk = data[:idx], data[idx + 2:]
            chunk_size = line.split(b(';'), 1)[0].strip()
            try:
                chunk_size = int(chunk_size, 16)
            except ValueError:
                raise InvalidChunkSize(chunk_size)

            if chunk_size == 0:
                self._parse_trailers(rest_chunk)
                return (0, None)
            return (
             chunk_size, rest_chunk)

    def _parse_trailers(self, data):
        idx = data.find(b('\r\n\r\n'))
        if data[:2] == b('\r\n'):
            self._trailers = self._parse_headers(data[:idx])