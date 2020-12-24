# uncompyle6 version 3.6.7
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/ally/http/impl/processor/method_deliver_ok.py
# Compiled at: 2013-10-02 09:54:40
__doc__ = '\nCreated on Nov 23, 2011\n\n@package: ally http\n@copyright: 2011 Sourcefabric o.p.s.\n@license: http://www.gnu.org/licenses/gpl-3.0.txt\n@author: Gabriel Nistor\n\nProvides a processor that just sends an ok status as a response without any body. This is useful for the OPTIONS\nmethod for instance where we just want to deliver some response headers. \n'
from ally.container.ioc import injected
from ally.design.processor.attribute import requires, defines
from ally.design.processor.context import Context
from ally.design.processor.execution import Chain
from ally.design.processor.handler import HandlerProcessor
from ally.http.spec.codes import PATH_FOUND

class Request(Context):
    """
    The request context.
    """
    method = requires(str)


class Response(Context):
    """
    The response context.
    """
    code = defines(str)
    status = defines(int)
    isSuccess = defines(bool)
    allows = defines(list)


@injected
class DeliverOkForMethodHandler(HandlerProcessor):
    """
    Handler that just sends an ok status.
    """
    forMethod = str

    def __init__(self):
        assert isinstance(self.forMethod, str), 'Invalid for method %s' % self.forMethod
        super().__init__()

    def process(self, chain, request: Request, response: Response, **keyargs):
        """
        @see: HandlerProcessor.process
        
        Delivers Ok if the request methos is the expected one.
        """
        assert isinstance(chain, Chain), 'Invalid processors chain %s' % chain
        assert isinstance(request, Request), 'Invalid request %s' % request
        assert isinstance(response, Response), 'Invalid response %s' % response
        if request.method == self.forMethod:
            response.code, response.status, response.isSuccess = PATH_FOUND
            return
        else:
            if response.allows is not None:
                response.allows.append(self.forMethod)
            else:
                response.allows = [
                 self.forMethod]
            chain.proceed()
            return