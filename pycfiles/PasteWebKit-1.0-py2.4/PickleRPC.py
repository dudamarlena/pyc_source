# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/paste/webkit/FakeWebware/MiscUtils/PickleRPC.py
# Compiled at: 2006-10-22 17:01:01
"""
PickleRPC provides a Server object for connection to Pickle-RPC servers
for the purpose of making requests and receiving the responses.

        >>> from MiscUtils.PickleRPC import Server
        >>> server = Server('http://localhost/cgi-bin/WebKit.cgi/Examples/PickleRPCExample')
        >>> server.multiply(10,20)
        200
        >>> server.add(10,20)
        30

See also: Server, Webkit.PickleRPCServlet, WebKit.Examples.PickleRPCExample

UNDER THE HOOD

Requests look like this:
        {
                'version':    1,  # default
                'action':     'call',  # default
                'methodName': 'NAME',
                'args':       (A, B, ...), # default = (,)
                'keywords':   {'A': A, 'B': B, ...}  # default = {}
        }

Only 'methodName' is required since that is the only key without a
default value.

Responses look like this:
        {
                'timeReceived': N,
                'timeReponded': M,
                'value': V,
                'exception': E,
                'requestError': E,
        }

TimeReceived is the time the initial request was received.
TimeResponded is the time at which the response was finished, as
close to transmission as possible. The times are expressed as
number of seconds since the Epoch, e.g., time.time().

Value is whatever the method happened to return.

Exception may be 'occurred' to indicate that an exception
occurred, the specific exception, such as "KeyError: foo" or the
entire traceback (as a string), at the discretion of the server.
It will always be a non-empty string if it is present.

RequestError is an exception such as "Missing method
in request." (with no traceback) that indicates a problem with the
actual request received by the Pickle-RPC server.

Value, exception and requestError are all exclusive to each other.

SECURITY

Pickle RPC uses the SafeUnpickler class (in this module) to
prevent unpickling of unauthorized classes.  By default, it
doesn't allow _any_ classes to be unpickled.  You can override
allowedGlobals() or findGlobal() in a subclass as needed to
allow specific class instances to be unpickled.

Note that both Transport in this module and PickleRPCServlet in
WebKit are derived from SafeUnpickler.

CREDIT

The implementation of this module was taken directly from Python 2.2's
xmlrpclib and then transformed from XML-orientation to Pickle-orientation.

The zlib compression was adapted from code by Skip Montanaro that I found
here: http://manatee.mojam.com/~skip/python/
"""
__version__ = 1
import types
try:
    from cPickle import dumps, Unpickler, UnpicklingError
except ImportError:
    from pickle import dumps, Unpickler, UnpicklingError

try:
    import zlib
except ImportError:
    zlib = None

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

class Error(Exception):
    """
        The abstract exception/error class for all PickleRPC errors.
        """
    __module__ = __name__


class ResponseError(Error):
    """
        These are unhandled exceptions raised when the server was computing
        a response. These will indicate errors such as:
                * exception in the actual target method on the server
                * malformed responses
                * non "200 OK" status code responses
        """
    __module__ = __name__


try:
    from xmlrpclib.xmlrpclib import ProtocolError as _PE
except ImportError:
    from xmlrpclib import ProtocolError as _PE

class ProtocolError(ResponseError, _PE):
    __module__ = __name__


class RequestError(Error):
    """
        These are errors originally raised by the server complaining about
        malformed requests.
        """
    __module__ = __name__


class InvalidContentTypeError(ResponseError):
    __module__ = __name__

    def __init__(self, headers, content):
        Exception.__init__(self)
        self.headers = headers
        self.content = content

    def __repr__(self):
        content = self.content
        return '%s: Content type is not text/x-python-pickled-dict\nheaders = %s\ncontent =\n%s' % (self.__class__.__name__, self.headers, content)

    __str__ = __repr__


class SafeUnpickler:
    """
        For security reasons, we don't want to allow just anyone to unpickle
        anything.  That can cause arbitrary code to be executed.
        So this SafeUnpickler base class is used to control
        what can be unpickled.  By default it doesn't let you unpickle
        any class instances at all, but you can create subclass that
        overrides allowedGlobals().

        Note that the PickleRPCServlet class in WebKit is derived from this class
        and uses its load() and loads() methods to do all unpickling.
        """
    __module__ = __name__

    def allowedGlobals(self):
        """
                Must return a list of (moduleName, klassName) tuples for all
                classes that you want to allow to be unpickled.

                Example:
                        return [('mx.DateTime', '_DT')]
                allows mx.DateTime instances to be unpickled.
                """
        return []

    def findGlobal(self, module, klass):
        if (
         module, klass) not in self.allowedGlobals():
            raise UnpicklingError, "For security reasons, you can't unpickle objects from module %s with type %s" % (module, klass)
        globals = {}
        exec 'from %s import %s as theClass' % (module, klass) in globals
        return globals['theClass']

    def load(self, file):
        safeUnpickler = Unpickler(file)
        safeUnpickler.find_global = self.findGlobal
        return safeUnpickler.load()

    def loads(self, str):
        return self.load(StringIO(str))


