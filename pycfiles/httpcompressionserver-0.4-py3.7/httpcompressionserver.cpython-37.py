# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\httpcompressionserver.py
# Compiled at: 2019-02-25 10:51:11
# Size of source mod 2**32: 11970 bytes
"""Add HTTP compression support to http.server.

When a request sent by the client includes an Accept-Encoding header, the
server handles the value (eg "gzip", "x-gzip" or "deflate") and tries to
compress the response body with the requested algorithm.

Class HTTPCompressionRequestHandler extends SimpleHTTPRequestHandler with
2 additional attributes:
- compressed_types: the list of mimetypes that will be returned compressed by
  the server. By default, it is set to a list of commonly compressed types.
- compressions: a mapping between an Accept-Encoding value and a generator
  that produces compressed data.

Chunked Transfer Encoding is used to send the compressed response.
"""
__version__ = '0.3'
__all__ = [
 'ThreadingHTTPServer', 'HTTPCompressionRequestHandler']
import datetime, email.utils, http.cookiejar, io, os, socket, socketserver, sys, urllib.parse
from functools import partial
from http import HTTPStatus
from http.server import HTTPServer, BaseHTTPRequestHandler, SimpleHTTPRequestHandler, CGIHTTPRequestHandler, _url_collapse_path, test
try:
    import zlib
except ImportError:
    zlib = None

commonly_compressed_types = [
 'application/atom+xml',
 'application/javascript',
 'application/json',
 'application/ld+json',
 'application/manifest+json',
 'application/rdf+xml',
 'application/rss+xml',
 'application/schema+json',
 'application/vnd.geo+json',
 'application/vnd.ms-fontobject',
 'application/x-font-ttf',
 'application/x-javascript',
 'application/x-web-app-manifest+json',
 'application/xhtml+xml',
 'application/xml',
 'font/eot',
 'font/opentype',
 'image/bmp',
 'image/svg+xml',
 'image/vnd.microsoft.icon',
 'image/x-icon',
 'text/cache-manifest',
 'text/css',
 'text/html',
 'text/javascript',
 'text/plain',
 'text/vcard',
 'text/vnd.rim.location.xloc',
 'text/vtt',
 'text/x-component',
 'text/x-cross-domain-policy',
 'text/xml']

def _zlib_producer(fileobj, wbits):
    """Generator that yields data read from the file object fileobj,
    compressed with the zlib library.
    wbits is the same argument as for zlib.compressobj.
    """
    bufsize = 262144
    producer = zlib.compressobj(wbits=wbits)
    with fileobj:
        while 1:
            buf = fileobj.read(bufsize)
            if not buf:
                yield producer.flush()
                return
                yield producer.compress(buf)


def _gzip_producer(fileobj):
    """Generator for gzip compression."""
    return _zlib_producer(fileobj, 31)


def _deflate_producer(fileobj):
    """Generator for deflate compression."""
    return _zlib_producer(fileobj, 15)


class ThreadingHTTPServer(socketserver.ThreadingMixIn, HTTPServer):
    daemon_threads = True


