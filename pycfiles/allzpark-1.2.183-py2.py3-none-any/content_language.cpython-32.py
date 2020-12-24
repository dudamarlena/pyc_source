# uncompyle6 version 3.6.7
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/ally/core/http/impl/processor/headers/content_language.py
# Compiled at: 2013-10-02 09:54:40
__doc__ = '\nCreated on Jun 12, 2012\n\n@package: ally core http\n@copyright: 2012 Sourcefabric o.p.s.\n@license: http://www.gnu.org/licenses/gpl-3.0.txt\n@author: Gabriel Nistor\n\nProvides the content language header decoding.\n'
from ally.api.type import Locale
from ally.container.ioc import injected
from ally.design.processor.attribute import requires, defines, optional
from ally.design.processor.context import Context
from ally.design.processor.handler import HandlerProcessorProceed
from ally.http.spec.server import IDecoderHeader, IEncoderHeader

class RequestDecode(Context):
    """
    The request context.
    """
    decoderHeader = requires(IDecoderHeader)
    argumentsOfType = optional(dict)
    language = defines(str, doc='\n    @rtype: string\n    The language for the content.\n    ')


@injected
class ContentLanguageDecodeHandler(HandlerProcessorProceed):
    """
    Implementation for a processor that provides the decoding of content language HTTP request header.
    """
    nameContentLanguage = 'Content-Language'

    def __init__(self):
        assert isinstance(self.nameContentLanguage, str), 'Invalid content language name %s' % self.nameContentLanguage
        super().__init__()

    def process(self, request: RequestDecode, **keyargs):
        """
        @see: HandlerProcessorProceed.process
        
        Provides the content language decode for the request.
        """
        assert isinstance(request, RequestDecode), 'Invalid request %s' % request
        assert isinstance(request.decoderHeader, IDecoderHeader), 'Invalid header decoder %s' % request.decoderHeader
        value = request.decoderHeader.retrieve(self.nameContentLanguage)
        if value:
            request.language = value
            if RequestDecode.argumentsOfType in request and request.argumentsOfType is not None:
                request.argumentsOfType[Locale] = request.language
        return


class ResponseEncode(Context):
    """
    The response context.
    """
    encoderHeader = requires(IEncoderHeader)
    language = requires(str)


@injected
class ContentLanguageEncodeHandler(HandlerProcessorProceed):
    """
    Implementation for a processor that provides the encoding of content language HTTP request header.
    """
    nameContentLanguage = 'Content-Language'

    def __init__(self):
        assert isinstance(self.nameContentLanguage, str), 'Invalid content language name %s' % self.nameContentLanguage
        super().__init__()

    def process(self, response: ResponseEncode, **keyargs):
        """
        @see: HandlerProcessorProceed.process
        
        Encodes the content language.
        """
        assert isinstance(response, ResponseEncode), 'Invalid response %s' % response
        assert isinstance(response.encoderHeader, IEncoderHeader), 'Invalid response header encoder %s' % response.encoderHeader
        if response.language:
            response.encoderHeader.encode(self.nameContentLanguage, response.language)