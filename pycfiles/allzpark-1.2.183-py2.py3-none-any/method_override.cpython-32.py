# uncompyle6 version 3.6.7
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/ally/http/impl/processor/method_override.py
# Compiled at: 2013-10-02 09:54:40
__doc__ = '\nCreated on Aug 9, 2011\n\n@package: ally http\n@copyright: 2012 Sourcefabric o.p.s.\n@license: http://www.gnu.org/licenses/gpl-3.0.txt\n@author: Gabriel Nistor\n\nProvides the method override header handling.\n'
from ally.container.ioc import injected
from ally.design.processor.attribute import requires, defines
from ally.design.processor.context import Context
from ally.design.processor.handler import HandlerProcessorProceed
from ally.http.spec.codes import HEADER_ERROR
from ally.http.spec.server import IDecoderHeader, HTTP_GET, HTTP_POST, HTTP_DELETE, HTTP_PUT
import logging
log = logging.getLogger(__name__)

class Request(Context):
    """
    The request context.
    """
    decoderHeader = requires(IDecoderHeader)
    method = requires(str)


class Response(Context):
    """
    The response context.
    """
    code = defines(str)
    status = defines(int)
    isSuccess = defines(bool)
    text = defines(str)


@injected
class MethodOverrideHandler(HandlerProcessorProceed):
    """
    Provides the method override processor.
    """
    nameXMethodOverride = 'X-HTTP-Method-Override'
    methodsOverride = {HTTP_GET: [
                HTTP_DELETE], 
     HTTP_POST: [
                 HTTP_PUT]}

    def __init__(self):
        assert isinstance(self.nameXMethodOverride, str), 'Invalid method override name %s' % self.nameXMethodOverride
        assert isinstance(self.methodsOverride, dict), 'Invalid methods override %s' % self.methodsOverride
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
        assert isinstance(request.decoderHeader, IDecoderHeader), 'Invalid header decoder %s' % request.decoderHeader
        value = request.decoderHeader.retrieve(self.nameXMethodOverride)
        if value:
            allowed = self.methodsOverride.get(request.method)
            if not allowed:
                response.code, response.status, response.isSuccess = HEADER_ERROR
                response.text = "Cannot override method '%s'" % request.method
                return
            else:
                value = value.upper()
                if value not in allowed:
                    pass
                response.code, response.status, response.isSuccess = HEADER_ERROR
                response.text = "Cannot override method '%s' to method '%s'" % (request.method, value)
                return
            if not log.debug('Successfully overridden method %s with %s', request.method, value):
                assert True
                request.method = value