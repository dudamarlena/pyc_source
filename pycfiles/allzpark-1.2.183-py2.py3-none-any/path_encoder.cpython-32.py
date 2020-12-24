# uncompyle6 version 3.6.7
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/ally/http/impl/processor/path_encoder.py
# Compiled at: 2013-10-02 09:54:40
__doc__ = '\nCreated on Jan 31, 2013\n\n@package: ally http\n@copyright: 2012 Sourcefabric o.p.s.\n@license: http://www.gnu.org/licenses/gpl-3.0.txt\n@author: Gabriel Nistor\n\nProvides the path encoder.\n'
from ally.container.ioc import injected
from ally.design.processor.attribute import requires, defines
from ally.design.processor.context import Context
from ally.design.processor.handler import HandlerProcessorProceed
from ally.http.spec.server import IDecoderHeader, IEncoderPath
from ally.support.util import Singletone
from collections import Iterable
from urllib.parse import urlsplit, urlunsplit, urlencode
import logging
log = logging.getLogger(__name__)

class Request(Context):
    """
    The request context.
    """
    scheme = requires(str)
    decoderHeader = requires(IDecoderHeader)


class Response(Context):
    """
    The response context.
    """
    code = defines(str)
    status = defines(int)
    isSuccess = defines(bool)
    encoderPath = defines(IEncoderPath, doc='\n    @rtype: IEncoderPath\n    The path encoder used for encoding paths that will be rendered in the response.\n    ')


@injected
class EncoderPathHandler(HandlerProcessorProceed):
    """
    Provides the path encoder for the response.
    """
    headerHost = 'Host'

    def __init__(self):
        assert isinstance(self.headerHost, str), 'Invalid string %s' % self.headerHost
        super().__init__()

    def process(self, request: Request, response: Response, **keyargs):
        """
        @see: HandlerProcessorProceed.process
        
        Overrides the request method based on a provided header.
        """
        assert isinstance(request, Request), 'Invalid request %s' % request
        assert isinstance(response, Response), 'Invalid response %s' % response
        if response.isSuccess is False:
            return
        else:
            assert isinstance(request.decoderHeader, IDecoderHeader), 'Invalid header decoder %s' % request.decoderHeader
            host = request.decoderHeader.retrieve(self.headerHost)
            if host is None:
                response.encoderPath = EncoderPathNothing()
                if not log.debug('No host header available for URI %s', request.uri):
                    assert True
                    return
            response.encoderPath = EncoderPathHost(request.scheme, host)
            return


class EncoderPathNothing(Singletone, IEncoderPath):
    """
    Provides no encoding for URIs.
    """
    __slots__ = ()

    def encode(self, path, parameters=None):
        """
        @see: IEncoderPath.encode
        """
        assert isinstance(path, str), 'Invalid path %s' % path
        url = urlsplit(path)
        assert not url.query, "No query expected for path '%s'" % path
        assert not url.fragment, "No fragment expected for path '%s'" % path
        if parameters:
            assert isinstance(parameters, Iterable), 'Invalid parameters %s' % parameters
            if not isinstance(parameters, list):
                parameters = list(parameters)
            for name, value in parameters:
                assert isinstance(name, str), 'Invalid parameter name %s' % name
                if not isinstance(value, str):
                    raise AssertionError('Invalid parameter value %s' % value)

            parameters = urlencode(parameters)
        else:
            parameters = ''
        return urlunsplit((url.scheme, url.netloc, url.path, parameters, ''))

    def encodePattern(self, path):
        """
        @see: IEncoderPath.encodePattern
        """
        raise NotImplementedError('Not need to implement, at least until now')


class EncoderPathHost(IEncoderPath):
    """
    Provides encoding host prefixing for the URI paths to be encoded in the response.
    """
    __slots__ = ('_scheme', '_host')

    def __init__(self, scheme, host):
        """
        Construct the encoder.
        
        @param scheme: string
            The encoded path scheme.
        @param host: string
            The host string.
        """
        assert isinstance(scheme, str), 'Invalid scheme %s' % scheme
        assert isinstance(host, str), 'Invalid host %s' % host
        self._scheme = scheme
        self._host = host

    def encode(self, path, parameters=None):
        """
        @see: IEncoderPath.encode
        
        @param parameters: Iterable(tuple(string, string))
            A iterable of tuples containing on the first position the parameter string name and on the second the string
            parameter value as to be represented in the request path.
        """
        assert isinstance(path, str), 'Invalid path %s' % path
        url = urlsplit(path)
        assert not url.query, "No query expected for path '%s'" % path
        assert not url.fragment, "No fragment expected for path '%s'" % path
        if parameters:
            assert isinstance(parameters, Iterable), 'Invalid parameters %s' % parameters
            if not isinstance(parameters, list):
                parameters = list(parameters)
            for name, value in parameters:
                assert isinstance(name, str), 'Invalid parameter name %s' % name
                if not isinstance(value, str):
                    raise AssertionError('Invalid parameter value %s' % value)

            parameters = urlencode(parameters)
        else:
            parameters = ''
        if url.scheme or url.netloc:
            return urlunsplit((url.scheme, url.netloc, url.path, parameters, ''))
        return urlunsplit((self._scheme, self._host, url.path, parameters, ''))

    def encodePattern(self, path):
        """
        @see: IEncoderPath.encodePattern
        """
        raise NotImplementedError('Not need to implement, at least until now')