# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ally/core/http/impl/processor/explain_error.py
# Compiled at: 2013-10-02 09:54:40
"""
Created on Jun 28, 2011

@package: ally core http
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Mihai Balaceanu

Provides support for explaining the errors in the content of the request.
"""
from ally.container.ioc import injected
from ally.core.spec.transform.render import Object, Value, renderObject
from ally.design.processor.attribute import requires, defines, optional
from ally.design.processor.context import Context
from ally.design.processor.handler import HandlerProcessorProceed
from collections import Iterable, Callable
from io import BytesIO
import logging
log = logging.getLogger(__name__)

class Response(Context):
    """
    The response context.
    """
    text = optional(str)
    errorMessage = optional(str, doc='\n    @rtype: object\n    The error message for the code.\n    ')
    errorDetails = optional(Object, doc='\n    @rtype: Object\n    The error text object describing a detailed situation for the error.\n    ')
    status = requires(int)
    code = requires(str)
    isSuccess = requires(bool)
    renderFactory = requires(Callable)


class ResponseContent(Context):
    """
    The response content context.
    """
    source = defines(Iterable)
    length = defines(int)


@injected
class ExplainErrorHandler(HandlerProcessorProceed):
    """
    Implementation for a processor that provides on the response a form of the error that can be extracted from 
    the response code and error message, this processor uses the code status (success) in order to trigger the error
    response.
    """

    def process(self, response: Response, responseCnt: ResponseContent, **keyargs):
        """
        @see: HandlerProcessorProceed.process
        
        Process the error into a response content.
        """
        assert isinstance(response, Response), 'Invalid response %s' % response
        assert isinstance(responseCnt, ResponseContent), 'Invalid response content %s' % responseCnt
        if response.isSuccess is False and response.renderFactory is not None:
            errors = [
             Value('code', str(response.status))]
            if Response.errorMessage in response and response.errorMessage:
                errors.append(Value('message', response.errorMessage))
            else:
                if Response.text in response and response.text:
                    errors.append(Value('message', response.text))
                else:
                    errors.append(Value('message', response.code))
                if Response.errorDetails in response and response.errorDetails:
                    errors.append(Object('details', response.errorDetails))
            output = BytesIO()
            render = response.renderFactory(output)
            renderObject(Object('error', *errors), render)
            content = output.getvalue()
            responseCnt.length = len(content)
            responseCnt.source = (output.getvalue(),)
        return