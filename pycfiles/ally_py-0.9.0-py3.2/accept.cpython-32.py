# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ally/http/impl/processor/headers/accept.py
# Compiled at: 2013-10-02 09:54:40
"""
Created on Jun 11, 2012

@package: ally core http
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the accept headers handling.
"""
from ally.container.ioc import injected
from ally.design.processor.attribute import requires, defines
from ally.design.processor.context import Context
from ally.design.processor.handler import HandlerProcessorProceed
from ally.http.spec.server import IDecoderHeader, IEncoderHeader

class AcceptConfigurations:
    """
    Configurations for accept HTTP request headers.
    """
    nameAccept = 'Accept'
    nameAcceptCharset = 'Accept-Charset'

    def __init__(self):
        assert isinstance(self.nameAccept, str), 'Invalid accept name %s' % self.nameAccept
        assert isinstance(self.nameAcceptCharset, str), 'Invalid accept charset name %s' % self.nameAcceptCharset


class RequestDecode(Context):
    """
    The request decode context.
    """
    decoderHeader = requires(IDecoderHeader)
    accTypes = defines(list, doc='\n    @rtype: list[string]\n    The content types accepted for response.\n    ')
    accCharSets = defines(list, doc='\n    @rtype: list[string]\n    The character sets accepted for response.\n    ')


@injected
class AcceptRequestDecodeHandler(HandlerProcessorProceed, AcceptConfigurations):
    """
    Implementation for a processor that provides the decoding of accept HTTP request headers.
    """

    def __init__(self):
        HandlerProcessorProceed.__init__(self)
        AcceptConfigurations.__init__(self)

    def process(self, request: RequestDecode, **keyargs):
        """
        @see: HandlerProcessorProceed.process
        
        Decode the accepted headers.
        """
        assert isinstance(request, RequestDecode), 'Invalid request %s' % request
        assert isinstance(request.decoderHeader, IDecoderHeader), 'Invalid decoder header %s' % request.decoderHeader
        value = request.decoderHeader.decode(self.nameAccept)
        if value:
            request.accTypes = list(val for val, _attr in value)
        value = request.decoderHeader.decode(self.nameAcceptCharset)
        if value:
            request.accCharSets = list(val for val, _attr in value)


class RequestEncode(Context):
    """
    The request context.
    """
    encoderHeader = requires(IEncoderHeader)
    accTypes = requires(list, doc='\n    @rtype: list[string]\n    The content types accepted for response.\n    ')
    accCharSets = requires(list, doc='\n    @rtype: list[string]\n    The character sets accepted for response.\n    ')


@injected
class AcceptRequestEncodeHandler(HandlerProcessorProceed, AcceptConfigurations):
    """
    Implementation for a processor that provides the encoding of accept HTTP request headers.
    """

    def __init__(self):
        HandlerProcessorProceed.__init__(self)
        AcceptConfigurations.__init__(self)

    def process(self, request: RequestEncode, **keyargs):
        """
        @see: HandlerProcessorProceed.process
        
        Encode the accepted headers.
        """
        assert isinstance(request, RequestEncode), 'Invalid request %s' % request
        assert isinstance(request.encoderHeader, IEncoderHeader), 'Invalid encoder header %s' % request.encoderHeader
        if RequestEncode.accTypes:
            request.encoderHeader.encode(self.nameAccept, *request.accTypes)
        if RequestEncode.accCharSets:
            request.encoderHeader.encode(self.nameAcceptCharset, *request.accCharSets)