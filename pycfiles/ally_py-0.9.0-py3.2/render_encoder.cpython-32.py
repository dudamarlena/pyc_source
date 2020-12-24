# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ally/core/impl/processor/render_encoder.py
# Compiled at: 2013-10-02 09:54:40
"""
Created on Jul 27, 2012

@package: ally core
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Renders the response encoder.
"""
from ally.container.ioc import injected
from ally.core.spec.transform.exploit import Resolve
from ally.core.spec.transform.render import IRender
from ally.design.processor.attribute import requires, defines
from ally.design.processor.context import Context
from ally.design.processor.handler import HandlerProcessorProceed
from collections import Callable, Iterable
from io import BytesIO
import logging
log = logging.getLogger(__name__)

class Response(Context):
    """
    The response context.
    """
    renderFactory = requires(Callable)
    encoder = requires(Callable)
    encoderData = requires(dict)
    obj = requires(object)
    isSuccess = requires(bool)


class ResponseContent(Context):
    """
    The response content context.
    """
    source = defines(Iterable, doc='\n    @rtype: Iterable\n    The generator containing the response content.\n    ')
    length = defines(int)


@injected
class RenderEncoderHandler(HandlerProcessorProceed):
    """
    Implementation for a handler that renders the response content encoder.
    """
    allowChunked = False
    bufferSize = 1024

    def __init__(self):
        assert isinstance(self.allowChunked, bool), 'Invalid allow chuncked flag %s' % self.allowChunked
        assert isinstance(self.bufferSize, int), 'Invalid buffer size %s' % self.bufferSize
        super().__init__()

    def process(self, response: Response, responseCnt: ResponseContent, **keyargs):
        """
        @see: HandlerProcessorProceed.process
        
        Process the encoder rendering.
        """
        assert isinstance(response, Response), 'Invalid response %s' % response
        assert isinstance(responseCnt, ResponseContent), 'Invalid response content %s' % responseCnt
        if response.isSuccess is False:
            return
        else:
            if response.encoder is None:
                return
            assert callable(response.renderFactory), 'Invalid response renderer factory %s' % response.renderFactory
            output = BytesIO()
            render = response.renderFactory(output)
            assert isinstance(render, IRender), 'Invalid render %s' % render
            resolve = Resolve(response.encoder).request(value=response.obj, render=render, **(response.encoderData or {}))
            if not self.allowChunked and responseCnt.length is None:
                while resolve.has():
                    resolve.do()

                content = output.getvalue()
                responseCnt.length = len(content)
                responseCnt.source = (content,)
                output.close()
            else:
                responseCnt.source = self.renderAsGenerator(resolve, output, self.bufferSize)
            return

    def renderAsGenerator(self, resolve, output, bufferSize):
        """
        Create a generator for rendering the encoder.
        """
        while resolve.has():
            if output.tell() >= bufferSize:
                yield output.getvalue()
                output.seek(0)
                output.truncate()
            resolve.do()

        yield output.getvalue()
        output.close()