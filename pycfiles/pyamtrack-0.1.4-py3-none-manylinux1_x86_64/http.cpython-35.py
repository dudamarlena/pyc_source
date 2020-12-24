# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_utils/protocol/http.py
# Compiled at: 2020-02-18 19:11:13
# Size of source mod 2**32: 3381 bytes
__doc__ = 'PyAMS_utils.protocol.http module\n\nThis module provides an HTTP client class, which allows to easilly define proxies and\nauthentication headers.\n'
import urllib.parse, httplib2
__docformat__ = 'restructuredtext'

class HTTPClient:
    """HTTPClient"""

    def __init__(self, method, protocol, servername, url, params=None, credentials=(), proxy=(), rdns=True, proxy_auth=(), timeout=None, headers=None):
        """Intialize HTTP connection"""
        self.connection = None
        self.method = method
        self.protocol = protocol
        self.servername = servername
        self.url = url
        self.params = params or {}
        self.location = None
        self.credentials = credentials
        self.proxy = proxy
        self.rdns = rdns
        self.proxy_auth = proxy_auth
        self.timeout = timeout
        self.headers = headers or {}
        if 'User-Agent' not in self.headers:
            self.headers['User-Agent'] = 'PyAMS HTTP Client/1.0'

    def get_response(self):
        """Common HTTP request"""
        if self.proxy and len(self.proxy) == 2:
            proxy_info = httplib2.ProxyInfo(httplib2.socks.PROXY_TYPE_HTTP, proxy_host=self.proxy[0], proxy_port=self.proxy[1], proxy_rdns=self.rdns, proxy_user=self.proxy_auth and self.proxy_auth[0] or None, proxy_pass=self.proxy_auth and self.proxy_auth[1] or None)
        else:
            proxy_info = None
        http = httplib2.Http(timeout=self.timeout, proxy_info=proxy_info)
        if self.credentials:
            http.add_credentials(self.credentials[0], self.credentials[1])
        uri = '%s://%s%s' % (self.protocol, self.servername, self.url)
        if self.params:
            uri += '?' + urllib.parse.urlencode(self.params)
        response, content = http.request(uri, self.method, headers=self.headers)
        return (
         response, content)


def get_client(method, protocol, servername, url, params=None, credentials=(), proxy=(), rdns=True, proxy_auth=(), timeout=None, headers=None):
    """HTTP client factory"""
    return HTTPClient(method, protocol, servername, url, params, credentials, proxy, rdns, proxy_auth, timeout, headers)


def get_client_from_url(url, credentials=(), proxy=(), rdns=True, proxy_auth=(), timeout=None, headers=None):
    """HTTP client factory from URL"""
    elements = urllib.parse.urlparse(url)
    return HTTPClient('GET', elements.scheme, elements.netloc, elements.path, elements.params, credentials, proxy, rdns, proxy_auth, timeout, headers)