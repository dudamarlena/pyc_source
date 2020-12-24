# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ally/http/impl/processor/headers/allow.py
# Compiled at: 2013-10-02 09:54:40
"""
Created on Jun 11, 2012

@package: ally http
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the allow headers handling.
"""
from ally.container.ioc import injected
from ally.design.processor.attribute import requires
from ally.design.processor.context import Context
from ally.design.processor.handler import HandlerProcessorProceed
from ally.http.spec.codes import METHOD_NOT_AVAILABLE
from ally.http.spec.server import IEncoderHeader

class Response(Context):
    """
    The response context.
    """
    status = requires(int)
    allows = requires(list)
    encoderHeader = requires(IEncoderHeader)


@injected
class AllowEncodeHandler(HandlerProcessorProceed):
    """
    Implementation for a processor that provides the encoding of allow HTTP request headers.
    """
    nameAllow = 'Allow'

    def __init__(self):
        assert isinstance(self.nameAllow, str), 'Invalid allow name %s' % self.nameAllow
        super().__init__()

    def process(self, response: Response, **keyargs):
        """
        @see: HandlerProcessorProceed.process
        
        Encode the allow headers.
        """
        assert isinstance(response, Response), 'Invalid response %s' % response
        assert isinstance(response.encoderHeader, IEncoderHeader), 'Invalid response header encoder %s' % response.encoderHeader
        if METHOD_NOT_AVAILABLE.status == response.status and response.allows:
            response.encoderHeader.encode(self.nameAllow, *response.allows)