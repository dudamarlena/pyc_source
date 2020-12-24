# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/rsl/xsd/manager.py
# Compiled at: 2009-01-12 07:29:42
"""
This module implements an XMLSchemaManager. An XMLSchemaManager, handles 
globally known schemata, and allows lookup of imported and well known schemata
from it's sub-schemata.
"""
from zope.interface import implements
from rsl.interfaces import ISchemaCollection, ISchemaFactory
from rsl.misc.namespace import clark2tuple
from rsl.globalregistry import lookupimpl
from rsl.xsd.schema import XMLSchema

class XMLSchemaManager(object):
    """
    A schema manager holds XSSchema instances for various namespaces.
    It helps to lookup types and elements in parsed schemas.
    """
    implements(ISchemaCollection)

    def __init__(self, parent=None):
        """
        initialise this schema manager.
        the parent manager is asked, if the manager itself does not know
        a requested schema. If parent is none, then this manager is the 
        root manager.
        """
        self.parent = parent
        self.schemas = {}

    def loadStandardSchema(self, namespace):
        """
        If an xml schema is found nowhere else, try to find a registered
        ISchemaFactory which may provide the requested namespace url.
        This function is only executed in the root schema manager.
        """
        xsdf = lookupimpl(ISchemaFactory, namespace)
        if xsdf is not None:
            self.addSchema(xsdf(self))
        return

    def addSchema(self, schema):
        """
        Add an ISchema instance to this schema manager.
        """
        self.schemas[schema.targetnamespace] = schema
        schema.manager = self

    def getElement(self, nameref):
        """
        Find an xsd-element instance by named reference in clark notation.
        
        @todo: this code is duplicated in XMLSchema
        """
        (xns, name) = clark2tuple(nameref)
        xmls = self.getSchema(xns)
        if name in xmls.elements:
            return xmls.elements[name]
        raise KeyError('Element %s in namespace %s not found' % (name, xns))

    def getType(self, nameref):
        """
        Find an xsd-type instance by named reference in clark notation.
        
        @todo: this code is duplicated in XMLSchema
        """
        (xns, name) = clark2tuple(nameref)
        xmls = self.getSchema(xns)
        if name in xmls.types:
            return xmls.types[name]
        raise KeyError('Type %s in namespace %s not found' % (name, xns))

    def getAttribute(self, nameref):
        """
        Find an xsd-attribute instance by named reference in clark notation.
        
        @todo: this code is duplicated in XMLSchema
        """
        (xns, name) = clark2tuple(nameref)
        xmls = self.getSchema(xns)
        if name in xmls.attributes:
            return xmls.attributes[name]
        raise KeyError('Attribute %s in namespace %s not found' % (name, xns))

    def getGroup(self, nameref):
        """
        Find an xsd-group instance by named reference in clark notation.
        
        @todo: this code is duplicated in XMLSchema
        """
        (xns, name) = clark2tuple(nameref)
        xmls = self.getSchema(xns)
        if name in xmls.groups:
            return xmls.groups[name]
        raise KeyError('Group %s in namespace %s not found' % (name, xns))

    def getSchema(self, namespace):
        """
        Find a registered ISchema instance by namespace. If it is not found in
        this schema manager, then the parent schema manager is asked. If the
        root schema manager does not know it, it tries to find a registered
        ISchemaFactory for this namespace.
        
        @todo: this code is duplicated in XMLSchema
        """
        if namespace in self.schemas:
            return self.schemas[namespace]
        if self.parent:
            return self.parent.getSchema(namespace)
        self.loadStandardSchema(namespace)
        return self.schemas[namespace]

    def parseSchema(self, schema_tree):
        """
        This function takes an etree representing a schema file 
        and adds the containing schemas to this schema manager
        """
        schema = XMLSchema(schema_tree, self)
        self.addSchema(schema)


GLOBALSCHEMAMANAGER = XMLSchemaManager()