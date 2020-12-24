# uncompyle6 version 3.6.7
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/ally/core/impl/processor/rendering.py
# Compiled at: 2013-10-02 09:54:40
__doc__ = '\nCreated on Jul 12, 2011\n\n@package: ally core\n@copyright: 2011 Sourcefabric o.p.s.\n@license: http://www.gnu.org/licenses/gpl-3.0.txt\n@author: Gabriel Nistor\n\nProvides the rendering processing.\n'
from ally.container.ioc import injected
from ally.core.spec.codes import ENCODING_UNKNOWN
from ally.design.processor.assembly import Assembly
from ally.design.processor.attribute import defines, optional
from ally.design.processor.context import Context
from ally.design.processor.execution import Chain, Processing
from ally.design.processor.handler import HandlerBranchingProceed
from ally.design.processor.processor import Included
from ally.exception import DevelError
import codecs, itertools

class Request(Context):
    """
    The request context.
    """
    accTypes = optional(list)
    accCharSets = optional(list)


class Response(Context):
    """
    The response context.
    """
    code = defines(str)
    isSuccess = defines(bool)
    text = defines(str)


class ResponseContent(Context):
    """
    The response content context.
    """
    type = defines(str, doc='\n    @rtype: string\n    The response content type.\n    ')
    charSet = defines(str, doc='\n    @rtype: string\n    The character set for the text content.\n    ')


@injected
class RenderingHandler(HandlerBranchingProceed):
    """
    Implementation for a processor that provides the support for creating the renderer. If a processor is successful
    in the render creation process it has to stop the chain execution.
    """
    contentTypeDefaults = [
     None]
    charSetDefault = str
    renderingAssembly = Assembly

    def __init__(self):
        assert isinstance(self.renderingAssembly, Assembly), 'Invalid renders assembly %s' % self.renderingAssembly
        assert isinstance(self.contentTypeDefaults, (list, tuple)), 'Invalid default content type %s' % self.contentTypeDefaults
        assert isinstance(self.charSetDefault, str), 'Invalid default character set %s' % self.charSetDefault
        super().__init__(Included(self.renderingAssembly))

    def process(self, rendering, request: Request, response: Response, responseCnt: ResponseContent, **keyargs):
        """
        @see: HandlerBranchingProceed.process
        
        Create the render for the response object.
        """
        assert isinstance(rendering, Processing), 'Invalid processing %s' % rendering
        assert isinstance(request, Request), 'Invalid request %s' % request
        assert isinstance(response, Response), 'Invalid response %s' % response
        assert isinstance(responseCnt, ResponseContent), 'Invalid response content %s' % responseCnt
        if responseCnt.charSet:
            try:
                codecs.lookup(responseCnt.charSet)
            except LookupError:
                responseCnt.charSet = None

        else:
            responseCnt.charSet = None
        if not responseCnt.charSet:
            if Request.accCharSets in request and request.accCharSets is not None:
                for charSet in request.accCharSets:
                    try:
                        codecs.lookup(charSet)
                    except LookupError:
                        continue

                    responseCnt.charSet = charSet
                    break

            if not responseCnt.charSet:
                responseCnt.charSet = self.charSetDefault
        resolved = False
        if responseCnt.type:
            renderChain = Chain(rendering)
            renderChain.process(request=request, response=response, responseCnt=responseCnt, **keyargs)
            if renderChain.doAll().isConsumed():
                if response.isSuccess is not False:
                    response.code, response.isSuccess = ENCODING_UNKNOWN
                    response.text = "Content type '%s' not supported for rendering" % responseCnt.type
            else:
                resolved = True
        if not resolved:
            if Request.accTypes in request and request.accTypes is not None:
                contentTypes = itertools.chain(request.accTypes, self.contentTypeDefaults)
            else:
                contentTypes = self.contentTypeDefaults
            for contentType in contentTypes:
                responseCnt.type = contentType
                renderChain = Chain(rendering)
                renderChain.process(request=request, response=response, responseCnt=responseCnt, **keyargs)
                if not renderChain.doAll().isConsumed():
                    break
            else:
                raise DevelError('There is no renderer available, this is more likely a setup issues since the default content types should have resolved the renderer')

        return