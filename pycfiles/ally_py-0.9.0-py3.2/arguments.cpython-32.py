# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ally/core/impl/processor/arguments.py
# Compiled at: 2013-10-02 09:54:40
"""
Created on Aug 8, 2011

@package: ally core
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the integration of the additional arguments into the main arguments.
"""
from ally.api.type import Input, typeFor
from ally.core.spec.resources import Invoker, Path
from ally.design.processor.attribute import requires, defines
from ally.design.processor.context import Context
from ally.design.processor.handler import HandlerProcessorProceed

class RequestProvide(Context):
    """
    The request context.
    """
    arguments = defines(dict, doc='\n    @rtype: dictionary{string, object}\n    The dictionary containing the arguments that will be passes to the invoker that provides the response object.\n    ')
    argumentsOfType = defines(dict, doc='\n    @rtype: dictionary{Type, object}\n    A dictionary containing as a key the argument type, this dictionary needs to be populated by the \n    processors with any system values that might be used for invoking, the actual use of this arguments depends\n    ')


class ArgumentsPrepareHandler(HandlerProcessorProceed):
    """
    Implementation for a processor that provides the integration of the additional arguments into the invoke arguments.
    This processor will provide the argument by type.
    """

    def process(self, request: RequestProvide, **keyargs):
        """
        @see: HandlerProcessorProceed.process
        
        Provides the additional arguments by type to be populated.
        """
        assert isinstance(request, RequestProvide), 'Invalid request %s' % request
        request.argumentsOfType = {}
        request.arguments = {}


class Request(Context):
    """
    The request context.
    """
    path = requires(Path)
    invoker = requires(Invoker)
    argumentsOfType = requires(dict)
    arguments = requires(dict)


class ArgumentsBuildHandler(HandlerProcessorProceed):
    """
    Implementation for a processor that provides the integration of the additional arguments into the invoke arguments.
    """

    def process(self, request: Request, **keyargs):
        """
        @see: HandlerProcessorProceed.process
        
        Transpose the additional arguments into the main arguments.
        """
        assert isinstance(request, Request), 'Invalid request %s' % request
        if request.invoker is None:
            return
        else:
            assert isinstance(request.path, Path), 'Invalid request path %s' % request.path
            assert isinstance(request.invoker, Invoker), 'Invalid request invoker %s' % request.invoker
            if request.argumentsOfType:
                for inp in request.invoker.inputs:
                    assert isinstance(inp, Input), 'Invalid input %s' % inp
                    if inp.name in request.arguments:
                        continue
                    for argType, value in request.argumentsOfType.items():
                        if typeFor(argType) == inp.type:
                            if inp.name not in request.arguments:
                                request.arguments[inp.name] = value
                            break

            request.arguments.update(request.path.toArguments(request.invoker))
            return