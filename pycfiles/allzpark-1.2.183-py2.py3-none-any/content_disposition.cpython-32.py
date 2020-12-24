# uncompyle6 version 3.6.7
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/ally/core/http/impl/processor/headers/content_disposition.py
# Compiled at: 2013-10-02 09:54:40
__doc__ = '\nCreated on Jun 11, 2012\n\n@package: ally core http\n@copyright: 2012 Sourcefabric o.p.s.\n@license: http://www.gnu.org/licenses/gpl-3.0.txt\n@author: Gabriel Nistor\n\nProvides the content disposition header decoding.\n'
from ally.container.ioc import injected
from ally.design.processor.attribute import requires, defines
from ally.design.processor.context import Context
from ally.design.processor.handler import HandlerProcessorProceed
from ally.http.spec.codes import HEADER_ERROR
from ally.http.spec.server import IDecoderHeader

class Request(Context):
    """
    The request context.
    """
    decoderHeader = requires(IDecoderHeader)


class RequestContent(Context):
    """
    The request content context.
    """
    name = defines(str, doc='\n    @rtype: string\n    The content name.\n    ')
    disposition = defines(str, doc='\n    @rtype: string\n    The content disposition.\n    ')
    dispositionAttr = defines(dict, doc='\n    @rtype: dictionary{string, string}\n    The content disposition attributes.\n    ')


class Response(Context):
    """
    The response context.
    """
    code = defines(str)
    status = defines(int)
    isSuccess = defines(bool)
    text = defines(str)
    errorMessage = defines(str)


@injected
class ContentDispositionDecodeHandler(HandlerProcessorProceed):
    """
    Implementation for a processor that provides the decoding of content disposition HTTP request header.
    """
    uploadFilename = 'filename'
    nameContentDisposition = 'Content-Disposition'

    def __init__(self):
        assert isinstance(self.uploadFilename, str), 'Invalid upload file name %s' % self.uploadFilename
        assert isinstance(self.nameContentDisposition, str), 'Invalid content disposition header name %s' % self.nameContentDisposition
        super().__init__()

    def process(self, request: Request, requestCnt: RequestContent, response: Response, **keyargs):
        """
        @see: HandlerProcessorProceed.process

        Provides the content type decode for the request.
        """
        assert isinstance(request, Request), 'Invalid request %s' % request
        assert isinstance(requestCnt, RequestContent), 'Invalid request content %s' % requestCnt
        assert isinstance(response, Response), 'Invalid response %s' % response
        assert isinstance(request.decoderHeader, IDecoderHeader), 'Invalid header decoder %s' % request.decoderHeader
        value = request.decoderHeader.decode(self.nameContentDisposition)
        if value:
            if len(value) > 1:
                if response.isSuccess is False:
                    return
                else:
                    response.code, response.status, response.isSuccess = HEADER_ERROR
                    response.text = "Invalid '%s'" % self.nameContentDisposition
                    response.errorMessage = "Invalid value '%s' for header '%s', expected only one value entry" % (
                     value, self.nameContentDisposition)
                    return
                value, attributes = value[0]
                requestCnt.disposition = value
                requestCnt.dispositionAttr = attributes
                if self.uploadFilename in attributes:
                    requestCnt.name = attributes[self.uploadFilename]