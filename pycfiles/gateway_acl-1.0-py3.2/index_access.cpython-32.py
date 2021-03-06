# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/acl/core/impl/processor/assembler/index_access.py
# Compiled at: 2013-10-29 05:41:07
"""
Created on Aug 8, 2013

@package: gateway acl
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Indexes the access invokers.
"""
from acl.api.access import IAccessService, Access, AccessCreate, generateId, generateHash
from acl.core.spec import signature
from ally.api.operator.type import TypeProperty, TypeModel, TypePropertyContainer
from ally.api.type import Input, Type, Non
from ally.container import wire
from ally.container.ioc import injected
from ally.container.support import setup
from ally.design.processor.attribute import requires, attribute
from ally.design.processor.context import Context
from ally.design.processor.handler import HandlerProcessor, Handler
from ally.http.spec.server import HTTP_POST, HTTP_PUT, HTTP_GET
import logging
log = logging.getLogger(__name__)

class Register(Context):
    """
    The register context.
    """
    invokers = requires(list)


class Invoker(Context):
    """
    The invoker context.
    """
    path = requires(list)
    methodHTTP = requires(str)
    output = requires(Type)
    modelInput = requires(Input)
    filterName = requires(str)
    shadowing = requires(Context)
    shadowed = requires(Context)


class Element(Context):
    """
    The element context.
    """
    accessEntryPosition = attribute(int, doc='\n    @rtype: integer\n    The access entry position assigned for the path element.\n    ')
    name = requires(str)
    property = requires(TypeProperty)
    shadowing = requires(Context)
    shadowed = requires(Context)


@injected
@setup(Handler, name='indexAccess')
class IndexAccessHandler(HandlerProcessor):
    """
    Implementation for a processor that indexes the access invokers by name.
    """
    input_methods = [
     HTTP_POST, HTTP_PUT]
    wire.config('input_methods', doc='\n    @rtype: list[string]\n    The HTTP method names that can have an input model in order to be processed by ACL.\n    ')
    excludable_methods = [HTTP_GET]
    wire.config('excludable_methods', doc='\n    @rtype: list[string]\n    The HTTP method names that can have excludable names to be processed by ACL.\n    ')
    accessService = IAccessService
    wire.entity('accessService')

    def __init__(self):
        assert isinstance(self.input_methods, list), 'Invalid input methods %s' % self.input_methods
        assert isinstance(self.excludable_methods, list), 'Invalid excludable methods %s' % self.excludable_methods
        assert isinstance(self.accessService, IAccessService), 'Invalid access service %s' % self.accessService
        super().__init__(Invoker=Invoker, Element=Element)
        self.input_methods = set(self.input_methods)
        self.excludable_methods = set(self.excludable_methods)

    def process(self, chain, register: Register, **keyargs):
        """
        @see: HandlerProcessor.process
        
        Merge the access invokers.
        """
        assert isinstance(register, Register), 'Invalid register %s' % register
        if not register.invokers:
            return
        else:
            shadows = []
            for invoker in register.invokers:
                assert isinstance(invoker, Invoker), 'Invalid invoker %s' % invoker
                if invoker.filterName is not None:
                    continue
                if invoker.shadowing:
                    shadows.append(invoker)
                    continue
                self.mergeAccess(invoker)

            for invoker in shadows:
                self.mergeAccess(invoker)

            return

    def mergeAccess(self, invoker):
        """
        Creates and persist the access for the provided invoker.
        """
        assert isinstance(invoker, Invoker), 'Invalid invoker %s' % invoker
        access = AccessCreate()
        access.Method = invoker.methodHTTP
        access.Output = signature(Non if invoker.output is None else invoker.output)
        position, items = 1, []
        for el in invoker.path:
            assert isinstance(el, Element), 'Invalid element %s' % el
            if el.property:
                if el.shadowing:
                    assert isinstance(el.shadowing, Element), 'Invalid element %s' % el.shadowing
                    assert isinstance(el.shadowing.accessEntryPosition, int), 'Invalid element position %s' % el.shadowing.accessEntryPosition
                    if access.EntriesShadowing is None:
                        access.EntriesShadowing = {}
                    access.EntriesShadowing[position] = el.shadowing.accessEntryPosition
                else:
                    if el.shadowed:
                        assert isinstance(el.shadowed, Element), 'Invalid element %s' % el.shadowed
                        assert isinstance(el.shadowed.accessEntryPosition, int), 'Invalid element position %s' % el.shadowed.accessEntryPosition
                        if access.EntriesShadowed is None:
                            access.EntriesShadowed = {}
                        access.EntriesShadowed[position] = el.shadowed.accessEntryPosition
                    else:
                        if access.Entries is None:
                            access.Entries = {}
                        access.Entries[position] = signature(el.property)
                        el.accessEntryPosition = position
                items.append('*')
                position += 1
            else:
                assert isinstance(el.name, str), 'Invalid element name %s' % el.name
                items.append(el.name)

        access.Path = '/'.join(items)
        if invoker.shadowing:
            spath = '/'.join(('*' if el.property else el.name) for el in invoker.shadowing.path)
            access.Shadowing = generateId(spath, invoker.shadowing.methodHTTP)
            spath = '/'.join(('*' if el.property else el.name) for el in invoker.shadowed.path)
            access.Shadowed = generateId(spath, invoker.shadowed.methodHTTP)
        if invoker.methodHTTP in self.input_methods and invoker.modelInput:
            assert isinstance(invoker.modelInput, Input), 'Invalid input %s' % invoker.modelInput
            assert isinstance(invoker.modelInput.type, TypeModel), 'Invalid model %s' % invoker.modelInput.type
            for name, prop in invoker.modelInput.type.properties.items():
                if not isinstance(prop, TypePropertyContainer):
                    continue
                assert isinstance(prop, TypePropertyContainer)
                if access.Properties is None:
                    access.Properties = {}
                access.Properties[name] = signature(prop.type)

        try:
            present = self.accessService.getById(generateId(access.Path, access.Method))
        except:
            if not log.debug("There is no access for '%s' with %s", access.Path, access.Method):
                assert True
        else:
            assert isinstance(present, Access), 'Invalid access %s' % present
            assert present.Path == access.Path, "Problems with hashing, hash %s it is the same for '%s' and '%s'" % (access.Id, present.Path, access.Path)
            if present.Hash == generateHash(access):
                return
            log.info('Removing access %s since is not compatible with the current structure', present)
            self.accessService.delete(present.Id)
        self.accessService.insert(access)
        if not log.debug('Added access %s', access):
            assert True
        return