class Server:
    """uri [,options] -> a logical connection to an XML-RPC server

        uri is the connection point on the server, given as
        scheme://host/target.

        The standard implementation always supports the "http" scheme.  If
        SSL socket support is available (Python 2.0), it also supports
        "https".

        If the target part and the slash preceding it are both omitted,
        "/PickleRPC" is assumed.

        See the module doc string for more information.
        """
    __module__ = __name__

    def __init__(self, uri, transport=None, verbose=0, binary=1, compressRequest=1, acceptCompressedResponse=1):
        import urllib
        (type, uri) = urllib.splittype(uri)
        if type not in ('http', 'https'):
            raise IOError, 'unsupported Pickle-RPC protocol'
        (self.__host, self.__handler) = urllib.splithost(uri)
        if not self.__handler:
            self.__handler = '/PickleRPC'
        if transport is None:
            if type == 'https':
                transport = SafeTransport()
            else:
                transport = Transport()
        self.__transport = transport
        self.__verbose = verbose
        self.__binary = binary
        self.__compressRequest = compressRequest
        self.__acceptCompressedResponse = acceptCompressedResponse
        return

    def _request(self, methodName, args, keywords):
        """
                Call a method on the remote server.
                """
        request = {'version': 1, 'action': 'call', 'methodName': methodName, 'args': args, 'keywords': keywords}
        if self.__binary:
            request = dumps(request, 1)
        else:
            request = dumps(request)
        if zlib is not None and self.__compressRequest and len(request) > 1000:
            request = zlib.compress(request, 1)
            compressed = 1
        else:
            compressed = 0
        response = self.__transport.request(self.__host, self.__handler, request, verbose=self.__verbose, binary=self.__binary, compressed=compressed, acceptCompressedResponse=self.__acceptCompressedResponse)
        return response

    def __requestValue(self, methodName, args, keywords):
        dict = self._request(methodName, args, keywords)
        if dict.has_key('value'):
            return dict['value']
        elif dict.has_key('exception'):
            raise ResponseError, dict['exception']
        elif dict.has_key('requestError'):
            raise RequestError, dict['requestError']
        else:
            raise RequestError, 'Response does not have a value, expection or requestError.'

    def __repr__(self):
        return '<%s for %s%s>' % (self.__class__.__name__, self.__host, self.__handler)

    __str__ = __repr__

    def __getattr__(self, name):
        return _Method(self.__requestValue, name)


ServerProxy = Server

class _Method:
    """
        Some magic to bind a Pickle-RPC method to an RPC server.
        Supports "nested" methods (e.g. examples.getStateName).
        """
    __module__ = __name__

    def __init__(self, send, name):
        self.__send = send
        self.__name = name

    def __getattr__(self, name):
        return _Method(self.__send, '%s.%s' % (self.__name, name))

    def __call__(self, *args, **keywords):
        return self.__send(self.__name, args, keywords)


class Transport(SafeUnpickler):
    """
        Handles an HTTP transaction to a Pickle-RPC server.
        """
    __module__ = __name__
    user_agent = 'PickleRPC/%s (by http://webware.sf.net/)' % __version__

    def request(self, host, handler, request_body, verbose=0, binary=0, compressed=0, acceptCompressedResponse=0):
        h = self.make_connection(host)
        if verbose:
            h.set_debuglevel(1)
        self.send_request(h, handler, request_body)
        self.send_host(h, host)
        self.send_user_agent(h)
        self.send_content(h, request_body, binary, compressed, acceptCompressedResponse)
        (errcode, errmsg, headers) = h.getreply()
        if errcode != 200:
            raise ProtocolError(host + handler, errcode, errmsg, headers)
        self.verbose = verbose
        if h.headers['content-type'] not in ['text/x-python-pickled-dict', 'application/x-python-binary-pickled-dict']:
            headers = h.headers.headers
            content = h.getfile().read()
            raise InvalidContentTypeError(headers, content)
        try:
            content_encoding = headers['content-encoding']
            if content_encoding and content_encoding == 'x-gzip':
                return self.parse_response_gzip(h.getfile())
            elif content_encoding:
                raise ProtocolError(host + handler, 500, 'Unknown encoding type: %s' % content_encoding, headers)
            else:
                return self.parse_response(h.getfile())
        except KeyError:
            return self.parse_response(h.getfile())

    def make_connection(self, host):
        import httplib
        return httplib.HTTP(host)

    def send_request(self, connection, handler, request_body):
        connection.putrequest('POST', handler)

    def send_host(self, connection, host):
        connection.putheader('Host', host)

    def send_user_agent(self, connection):
        connection.putheader('User-Agent', self.user_agent)

    def send_content(self, connection, request_body, binary=0, compressed=0, acceptCompressedResponse=0):
        if binary:
            connection.putheader('Content-Type', 'application/x-python-binary-pickled-dict')
        else:
            connection.putheader('Content-Type', 'text/x-python-pickled-dict')
        connection.putheader('Content-Length', str(len(request_body)))
        if compressed:
            connection.putheader('Content-Encoding', 'x-gzip')
        if zlib is not None and acceptCompressedResponse:
            connection.putheader('Accept-Encoding', 'gzip')
        connection.endheaders()
        if request_body:
            connection.send(request_body)
        return

    def parse_response(self, f):
        return self.load(f)

    def parse_response_gzip(self, f):
        return self.loads(zlib.decompress(f.read()))


class SafeTransport(Transport):
    """
        Handles an HTTPS transaction to a Pickle-RPC server.
        """
    __module__ = __name__

    def make_connection(self, host):
        import httplib
        if isinstance(host, types.TupleType):
            (host, x509) = host
        else:
            x509 = {}
        try:
            HTTPS = httplib.HTTPS
        except AttributeError:
            raise NotImplementedError, "your version of httplib doesn't support HTTPS"
        else:
            return apply(HTTPS, (host, None), x509)

        return

    def send_host(self, connection, host):
        if isinstance(host, types.TupleType):
            (host, x509) = host
        connection.putheader('Host', host)