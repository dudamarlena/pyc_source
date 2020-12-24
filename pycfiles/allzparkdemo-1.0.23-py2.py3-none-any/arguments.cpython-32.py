# uncompyle6 version 3.6.7
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/ally/core/impl/processor/arguments.py
# Compiled at: 2013-10-02 09:54:40
__doc__ = '\nCreated on Aug 8, 2011\n\n@package: ally core\n@copyright: 2011 Sourcefabric o.p.s.\n@license: http://www.gnu.org/licenses/gpl-3.0.txt\n@author: Gabriel Nistor\n\nProvides the integration of the additional arguments into the main arguments.\n'
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