# uncompyle6 version 3.6.7
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/ally/http/impl/processor/deliver_code.py
# Compiled at: 2013-10-02 09:54:40
__doc__ = '\nCreated on Feb 4, 2013\n\n@package: ally http\n@copyright: 2012 Sourcefabric o.p.s.\n@license: http://www.gnu.org/licenses/gpl-3.0.txt\n@author: Gabriel Nistor\n\nPopulates a provided code for the response.\n'
from ally.container.ioc import injected
from ally.design.processor.attribute import defines
from ally.design.processor.context import Context
from ally.design.processor.handler import HandlerProcessorProceed

class Response(Context):
    """
    The response context.
    """
    code = defines(str)
    status = defines(int)
    isSuccess = defines(bool)


@injected
class DeliverCodeHandler(HandlerProcessorProceed):
    """
    Handler that just populates a code on the response and then proceeds.
    """
    code = str
    status = int
    isSuccess = bool

    def __init__(self):
        assert isinstance(self.code, str), 'Invalid code %s' % self.code
        assert isinstance(self.status, int), 'Invalid status %s' % self.status
        assert isinstance(self.isSuccess, bool), 'Invalid success flag %s' % self.isSuccess
        super().__init__()

    def process(self, response: Response, **keyargs):
        """
        @see: HandlerProcessorProceed.process
        
        Delivers the code.
        """
        assert isinstance(response, Response), 'Invalid response %s' % response
        response.code, response.status, response.isSuccess = self.code, self.status, self.isSuccess