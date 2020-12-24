# uncompyle6 version 3.6.7
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/ally/gateway/http/impl/processor/place_error.py
# Compiled at: 2013-10-02 09:54:40
__doc__ = '\nCreated on Feb 8, 2013\n\n@package: gateway service\n@copyright: 2011 Sourcefabric o.p.s.\n@license: http://www.gnu.org/licenses/gpl-3.0.txt\n@author: Gabriel Nistor\n\nProvides the gateway error parameters populating.\n'
from ally.container.ioc import injected
from ally.design.processor.attribute import requires, defines
from ally.design.processor.context import Context
from ally.design.processor.handler import HandlerProcessorProceed
from ally.http.spec.codes import METHOD_NOT_AVAILABLE
import logging
log = logging.getLogger(__name__)

class Request(Context):
    """
    The request context.
    """
    parameters = defines(list)


class Response(Context):
    """
    Context for response. 
    """
    status = requires(int)
    isSuccess = requires(bool)
    allows = requires(list)


@injected
class GatewayErrorHandler(HandlerProcessorProceed):
    """
    Implementation for a handler that populates the gateway error parameters.
    """
    nameStatus = 'status'
    nameAllow = 'allow'

    def __init__(self):
        assert isinstance(self.nameStatus, str), 'Invalid status name %s' % self.nameStatus
        assert isinstance(self.nameAllow, str), 'Invalid allow name %s' % self.nameAllow
        super().__init__()

    def process(self, request: Request, response: Response, **keyargs):
        """
        @see: HandlerProcessorProceed.process
        
        Places the error.
        """
        assert isinstance(request, Request), 'Invalid request %s' % request
        assert isinstance(response, Response), 'Invalid response %s' % response
        if response.isSuccess is not False:
            return
        else:
            assert isinstance(response.status, int), 'Invalid response status %s' % response.status
            if request.parameters is None:
                request.parameters = []
            request.parameters.insert(0, (self.nameStatus, response.status))
            if response.status == METHOD_NOT_AVAILABLE.status and response.allows is not None:
                for allow in response.allows:
                    request.parameters.append((self.nameAllow, allow))

            return