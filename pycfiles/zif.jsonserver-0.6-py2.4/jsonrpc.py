# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/zif/jsonserver/jsonrpc.py
# Compiled at: 2007-05-25 16:54:18
__docformat__ = 'restructuredtext'
from zope.app.publication.http import BaseHTTPPublication
from interfaces import IMethodPublisher, IJSONRPCView, IJSONRPCPublisher, IJSONRPCRequest, IJSONReader, IJSONWriter, IJSONRPCPremarshaller, IJSONView
from zope.interface import implements
from zope.location.location import Location
from zope.publisher.http import HTTPRequest, HTTPResponse, getCharsetUsingRequest, DirectResult
from zope.publisher.browser import BrowserRequest
from zope.security.proxy import isinstance
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.publisher.interfaces.browser import IBrowserApplicationRequest
from zope.component import getUtility
from zope.publisher.browser import BrowserPage
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

import traceback, logging
DEBUG = logging.DEBUG
logger = logging.getLogger()
keyword_key = 'pythonKwMaRkEr'
json_charsets = ('utf-8', 'utf-16', 'utf-32')
writeProfileData = False
compressionTrigger = 1024
compressionLevel = 6
JSONRPCPublication = BaseHTTPPublication

class JSONRPCPublicationFactory(object):
    """a JSON-RPC Publication handler
    modeled after zope.app.publication.xmlrpc.XMLRPCPublicationFactory
    """
    __module__ = __name__

    def __init__(self, db):
        self.__pub = JSONRPCPublication(db)

    def __call__(self):
        return self.__pub


def intsort(item):
    return int(item[0])


class JSONRPCRequest(BrowserRequest):
    """a JSON-RPC Request
    modeled after zope.publisher.xmlrpc.XMLRPCRequest
    REQUEST from JSON-RPC client
    should have
    method
    params
    id
    """
    __module__ = __name__
    jsonID = 'dummy'
    form = {}
    implements(IJSONRPCRequest, IBrowserRequest, IBrowserApplicationRequest)
    _args = ()

    def _createResponse(self):
        """return a response"""
        return JSONRPCResponse()

    def processInputs(self):
        """take the converted request and make useful args of it"""
        json = getUtility(IJSONReader)
        stream = self._body_instream
        input = []
        incoming = stream.read(1000)
        while incoming:
            input.append(incoming)
            incoming = stream.read(1000)

        input = ('').join(input)
        input = self._decode(input)
        data = json.read(input)
        if writeProfileData:
            infile = 'profiledata.js'
            t = open(infile, 'a')
            t.write('%s\n' % input)
            t.close()
        logger.log(DEBUG, 'processing inputs (%s)' % data)
        functionstr = data['method']
        function = functionstr.split('.')
        self.jsonID = data['id']
        params = data['params']
        if isinstance(params, list):
            args = params
            kwargs = None
            notPositional = []
            for k in args:
                if isinstance(k, dict):
                    if k.has_key(keyword_key):
                        if isinstance(k[keyword_key], dict):
                            j = k[keyword_key]
                            kwargs = j
                            notPositional.append(k)

            if notPositional:
                for k in notPositional:
                    args.remove(k)

            if kwargs:
                for m in kwargs.keys():
                    self.form[str(m)] = kwargs[m]

        elif isinstance(params, dict):
            temp_positional = []
            for key in params:
                if key.isdigit():
                    temp_positional.append((key, params[key]))

            temp_positional.sort(key=intsort)
            args = []
            for item in temp_positional:
                args.append(item[1])
                del params[item[0]]

            for named_param in params:
                self.form[str(named_param)] = params[named_param]

        else:
            raise TypeError, 'Unsupported type for JSON-RPC "params" (%s)' % type(params)
        self._args = tuple(args)
        super(JSONRPCRequest, self).processInputs()
        self._environ['JSONRPC_MODE'] = True
        if function:
            self.setPathSuffix(function)
        return

    def traverse(self, object):
        return super(BrowserRequest, self).traverse(object)

    def __getitem__(self, key):
        return self.get(key)


class JSONRPCResponse(HTTPResponse):
    """JSON-RPC Response
    modeled after zope.publisher.xmlrpc.XMLRPCResponse
    """
    __module__ = __name__

    def setResult(self, result):
        """return
        {
        'id' : matches id in request
        'result' : the result or null if error
        'error' : the error or null if result
        }
        """
        id = self._request.jsonID
        if id is not None:
            result = premarshal(result)
            wrapper = {'id': id}
            wrapper['result'] = result
            wrapper['error'] = None
            if writeProfileData:
                outfile = 'profiledata.py'
                t = open(outfile, 'a')
                t.write('%s\n' % wrapper)
                t.close()
            json = getUtility(IJSONWriter)
            encoding = getCharsetUsingRequest(self._request)
            result = json.write(wrapper)
            body = self._prepareResult(result)
            super(JSONRPCResponse, self).setResult(body)
            logger.log(DEBUG, '%s' % result)
        else:
            self.setStatus(204)
            super(JSONRPCResponse, self).setResult('')
        return

    def _prepareResult(self, result):
        encoding = getCharsetUsingRequest(self._request) or 'utf-8'
        enc = encoding.lower()
        if enc not in json_charsets:
            encoding = 'utf-8'
        if isinstance(result, unicode):
            body = result.encode(encoding)
            charset = encoding
        else:
            raise TypeError, 'JSON did not return unicode (%s)' % type(result)
        self.setHeader('content-type', 'application/x-javascript;charset=%s' % charset)
        return body

    def handleException(self, exc_info):
        (t, value) = exc_info[:2]
        exc_data = []
        for (file, lineno, function, text) in traceback.extract_tb(exc_info[2]):
            exc_data.append('%s %s %s %s %s' % (file, 'line', lineno, 'in', function))
            exc_data.append('%s %s' % ('=>', repr(text)))
            exc_data.append('** %s: %s' % exc_info[:2])

        logger.log(logging.ERROR, ('\n').join(exc_data))
        s = '%s: %s' % (getattr(t, '__name__', t), value)
        wrapper = {'id': self._request.jsonID}
        wrapper['result'] = None
        wrapper['error'] = s
        json = getUtility(IJSONWriter)
        result = json.write(wrapper)
        body = self._prepareResult(result)
        super(JSONRPCResponse, self).setResult(body)
        logger.log(DEBUG, 'Exception: %s' % result)
        self.setStatus(200)
        return