class HTTPCompressionRequestHandler(SimpleHTTPRequestHandler):
    __doc__ = 'Extends SimpleHTTPRequestHandler to support HTTP compression\n    '
    server_version = 'CompressionHTTP/' + __version__
    compressed_types = commonly_compressed_types
    compressions = {}
    if zlib:
        compressions = {'deflate':_deflate_producer,  'gzip':_gzip_producer, 
         'x-gzip':_gzip_producer}

    def do_GET(self):
        """Serve a GET request."""
        f = self.send_head()
        if f:
            try:
                if hasattr(f, 'read'):
                    self.copyfile(f, self.wfile)
                else:
                    if self.protocol_version >= 'HTTP/1.1':
                        for data in f:
                            if data:
                                self.wfile.write(self._make_chunk(data))

                        self.wfile.write(self._make_chunk(b''))
                    else:
                        for data in f:
                            self.wfile.write(data)

            finally:
                f.close()

    def _make_chunk(self, data):
        """Make a data chunk in Chunked Transfer Encoding format."""
        return f"{len(data):X}".encode('ascii') + b'\r\n' + data + b'\r\n'

    def send_head(self):
        """Common code for GET and HEAD commands.

        This sends the response code and MIME headers.

        Return value is either:
        - a file object (which has to be copied to the outputfile by the
        caller unless the command was HEAD, and must be closed by the caller
        under all circumstances)
        - a generator of pieces of compressed data if HTTP compression is used
        - None, in which case the caller has nothing further to do
        """
        path = self.translate_path(self.path)
        f = None
        if os.path.isdir(path):
            parts = urllib.parse.urlsplit(self.path)
            if not parts.path.endswith('/'):
                self.send_response(HTTPStatus.MOVED_PERMANENTLY)
                new_parts = (parts[0], parts[1], parts[2] + '/',
                 parts[3], parts[4])
                new_url = urllib.parse.urlunsplit(new_parts)
                self.send_header('Location', new_url)
                self.end_headers()
                return
            for index in ('index.html', 'index.htm'):
                index = os.path.join(path, index)
                if os.path.exists(index):
                    path = index
                    break
            else:
                return self.list_directory(path)

        ctype = self.guess_type(path)
        try:
            f = open(path, 'rb')
        except OSError:
            self.send_error(HTTPStatus.NOT_FOUND, 'File not found')
            return
        else:
            try:
                fs = os.fstat(f.fileno())
                content_length = fs[6]
                if 'If-Modified-Since' in self.headers and 'If-None-Match' not in self.headers:
                    try:
                        ims = email.utils.parsedate_to_datetime(self.headers['If-Modified-Since'])
                    except (TypeError, IndexError, OverflowError, ValueError):
                        pass
                    else:
                        if ims.tzinfo is None:
                            ims = ims.replace(tzinfo=(datetime.timezone.utc))
                        if ims.tzinfo is datetime.timezone.utc:
                            last_modif = datetime.datetime.fromtimestamp(fs.st_mtime, datetime.timezone.utc)
                            last_modif = last_modif.replace(microsecond=0)
                            if last_modif <= ims:
                                self.send_response(HTTPStatus.NOT_MODIFIED)
                                self.end_headers()
                                f.close()
                                return
                        self.send_response(HTTPStatus.OK)
                        self.send_header('Content-type', ctype)
                        self.send_header('Last-Modified', self.date_time_string(fs.st_mtime))
                        if ctype not in self.compressed_types:
                            self.send_header('Content-Length', str(content_length))
                            self.end_headers()
                            return f
                        accept_encoding = self.headers.get_all('Accept-Encoding', ())
                        encodings = {}
                        for accept in http.cookiejar.split_header_words(accept_encoding):
                            params = iter(accept)
                            encoding = next(params, ('', ''))[0]
                            quality, value = next(params, ('', ''))
                            if quality == 'q':
                                if value:
                                    try:
                                        q = float(value)
                                    except ValueError:
                                        q = 0

                                else:
                                    q = 1
                                if q:
                                    encodings[encoding] = max(encodings.get(encoding, 0), q)

                        compressions = set(encodings).intersection(self.compressions)
                        compression = None
                        if compressions:
                            compression = max(((encodings[enc], enc) for enc in compressions))[1]
                else:
                    if '*' in encodings:
                        if self.compressions:
                            compression = list(self.compressions)[0]
                    if compression:
                        producer = self.compressions[compression]
                        self.send_header('Content-Encoding', compression)
                        if content_length < 524288:
                            with f:
                                content = (b'').join(producer(f))
                            content_length = len(content)
                            f = io.BytesIO(content)
                        else:
                            chunked = self.protocol_version >= 'HTTP/1.1'
                            if chunked:
                                self.send_header('Transfer-Encoding', 'chunked')
                            self.end_headers()
                            return producer(f)
                    self.send_header('Content-Length', str(content_length))
                    self.end_headers()
                return f
            except:
                f.close()
                raise


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--bind', '-b', default='', metavar='ADDRESS', help='Specify alternate bind address [default: all interfaces]')
    parser.add_argument('port', action='store', default=8000,
      type=int,
      nargs='?',
      help='Specify alternate port [default: 8000]')
    args = parser.parse_args()
    test(HandlerClass=HTTPCompressionRequestHandler, port=(args.port),
      bind=(args.bind))