# uncompyle6 version 3.6.7
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/ally/gateway/http/impl/processor/selector.py
# Compiled at: 2013-10-02 09:54:40
__doc__ = '\nCreated on Feb 8, 2013\n\n@package: gateway service\n@copyright: 2011 Sourcefabric o.p.s.\n@license: http://www.gnu.org/licenses/gpl-3.0.txt\n@author: Gabriel Nistor\n\nProvides the gateway repository selector processor.\n'
from ally.container.ioc import injected
from ally.design.processor.attribute import requires, defines
from ally.design.processor.context import Context
from ally.design.processor.handler import HandlerProcessorProceed
from ally.gateway.http.spec.gateway import IRepository
from ally.http.spec.codes import PATH_NOT_FOUND, METHOD_NOT_AVAILABLE

class Request(Context):
    """
    The request context.
    """
    method = requires(str)
    headers = requires(dict)
    uri = requires(str)
    repository = requires(IRepository)
    match = defines(Context)


class Response(Context):
    """
    Context for response. 
    """
    code = defines(str)
    status = defines(int)
    isSuccess = defines(bool)
    allows = defines(list)


@injected
class GatewaySelectorHandler(HandlerProcessorProceed):
    """
    Implementation for a handler that provides the gateway repository selector. This handler will pick the appropriate gateway
    for processing.
    """

    def process(self, request: Request, response: Response, **keyargs):
        """
        @see: HandlerProcessorProceed.process
        
        Provides the gateway selection.
        """
        assert isinstance(request, Request), 'Invalid request %s' % request
        assert isinstance(response, Response), 'Invalid response %s' % response
        if response.isSuccess is False:
            return
        else:
            assert isinstance(request.repository, IRepository), 'Invalid request repository %s' % request.repository
            request.match = request.repository.find(request.method, request.headers, request.uri)
            if not request.match:
                allows = request.repository.allowsFor(request.headers, request.uri)
                if allows:
                    response.code, response.status, response.isSuccess = METHOD_NOT_AVAILABLE
                    if response.allows is None:
                        response.allows = list(allows)
                    else:
                        response.allows.extend(allows)
                    request.match = request.repository.find(request.method, request.headers, request.uri, METHOD_NOT_AVAILABLE.status)
                else:
                    response.code, response.status, response.isSuccess = PATH_NOT_FOUND
                request.match = request.repository.find(request.method, request.headers, request.uri, PATH_NOT_FOUND.status)
            return