class PreMarshallerBase(object):
    """Abstract base class for pre-marshallers."""
    __module__ = __name__
    implements(IJSONRPCPremarshaller)

    def __init__(self, data):
        self.data = data

    def __call__(self):
        raise Exception, 'Not implemented'


class DictPreMarshaller(PreMarshallerBase):
    """Pre-marshaller for dicts"""
    __module__ = __name__

    def __call__(self):
        return dict([ (premarshal(k), premarshal(v)) for (k, v) in self.data.items() ])


class ListPreMarshaller(PreMarshallerBase):
    """Pre-marshaller for list"""
    __module__ = __name__

    def __call__(self):
        return map(premarshal, self.data)


def premarshal(data):
    """Premarshal data before handing it to JSON writer for marshalling

    The initial purpose of this function is to remove security proxies
    without resorting to removeSecurityProxy.   This way, we can avoid
    inadvertently providing access to data that should be protected.
    """
    premarshaller = IJSONRPCPremarshaller(data, alternate=None)
    if premarshaller is not None:
        return premarshaller()
    return data


class JSONView(BrowserPage):
    """This is a base view class for 'ordinary' JSON methods.
    JSONViews are accessible by ordinary URLs and HTTP GETs.
    """
    __module__ = __name__
    implements(IJSONView)
    contentType = 'application/json'

    def render(self, *args, **kw):
        """return the python list or dict that will be the body of the response.
        This needs to be overridden in subclasses"""
        raise NotImplementedError('Subclasses should override render to provide a response body')

    def doCacheControl(self):
        """ at the moment, KHTML-based browsers do not handle cached JSON data
        properly.  This may be Dojo-specific, and may be only necessary for
        a short time until Konq and Safari behave like other browsers in this
        respect.
        Default here is to send 'no-cache' header to KHTML browsers.
        For other user agents, a 1-hour public cache is specified.
        
        May be overridden/extended in subclasses.
        """
        agent = self.request.get('HTTP_USER_AGENT', '')
        response = self.request.response
        if 'KHTML' in agent:
            response.setHeader('cache-control', 'no-cache')
        else:
            response.setHeader('cache-control', 'public, must-revalidate, max-age=3600')

    def __call__(self, *args, **kw):
        """the render method is called.

        First, anything that matches the method signature in request.form is 
        put in the method's **kw.

        After call, the response is JSONized and sent out with appropriate
        encoding.

        """
        request = self.request
        meth = self.render
        params = meth.im_func.func_code.co_varnames[1:]
        for key in request.form.keys():
            if key in params:
                kw[str(key)] = request.form.get(key)

        try:
            resp = premarshal(self.render(*args, **kw))
        except TypeError, err:
            request.response.setStatus('500')
            resp = {'error': '%s' % err}

        if not isinstance(resp, dict) and not isinstance(resp, list):
            raise ValueError('JSON responses must be dicts or lists')
        self.doCacheControl()
        encoding = getCharsetUsingRequest(self.request)
        enc = encoding.lower()
        if enc not in json_charsets:
            enc = 'utf-8'
        request.response.setHeader('content-type', '%s;charset=%s' % (self.contentType, enc))
        json = getUtility(IJSONWriter)
        s = json.write(resp).encode(enc)
        return s


class JSONRPCView(object):
    """A base JSON-RPC view that can be used as mix-in for JSON-RPC views.
       like zope.app.publisher.xmlrpc.XMLRPCView
    """
    __module__ = __name__
    implements(IJSONRPCView)

    def __init__(self, context, request):
        self.context = context
        self.request = request


class MethodPublisher(JSONRPCView, Location):
    """Base class for JSON-RPC views that publish methods
       like zope.app.publisher.xmlrpc.MethodPublisher
    """
    __module__ = __name__
    implements(IMethodPublisher)

    def __getParent(self):
        return hasattr(self, '_parent') and self._parent or self.context

    def __setParent(self, parent):
        self._parent = parent

    __parent__ = property(__getParent, __setParent)


class MethodTraverser(object):
    __module__ = __name__
    implements(IJSONRPCPublisher)
    __used_for__ = IMethodPublisher

    def __init__(self, context, request):
        self.context = context

    def publishTraverse(self, request, name):
        return getattr(self.context, name)


class TestRequest(JSONRPCRequest):
    """modeled after zope.publisher.xmlrpc.TestRequest"""
    __module__ = __name__

    def __init__(self, body_instream=None, environ=None, response=None, **kw):
        _testEnv = {'SERVER_URL': 'http://127.0.0.1', 'HTTP_HOST': '127.0.0.1', 'CONTENT_LENGTH': '0', 'GATEWAY_INTERFACE': 'TestFooInterface/1.0'}
        if environ:
            _testEnv.update(environ)
        if kw:
            _testEnv.update(kw)
        if body_instream is None:
            body_instream = StringIO('')
        super(TestRequest, self).__init__(body_instream, _testEnv, response)
        return