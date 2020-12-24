# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/utils/protocol/xmlrpc.py
# Compiled at: 2015-07-09 11:05:16
import base64, cookielib, httplib, socket, urllib2, xmlrpclib

class TimeoutHTTP(httplib.HTTP):

    def __init__(self, host='', port=None, strict=None, timeout=None):
        if port == 0:
            port = None
        self._setup(self._connection_class(host, port, strict, timeout))
        return


class TimeoutHTTPS(httplib.HTTPS):

    def __init__(self, host='', port=None, strict=None, timeout=None):
        if port == 0:
            port = None
        self._setup(self._connection_class(host, port, strict, timeout))
        return


class XMLRPCCookieAuthTransport(xmlrpclib.Transport):
    """An XML-RPC transport handling authentication via cookies"""
    _http_connection = httplib.HTTPConnection
    _http_connection_compat = TimeoutHTTP

    def __init__(self, user_agent, credentials=(), cookies=None, timeout=socket._GLOBAL_DEFAULT_TIMEOUT, headers=None):
        xmlrpclib.Transport.__init__(self)
        self.user_agent = user_agent
        self.credentials = credentials
        self.cookies = cookies
        self.timeout = timeout
        self.headers = headers
        if self._connection_required_compat():
            self.make_connection = self._make_connection_compat
            self.get_response = self._get_response_compat

    def _connection_required_compat(self):
        try:
            self._connection
            return False
        except AttributeError:
            return True

    def make_connection(self, host):
        if self._connection and host == self._connection[0]:
            return self._connection[1]
        chost, self._extra_headers, _x509 = self.get_host_info(host)
        self._connection = (host, self._http_connection(chost, timeout=self.timeout))
        return self._connection[1]

    def _make_connection_compat(self, host):
        host, _extra_headers, _x509 = self.get_host_info(host)
        return self._http_connection_compat(host, timeout=self.timeout)

    def send_host(self, connection, host):
        xmlrpclib.Transport.send_host(self, connection, host)
        if self.cookies is not None and len(self.cookies) > 0:
            for cookie in self.cookies:
                connection.putheader('Cookie', '%s=%s' % (cookie.name, cookie.value))

        elif self.credentials:
            auth = 'Basic %s' % base64.encodestring('%s:%s' % self.credentials).strip()
            connection.putheader('Authorization', auth)
        return

    def send_headers(self, connection):
        for k, v in (self.headers or {}).iteritems():
            connection.putheader(k, v)

    class CookieRequest(urllib2.Request):
        pass

    class CookieResponseHelper:

        def __init__(self, response):
            self.response = response

        def getheaders(self, header):
            return self.response.msg.getallmatchingheaders(header)

    class CookieResponse:

        def __init__(self, response):
            self.response = response

        def info(self):
            return XMLRPCCookieAuthTransport.CookieResponseHelper(self.response)

    class CompatCookieResponse:

        def __init__(self, headers):
            self.headers = headers

        def info(self):
            return self.headers

    def request(self, host, handler, request_body, verbose=False):
        connection = self.make_connection(host)
        self.verbose = verbose
        if verbose:
            connection.set_debuglevel(1)
        self.send_request(connection, handler, request_body)
        self.send_host(connection, host)
        self.send_user_agent(connection)
        self.send_headers(connection)
        self.send_content(connection, request_body)
        return self.get_response(connection, host, handler)

    def get_response(self, connection, host, handler):
        response = connection.getresponse()
        if self.cookies is not None:
            crequest = XMLRPCCookieAuthTransport.CookieRequest('http://%s/' % host)
            cresponse = XMLRPCCookieAuthTransport.CookieResponse(response)
            for cookie in self.cookies.make_cookies(cresponse, crequest):
                if cookie.name.startswith('Set-Cookie'):
                    cookie.name = cookie.name.split(': ', 1)[1]
                self.cookies.set_cookie(cookie)

        if response.status != 200:
            raise xmlrpclib.ProtocolError(host + handler, response.status, response.reason, response.getheaders())
        return self.parse_response(response)

    def _get_response_compat(self, connection, host, handler):
        errcode, errmsg, headers = connection.getreply()
        if self.cookies is not None:
            crequest = XMLRPCCookieAuthTransport.CookieRequest('http://%s/' % host)
            cresponse = XMLRPCCookieAuthTransport.CompatCookieResponse(headers)
            self.cookies.extract_cookies(cresponse, crequest)
        if errcode != 200:
            raise xmlrpclib.ProtocolError(host + handler, errcode, errmsg, headers)
        try:
            sock = connection._conn.sock
        except AttributeError:
            sock = None

        return self._parse_response(connection.getfile(), sock)


class SecureXMLRPCCookieAuthTransport(XMLRPCCookieAuthTransport):
    """Secure XML-RPC transport"""
    _http_connection = httplib.HTTPSConnection
    _http_connection_compat = TimeoutHTTPS


def getClient(uri, credentials=(), verbose=False, allow_none=0, timeout=socket._GLOBAL_DEFAULT_TIMEOUT, headers=None):
    """Get an XML-RPC client which supports basic authentication"""
    if uri.startswith('https:'):
        transport = SecureXMLRPCCookieAuthTransport('Python XML-RPC Client/0.1 (ZTFY secure transport)', credentials, timeout=timeout, headers=headers)
    else:
        transport = XMLRPCCookieAuthTransport('Python XML-RPC Client/0.1 (ZTFY basic transport)', credentials, timeout=timeout, headers=headers)
    return xmlrpclib.Server(uri, transport=transport, verbose=verbose, allow_none=allow_none)


def getClientWithCookies(uri, credentials=(), verbose=False, allow_none=0, timeout=socket._GLOBAL_DEFAULT_TIMEOUT, headers=None, cookies=None):
    """Get an XML-RPC client which supports authentication through cookies"""
    if cookies is None:
        cookies = cookielib.CookieJar()
    if uri.startswith('https:'):
        transport = SecureXMLRPCCookieAuthTransport('Python XML-RPC Client/0.1 (ZTFY secure cookie transport)', credentials, cookies, timeout, headers)
    else:
        transport = XMLRPCCookieAuthTransport('Python XML-RPC Client/0.1 (ZTFY basic cookie transport)', credentials, cookies, timeout, headers)
    return xmlrpclib.Server(uri, transport=transport, verbose=verbose, allow_none=allow_none)