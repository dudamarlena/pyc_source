# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ally/core/http/impl/processor/redirect.py
# Compiled at: 2013-10-02 09:54:40
"""
Created on Apr 12, 2012

@package: ally core
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the content location redirect based on references.
"""
from ally.api.operator.type import TypeModelProperty
from ally.api.type import TypeReference
from ally.container.ioc import injected
from ally.core.http.spec.codes import REDIRECT
from ally.core.spec.resources import Invoker
from ally.design.processor.assembly import Assembly
from ally.design.processor.attribute import requires, defines
from ally.design.processor.context import Context
from ally.design.processor.execution import Processing, Chain
from ally.design.processor.handler import HandlerBranching
from ally.design.processor.processor import Included
from ally.http.spec.server import IEncoderHeader, IEncoderPath
import logging
log = logging.getLogger(__name__)

class Request(Context):
    """
    The request context.
    """
    invoker = requires(Invoker)


class Response(Context):
    """
    The response context.
    """
    encoderHeader = requires(IEncoderHeader)
    encoderPath = requires(IEncoderPath)
    obj = requires(object)
    code = defines(str)
    status = defines(int)
    isSuccess = defines(bool)


@injected
class RedirectHandler(HandlerBranching):
    """
    Implementation for a processor that provides the redirect by using the content location based on found references.
    """
    nameLocation = 'Location'
    redirectAssembly = Assembly

    def __init__(self):
        assert isinstance(self.redirectAssembly, Assembly), 'Invalid redirect assembly %s' % self.redirectAssembly
        assert isinstance(self.nameLocation, str), 'Invalid string %s' % self.nameLocation
        super().__init__(Included(self.redirectAssembly))

    def process(self, chain, redirect, request: Request, response: Response, **keyargs):
        """
        @see: HandlerBranching.process
        
        Process the redirect.
        """
        assert isinstance(chain, Chain), 'Invalid processors chain %s' % chain
        assert isinstance(redirect, Processing), 'Invalid processing %s' % redirect
        assert isinstance(request, Request), 'Invalid request %s' % request
        assert isinstance(response, Response), 'Invalid response %s' % response
        if response.isSuccess is not False:
            assert isinstance(request.invoker, Invoker), 'Invalid request invoker %s' % request.invoker
            assert isinstance(response.encoderHeader, IEncoderHeader), 'Invalid header encoder %s' % response.encoderHeader
            assert isinstance(response.encoderPath, IEncoderPath), 'Invalid encoder path %s' % response.encoderPath
            typ = request.invoker.output
            if isinstance(typ, TypeModelProperty):
                typ = typ.type
            if isinstance(typ, TypeReference):
                Chain(redirect).process(request=request, response=response, **keyargs).doAll()
                if response.isSuccess is not False:
                    response.encoderHeader.encode(self.nameLocation, response.encoderPath.encode(response.obj))
                    response.code, response.status, response.isSuccess = REDIRECT
                    return
        chain.proceed()