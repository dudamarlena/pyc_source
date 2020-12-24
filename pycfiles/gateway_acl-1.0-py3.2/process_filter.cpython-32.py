# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/acl/core/impl/processor/assembler/process_filter.py
# Compiled at: 2013-10-04 10:48:33
"""
Created on Aug 7, 2013

@package: gateway acl
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the filter calls processing.
"""
from ally.api.config import GET
from ally.api.operator.type import TypeModel, TypeProperty, TypeCall
from ally.api.type import Type, typeFor
from ally.container.ioc import injected
from ally.container.support import setup
from ally.design.processor.attribute import requires, defines, definesIf
from ally.design.processor.context import Context
from ally.design.processor.execution import Abort
from ally.design.processor.handler import HandlerProcessor, Handler
from gateway.api.gateway import Allowed
import logging
log = logging.getLogger(__name__)

class Register(Context):
    """
    The register context.
    """
    hintsCall = definesIf(dict)
    invokers = requires(list)


class Invoker(Context):
    """
    The invoker context.
    """
    path = defines(list, doc='\n    @rtype: list[Context]\n    The starting path elements for filter.\n    ')
    filterName = definesIf(str, doc='\n    @rtype: string\n    If present it means the invoker is a filter type invoker and is known with the provided name.\n    ')
    call = requires(TypeCall)
    method = requires(int)
    output = requires(Type)
    location = requires(str)


class ElementFilter(Context):
    """
    The element context.
    """
    name = defines(str, doc='\n    @rtype: string\n    The element name.\n    ')
    model = defines(TypeModel, doc='\n    @rtype: TypeModel\n    The model represented by the element.\n    ')


@injected
@setup(Handler, name='processFilter')
class ProcessFilterHandler(HandlerProcessor):
    """
    Implementation for a processor that provides the filter calls processing.
    """
    hintName = 'filter'
    hintDescription = '(string) The filter name to associate with the filter call, the filter calls are specially managed by the container, the sole purpose of this type of calls is to validate resources and should not be used as part of the main API.'
    typeModelAllowed = typeFor(Allowed)
    typePropertyAllowed = typeFor(Allowed.IsAllowed)

    def __init__(self):
        assert isinstance(self.hintName, str), 'Invalid hint name %s' % self.hintName
        assert isinstance(self.hintDescription, str), 'Invalid hint description %s' % self.hintDescription
        assert isinstance(self.typeModelAllowed, TypeModel), 'Invalid type model allowed %s' % self.typeModelAllowed
        assert isinstance(self.typePropertyAllowed, TypeProperty), 'Invalid type property allowed %s' % self.typePropertyAllowed
        super().__init__(Invoker=Invoker)

    def process(self, chain, register: Register, Element: ElementFilter, **keyargs):
        """
        @see: HandlerProcessor.process
        
        Process the filter calls.
        """
        assert isinstance(register, Register), 'Invalid register %s' % register
        assert issubclass(Element, ElementFilter), 'Invalid path element %s' % Element
        if not register.invokers:
            return
        else:
            if Register.hintsCall in register:
                if register.hintsCall is None:
                    register.hintsCall = {}
                register.hintsCall[self.hintName] = self.hintDescription
            aborted = []
            for invoker in register.invokers:
                assert isinstance(invoker, Invoker), 'Invalid invoker %s' % invoker
                if not invoker.call:
                    continue
                assert isinstance(invoker.call, TypeCall), 'Invalid call %s' % invoker.call
                if self.hintName not in invoker.call.hints:
                    continue
                filterName = invoker.call.hints[self.hintName]
                if not isinstance(filterName, str) and filterName:
                    log.error("Cannot use because invalid filter name '%s', expected a string value with at least one character, at:%s", filterName, invoker.location)
                    aborted.append(invoker)
                    continue
                if not invoker.method == GET:
                    log.error('Cannot use because filter call needs to be a GET call, at:%s', invoker.location)
                    aborted.append(invoker)
                    continue
                assert isinstance(invoker.output, Type), 'Invalid output %s' % invoker.output
                if not invoker.output.isOf(bool):
                    log.error("Cannot use because filter call has invalid output '%s', expected a boolean return, at:%s", invoker.output, invoker.location)
                    aborted.append(invoker)
                    continue
                if invoker.path is None:
                    invoker.path = []
                invoker.path.insert(0, Element(name=self.typeModelAllowed.name, model=self.typeModelAllowed))
                invoker.output = self.typePropertyAllowed
                if Invoker.filterName in invoker:
                    invoker.filterName = filterName.strip()
                    continue

            if aborted:
                raise Abort(*aborted)
            return