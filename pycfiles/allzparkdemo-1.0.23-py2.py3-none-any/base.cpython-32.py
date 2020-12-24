# uncompyle6 version 3.6.7
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/ally/core/impl/processor/render/base.py
# Compiled at: 2013-10-02 09:54:40
__doc__ = '\nCreated on Jan 25, 2012\n\n@package: ally core\n@copyright: 2011 Sourcefabric o.p.s.\n@license: http://www.gnu.org/licenses/gpl-3.0.txt\n@author: Gabriel Nistor\n\nProvides the text base encoder processor handler.\n'
from ally.container.ioc import injected
from ally.design.processor.attribute import requires, defines
from ally.design.processor.context import Context
from ally.design.processor.execution import Chain
from ally.design.processor.handler import HandlerProcessor
from collections import Callable
from functools import partial
import abc, logging
log = logging.getLogger(__name__)

class Response(Context):
    """
    The response context.
    """
    renderFactory = defines(Callable, doc='\n    @rtype: callable(IOutputStream) -> IRender\n    The renderer factory to be used for the response.\n    ')


class ResponseContent(Context):
    """
    The response content context.
    """
    type = requires(str)
    charSet = requires(str)


@injected
class RenderBaseHandler(HandlerProcessor):
    """
    Provides the text base renderer.
    """
    contentTypes = dict

    def __init__(self):
        assert isinstance(self.contentTypes, dict), 'Invalid content types %s' % self.contentTypes
        super().__init__()

    def process(self, chain, response: Response, responseCnt: ResponseContent, **keyargs):
        """
        @see: HandlerProcessor.process
        
        Encode the ressponse object.
        """
        assert isinstance(chain, Chain), 'Invalid processors chain %s' % chain
        assert isinstance(response, Response), 'Invalid response %s' % response
        assert isinstance(responseCnt, ResponseContent), 'Invalid response content %s' % responseCnt
        if responseCnt.type not in self.contentTypes:
            if not log.debug("The content type '%s' is not for this %s encoder", responseCnt.type, self):
                assert True
        else:
            contentType = self.contentTypes[responseCnt.type]
            if contentType:
                if not log.debug("Normalized content type '%s' to '%s'", responseCnt.type, contentType):
                    assert True
                    responseCnt.type = contentType
                response.renderFactory = partial(self.renderFactory, responseCnt.charSet)
                return
        chain.proceed()

    @abc.abstractclassmethod
    def renderFactory(self, charSet, output):
        """
        Factory method used for creating a renderer.
        
        @param charSet: string
            The character set to be used by the created factory.
        @param output: IOutputStream
            The output stream to be used by the renderer.
        @return: IRender
            The renderer.
        """
        pass