# uncompyle6 version 3.6.7
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/ally/core/http/impl/processor/uri.py
# Compiled at: 2013-10-02 09:54:40
__doc__ = '\nCreated on Jun 28, 2011\n\n@package: ally core http\n@copyright: 2012 Sourcefabric o.p.s.\n@license: http://www.gnu.org/licenses/gpl-3.0.txt\n@author: Gabriel Nistor\n\nProvides the URI request path handler.\n'
from ally.api.type import Scheme, Type
from ally.container.ioc import injected
from ally.core.spec.resources import ConverterPath, Path, Converter, Normalizer, Node
from ally.design.processor.attribute import requires, defines, optional
from ally.design.processor.context import Context
from ally.design.processor.handler import HandlerProcessorProceed
from ally.http.spec.codes import PATH_FOUND, PATH_NOT_FOUND
from ally.support.core.util_resources import findPath
from urllib.parse import unquote
import logging
from ally.core.impl.node import NodeProperty
log = logging.getLogger(__name__)

class Request(Context):
    """
    The request context.
    """
    uri = requires(str)
    argumentsOfType = optional(dict)
    extension = defines(str, doc='\n    @rtype: string\n    The extension of the requested URI.\n    ')
    path = defines(Path, doc='\n    @rtype: Path\n    The path to the resource node.\n    ')
    converterId = defines(Converter, doc="\n    @rtype: Converter\n    The converter to use for model id's.\n    ")
    normalizerParameters = defines(Normalizer, doc='\n    @rtype: Normalizer\n    The normalizer to use for decoding parameters names.\n    ')
    converterParameters = defines(Converter, doc='\n    @rtype: Converter\n    The converter to use for the parameters values.\n    ')


class Response(Context):
    """
    The response context.
    """
    code = defines(str)
    status = defines(int)
    isSuccess = defines(bool)
    text = defines(str)
    converterId = defines(Converter, doc="\n    @rtype: Converter\n    The converter to use for model id's.\n    ")


class ResponseContent(Context):
    """
    The response content context.
    """
    type = defines(str, doc='\n    @rtype: string\n    The response content type.\n    ')


@injected
class URIHandler(HandlerProcessorProceed):
    """
    Implementation for a processor that provides the searches based on the request URL the resource path, also
    populates the parameters and extension format on the request.
    """
    resourcesRoot = Node
    converterPath = ConverterPath

    def __init__(self):
        assert isinstance(self.resourcesRoot, Node), 'Invalid resources node %s' % self.resourcesRoot
        assert isinstance(self.converterPath, ConverterPath), 'Invalid ConverterPath object %s' % self.converterPath
        super().__init__()

    def process(self, request: Request, response: Response, responseCnt: ResponseContent, **keyargs):
        """
        @see: HandlerProcessorProceed.process
        
        Process the URI to a resource path.
        """
        assert isinstance(request, Request), 'Invalid required request %s' % request
        assert isinstance(response, Response), 'Invalid response %s' % response
        assert isinstance(responseCnt, ResponseContent), 'Invalid response content %s' % responseCnt
        assert isinstance(request.uri, str), 'Invalid request URI %s' % request.uri
        if response.isSuccess is False:
            return
        paths = request.uri.split('/')
        i = paths[(-1)].rfind('.') if len(paths) > 0 else -1
        if i < 0:
            clearExtension = True
            request.extension = None
        else:
            clearExtension = i == 0
            request.extension = paths[(-1)][i + 1:].lower()
            paths[-1] = paths[(-1)][0:i]
        paths = [unquote(p) for p in paths if p]
        if request.extension:
            responseCnt.type = request.extension
        request.path = findPath(self.resourcesRoot, paths, self.converterPath)
        assert isinstance(request.path, Path), 'Invalid path %s' % request.path
        node = request.path.node
        if not node:
            response.code, response.status, response.isSuccess = PATH_NOT_FOUND
            if not log.debug('No resource found for URI %s', request.uri):
                assert True
            return
        else:
            if not clearExtension:
                if isinstance(node, NodeProperty):
                    assert isinstance(node, NodeProperty)
                    assert isinstance(node.type, Type)
                    if node.type.isOf(str):
                        response.code, response.status, response.isSuccess = PATH_NOT_FOUND
                        response.text = 'Missing trailing slash'
                        if not log.debug('Unclear extension for URI %s', request.uri):
                            assert True
                            return
            if not log.debug('Found resource for URI %s', request.uri):
                assert True
            request.converterId = self.converterPath
            request.converterParameters = self.converterPath
            request.normalizerParameters = self.converterPath
            if Request.argumentsOfType in request and request.argumentsOfType is not None:
                request.argumentsOfType[Scheme] = request.scheme
            response.code, response.status, response.isSuccess = PATH_FOUND
            response.converterId = self.converterPath
            return