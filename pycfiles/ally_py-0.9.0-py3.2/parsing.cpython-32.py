# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ally/core/impl/processor/parsing.py
# Compiled at: 2013-10-02 09:54:40
"""
Created on Aug 24, 2012

@package: ally core
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the parsing chain processors.
"""
from ally.container.ioc import injected
from ally.core.spec.codes import ENCODING_UNKNOWN
from ally.design.processor.assembly import Assembly
from ally.design.processor.attribute import requires, defines
from ally.design.processor.context import Context
from ally.design.processor.execution import Chain, Processing
from ally.design.processor.handler import HandlerBranching
from ally.design.processor.processor import Included
from collections import Callable
import codecs
from itertools import chain

class Request(Context):
    """
    The request context.
    """
    decoder = requires(Callable)


class RequestContent(Context):
    """
    The request content context.
    """
    type = requires(str)
    charSet = requires(str)


class Response(Context):
    """
    The response context.
    """
    code = defines(str)
    isSuccess = defines(bool)
    text = defines(str)


class ResponseContent(Context):
    """
    The response context.
    """
    type = requires(str)


@injected
class ParsingHandler(HandlerBranching):
    """
    Implementation for a processor that provides the parsing based on contained parsers. If a parser
    processor is successful in the parsing process it has to stop the chain execution.
    """
    charSetDefault = str
    parsingAssembly = Assembly

    def __init__(self, *branches):
        assert isinstance(self.parsingAssembly, Assembly), 'Invalid parsers assembly %s' % self.parsingAssembly
        assert isinstance(self.charSetDefault, str), 'Invalid default character set %s' % self.charSetDefault
        super().__init__(*chain(branches, (Included(self.parsingAssembly),)))

    def process(self, chain, parsing, request: Request, requestCnt: RequestContent, response: Response, **keyargs):
        """
        @see: HandlerBranching.process
        
        Parse the request content.
        """
        assert isinstance(chain, Chain), 'Invalid processors chain %s' % chain
        assert isinstance(parsing, Processing), 'Invalid processing %s' % parsing
        assert isinstance(request, Request), 'Invalid request %s' % request
        assert isinstance(response, Response), 'Invalid response %s' % response
        chain.proceed()
        if response.isSuccess is False:
            return
        else:
            if request.decoder is None:
                return
            if self.processParsing(parsing, request=request, requestCnt=requestCnt, response=response, **keyargs):
                chain.arg.requestCnt = None
            return

    def processParsing(self, parsing, request, requestCnt, response, responseCnt, **keyargs):
        """
        Process the parsing for the provided contexts.
        
        @return: boolean
            True if the parsing has been successfully done on the request content.
        """
        assert isinstance(parsing, Processing), 'Invalid processing %s' % parsing
        assert isinstance(request, Request), 'Invalid request %s' % request
        assert isinstance(requestCnt, RequestContent), 'Invalid request content %s' % requestCnt
        assert isinstance(response, Response), 'Invalid response %s' % response
        assert isinstance(responseCnt, ResponseContent), 'Invalid response content %s' % responseCnt
        if requestCnt.charSet:
            try:
                codecs.lookup(requestCnt.charSet)
            except LookupError:
                requestCnt.charSet = self.charSetDefault

        else:
            requestCnt.charSet = self.charSetDefault
        if not requestCnt.type:
            requestCnt.type = responseCnt.type
        chain = Chain(parsing)
        chain.process(request=request, requestCnt=requestCnt, response=response, responseCnt=responseCnt, **keyargs)
        if not chain.doAll().isConsumed():
            return True
        if response.isSuccess is not False:
            response.code, response.isSuccess = ENCODING_UNKNOWN
            response.text = "Content type '%s' not supported for parsing" % requestCnt.type