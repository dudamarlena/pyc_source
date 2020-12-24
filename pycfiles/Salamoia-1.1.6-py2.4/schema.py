# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/salamoia/nacl/ldap/schema.py
# Compiled at: 2007-12-02 16:26:58
from salamoia.h2o.logioni import Ione
from salamoia.h2o.schema import Schema, EntityDescription, SingletonDescription, IAdapterDescription
from salamoia.h2o.decorators import lazy
from salamoia.nacl.ldap.object import LDAPObject
from salamoia.h2o.protocols import Interface, DelegatingAdapter, declareAdapter, adapt, NO_ADAPTER_NEEDED, declareMultiAdapter, multiAdapt
from salamoia.h2o.generics import Any, Each
from salamoia.h2o.functional import partial, rpartial

class ILdapSchemaDefinition(Interface):
    __module__ = __name__


class ILdapAdapterDefinition(Interface):
    __module__ = __name__


class AdapterDefinitionAdapter(DelegatingAdapter):
    __module__ = __name__

    def registerAdapter(self, schema):
        self.parent = schema
        if len(self.for_) == 1:
            if self.factory:
                declareAdapter(self.factory, [
                 self.parent.interface], forProtocols=[self.for_[0]])
            else:
                declareAdapter(lambda x: self.parent, [
                 self.parent.interface], forProtocols=[self.for_[0]])
                declareAdapter(NO_ADAPTER_NEEDED, [
                 self.parent.interface], forObjects=[self.parent])
        else:
            declareMultiAdapter(self.factory or self.constructFromAdaptation, [
             self.parent.interface], forProtocols=[self.for_])


declareAdapter(AdapterDefinitionAdapter, [ILdapAdapterDefinition], forProtocols=[IAdapterDescription])

class DefinitionAdapter(DelegatingAdapter):
    """
    This adapter adapts a schema definition description to a ldap specific schema definition.

    The difference is that a ldap specific definition knows about specific ldap classes like LDAPObject
    and is bound to a Schema (LDAPSchema) object.

    There can be multiple sepcific schema definition adapter for each schema definition
    """
    __module__ = __name__

    @lazy
    def containerClass(self):
        if self.container:
            return self.parent.classMap[self.container]

    def mergedInSchema(self, schema):
        self.schema = schema
        self.adapters = ILdapAdapterDefinition.conformingItems(self.children)
        Each(self.adapters).registerAdapter(self)


class EntityAdapter(DefinitionAdapter):
    __module__ = __name__

    @lazy
    def schemaClass(self):

        class SchemaClass(LDAPObject):
            __module__ = __name__

            def __init__(self, service=None):
                self._service = service
                super(self.__class__, self).__init__()
                self._updateStaticACL()

            requiredObjectClasses = self.subject.ldap.objectClasses.objectClasses
            primaryObjectClass = self.subject.ldap.objectClasses.structural
            attributeMap = {}
            for attr in self.subject.ldap.mappings:
                attributeMap[attr.ldap] = attr.name

            reverseAttributeMap = {}
            for k in attributeMap.keys():
                reverseAttributeMap[attributeMap[k]] = k

            _attributeTypeMap = {}
            for attr in self.subject.attributes:
                if attr.type is not None:
                    _attributeTypeMap[attr.name] = attr.type

            keyAttribute = self.subject.keyAttribute
            hookMap = {}
            creationHooks = []
            modificationHooks = []
            schema = self

        SchemaClass.__name__ = str(self.subject.name)
        try:
            for h in self.hooks:
                h.patchClass(SchemaClass)

            for a in self.attributes:
                for h in a.hooks:
                    h.patchClass(SchemaClass)

        except:
            Ione.exception('hooking hooks', traceback=True)

        return SchemaClass

    @property
    def containerClass(self):
        if self.container:
            return self.schema.classMap[self.container]


class SingletonAdapter(DefinitionAdapter):
    __module__ = __name__

    @lazy
    def schemaClass(self):

        class SchemaSingleton(LDAPObject):
            __module__ = __name__

            def __init__(self, service=None):
                self._service = service
                super(self.__class__, self).__init__()
                self._updateStaticACL()

            objectClasses = self.ldap.objectClasses.objectClasses
            primaryObjectClass = self.ldap.objectClasses.structural
            attributeMap = {}
            _attributeTypeMap = {}
            keyAttribute = self.dn.split('=')[0]
            schema = self

        SchemaSingleton.__name__ = '%s-singleton' % str(self.name)
        return SchemaSingleton

    def absoluteDN(self):
        if not self.container:
            return self.dn
        parent = self.schema.classMap[self.container]
        parentDN = parent.schema.absoluteDN()
        assert parentDN
        return self.dn + ',' + parentDN

    @property
    def containerClass(self):
        if self.container:
            return self.schema.classMap[self.container]


declareAdapter(EntityAdapter, [ILdapSchemaDefinition], forTypes=[EntityDescription])
declareAdapter(SingletonAdapter, [ILdapSchemaDefinition], forTypes=[SingletonDescription])

class LDAPSchema(Schema):
    """
    >>> s = LDAPSchema()
    >>> s.definitions
    {}
    """
    __module__ = __name__

    def __init__(self):
        super(LDAPSchema, self).__init__()
        self.classMap = {}
        self.reverseClassMap = {}
        self.objectClassMap = {}
        self.reverseObjectClassMap = {}

    def mergeDefinition(self, definition):
        definition = ILdapSchemaDefinition(definition)
        self.definitions[definition.name] = definition
        cls = definition.schemaClass
        self.classMap[cls.schema.name] = cls
        self.reverseClassMap[cls] = cls.schema.name
        self.objectClassMap[cls.schema.name] = cls.primaryObjectClass
        self.reverseObjectClassMap[cls.primaryObjectClass] = cls.schema.name
        definition.mergedInSchema(self)


from salamoia.tests import *
runDocTests()