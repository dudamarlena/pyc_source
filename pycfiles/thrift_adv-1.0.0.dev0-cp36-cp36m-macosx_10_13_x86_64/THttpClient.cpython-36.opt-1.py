# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /thrift/transport/THttpClient.py
# Compiled at: 2018-09-11 21:54:05
# Size of source mod 2**32: 7114 bytes
from io import BytesIO
import os, ssl, sys, warnings, base64
from six.moves import urllib
from six.moves import http_client
from .TTransport import TTransportBase
import six

class THttpClient(TTransportBase):
    __doc__ = 'Http implementation of TTransport base.'

    def __init__(self, uri_or_host, port=None, path=None, cafile=None, cert_file=None, key_file=None, ssl_context=None):
        """THttpClient supports two different types of construction:

        THttpClient(host, port, path) - deprecated
        THttpClient(uri, [port=<n>, path=<s>, cafile=<filename>, cert_file=<filename>, key_file=<filename>, ssl_context=<context>])

        Only the second supports https.  To properly authenticate against the server,
        provide the client's identity by specifying cert_file and key_file.  To properly
        authenticate the server, specify either cafile or ssl_context with a CA defined.
        NOTE: if both cafile and ssl_context are defined, ssl_context will override cafile.
        """
        if port is not None:
            warnings.warn("Please use the THttpClient('http{s}://host:port/path') constructor",
              DeprecationWarning,
              stacklevel=2)
            self.host = uri_or_host
            self.port = port
            assert path
            self.path = path
            self.scheme = 'http'
        else:
            parsed = urllib.parse.urlparse(uri_or_host)
            self.scheme = parsed.scheme
            assert self.scheme in ('http', 'https')
            if self.scheme == 'http':
                self.port = parsed.port or http_client.HTTP_PORT
            else:
                if self.scheme == 'https':
                    self.port = parsed.port or http_client.HTTPS_PORT
                    self.certfile = cert_file
                    self.keyfile = key_file
                    self.context = ssl.create_default_context(cafile=cafile) if (cafile and not ssl_context) else ssl_context
            self.host = parsed.hostname
            self.path = parsed.path
        if parsed.query:
            self.path += '?%s' % parsed.query
        try:
            proxy = urllib.request.getproxies()[self.scheme]
        except KeyError:
            proxy = None
        else:
            if urllib.request.proxy_bypass(self.host):
                proxy = None
            else:
                if proxy:
                    parsed = urllib.parse.urlparse(proxy)
                    self.realhost = self.host
                    self.realport = self.port
                    self.host = parsed.hostname
                    self.port = parsed.port
                    self.proxy_auth = self.basic_proxy_auth_header(parsed)
                else:
                    self.realhost = self.realport = self.proxy_auth = None
            self._THttpClient__wbuf = BytesIO()
            self._THttpClient__http = None
            self._THttpClient__http_response = None
            self._THttpClient__timeout = None
            self._THttpClient__custom_headers = None

    @staticmethod
    def basic_proxy_auth_header(proxy):
        if proxy is None or not proxy.username:
            return
        else:
            ap = '%s:%s' % (urllib.parse.unquote(proxy.username),
             urllib.parse.unquote(proxy.password))
            cr = base64.b64encode(ap).strip()
            return 'Basic ' + cr

    def using_proxy(self):
        return self.realhost is not None

    def open(self):
        if self.scheme == 'http':
            self._THttpClient__http = http_client.HTTPConnection((self.host), (self.port), timeout=(self._THttpClient__timeout))
        else:
            if self.scheme == 'https':
                self._THttpClient__http = http_client.HTTPSConnection((self.host), (self.port), key_file=(self.keyfile),
                  cert_file=(self.certfile),
                  timeout=(self._THttpClient__timeout),
                  context=(self.context))
        if self.using_proxy():
            self._THttpClient__http.set_tunnel(self.realhost, self.realport, {'Proxy-Authorization': self.proxy_auth})

    def close(self):
        self._THttpClient__http.close()
        self._THttpClient__http = None
        self._THttpClient__http_response = None

    def isOpen(self):
        return self._THttpClient__http is not None

    def setTimeout(self, ms):
        if ms is None:
            self._THttpClient__timeout = None
        else:
            self._THttpClient__timeout = ms / 1000.0

    def setCustomHeaders(self, headers):
        self._THttpClient__custom_headers = headers

    def read(self, sz):
        return self._THttpClient__http_response.read(sz)

    def write(self, buf):
        self._THttpClient__wbuf.write(buf)

    def flush(self):
        if self.isOpen():
            self.close()
        else:
            self.open()
            data = self._THttpClient__wbuf.getvalue()
            self._THttpClient__wbuf = BytesIO()
            if self.using_proxy():
                if self.scheme == 'http':
                    self._THttpClient__http.putrequest('POST', 'http://%s:%s%s' % (
                     self.realhost, self.realport, self.path))
            else:
                self._THttpClient__http.putrequest('POST', self.path)
            self._THttpClient__http.putheader('Content-Type', 'application/x-thrift')
            self._THttpClient__http.putheader('Content-Length', str(len(data)))
            if self.using_proxy():
                if self.scheme == 'http':
                    if self.proxy_auth is not None:
                        self._THttpClient__http.putheader('Proxy-Authorization', self.proxy_auth)
            if not self._THttpClient__custom_headers or 'User-Agent' not in self._THttpClient__custom_headers:
                user_agent = 'Python/THttpClient'
                script = os.path.basename(sys.argv[0])
                if script:
                    user_agent = '%s (%s)' % (user_agent, urllib.parse.quote(script))
                self._THttpClient__http.putheader('User-Agent', user_agent)
            if self._THttpClient__custom_headers:
                for key, val in six.iteritems(self._THttpClient__custom_headers):
                    self._THttpClient__http.putheader(key, val)

        self._THttpClient__http.endheaders()
        self._THttpClient__http.send(data)
        self._THttpClient__http_response = self._THttpClient__http.getresponse()
        self.code = self._THttpClient__http_response.status
        self.message = self._THttpClient__http_response.reason
        self.headers = self._THttpClient__http_response.msg