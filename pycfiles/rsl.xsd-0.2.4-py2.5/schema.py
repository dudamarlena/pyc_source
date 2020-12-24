# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/rsl/xsd/schema.py
# Compiled at: 2009-01-12 07:29:42
"""
This module provides an ISchema implementation for xsd-schemas to be used in 
rsl.
"""
import warnings, urllib2, urlparse
from lxml import etree
from zope.interface import implements
from rsl.interfaces import ISchema
from rsl.misc.namespace import clark2tuple
from rsl.xsd.urtype import AnyType
from rsl.xsd.component import XSAnnotated, XSElement, XSComplexType, XSGroup
from rsl.xsd.component import XSAttribute, XSSimpleType
from rsl.xsd.namespace import NS_XMLSCHEMA, NS_XMLSCHEMA_99

class ComplexType(AnyType):
    """
    This may become the base type for all schema types.
    """
    pass


class XMLSchema(XSAnnotated):
    """ 
    This is the top level Schema representation. (<schema> ... </schema>)
    """
    implements(ISchema)

    def __init__(self, manager=None, uri=None):
        """
        initialise a blank XMLSchema instance.
        """
        self.manager = manager
        self.uri = uri
        self.attributeformdefault = 'unqualified'
        self.elementformdefault = 'unqualified'
        self.targetnamespace = None
        self.types = {}
        self.elements = {}
        self.groups = {}
        self.attributes = {}
        self.attributegroups = {}
        self.annotations = {}
        return

    def frometree(self, schemaelem):
        """
        load all data from schemaelem (etree) into this instance.
        
        this method does all the preparations and reads in data on
        <schema> element, and passes the actual work to _parseSchema
        """
        super(XMLSchema, self).frometree(schemaelem)
        if schemaelem is not None:
            self.attributeformdefault = schemaelem.get('attributeFormDefault', 'unqualified')
            self.elementformdefault = schemaelem.get('elementFormDefault', 'unqualified')
            self.targetnamespace = schemaelem.get('targetNamespace')
        else:
            self.attributeformdefault = 'unqualified'
            self.elementformdefault = 'unqualified'
        if schemaelem is not None:
            self._parseSchema(schemaelem)
        return self

    def _parseSchema(self, schemaelem):
        """
        parse all schema definitions contained in the etree schemaelem.
        """
        for elem in schemaelem.getchildren():
            if elem.tag == etree.Comment:
                continue
            (elemns, elemname) = clark2tuple(elem.tag)
            if elemns in (NS_XMLSCHEMA, NS_XMLSCHEMA_99):
                if elemname == 'element':
                    self.elements[elem.get('name')] = XSElement(elem, self)
                elif elemname == 'complexType':
                    self.types[elem.get('name')] = XSComplexType(elem, self)
                elif elemname == 'import':
                    namespace = elem.get('namespace')
                    schemalocation = elem.get('schemaLocation')
                    if namespace:
                        if namespace == self.targetnamespace:
                            raise Exception("can't import schema with the same                                              namespace as targetNamespace")
                        try:
                            if self.getSchema(namespace):
                                continue
                        except KeyError:
                            pass

                    if schemalocation:
                        try:
                            impuri = urlparse.urljoin(self.uri, schemalocation)
                            fobj = urllib2.urlopen(impuri)
                            importtree = etree.parse(fobj)
                            fobj.close()
                            importxsd = XMLSchema(self.manager, uri=impuri)
                            importxsd.frometree(importtree.getroot())
                            if namespace:
                                if namespace != importxsd.targetnamespace:
                                    warnings.warn('namespace and                                         targetNamespace of imported schema must                                         be equal (%s, %s)' % (
                                     namespace, importxsd.targetnamespace))
                            if self.manager is not None:
                                self.manager.addSchema(importxsd)
                            else:
                                warnings.warn('can not import schema, beause                                              there is no local schema manager')
                        except OSError:
                            warnings.warn("can not import schema because I                                            can't open location.")

                elif elemname == 'include':
                    schemalocation = elem.get('schemaLocation')
                    if schemalocation:
                        includeuri = urlparse.urljoin(self.uri, schemalocation)
                        includetree = etree.parse(includeuri)
                        includexsd = XMLSchema(self.manager, includeuri)
                        includexsd.frometree(includetree.getroot())
                        if includexsd.targetnamespace is not None and includexsd.targetnamespace != self.targetnamespace:
                            raise Exception('include different namespace                                              not allowed')
                    warnings.warn('Include: schema merge not implemented ' + str(elem.attrib))
                elif elemname == 'group':
                    self.groups[elem.get('name')] = XSGroup(elem, self)
                elif elemname == 'simpleType':
                    self.types[elem.get('name')] = XSSimpleType(elem, self)
                elif elemname == 'attributeGroup':
                    pass
                elif elemname == 'notation':
                    pass
                elif elemname == 'attribute':
                    self.attributes[elem.get('name')] = XSAttribute(elem, self)
                else:
                    warnings.warn('Schemaelement : ' + elem.tag + ' not implemented')
            else:
                raise Warning('Schemanamespace : ' + elemns + ' not supported.')

        return

    def tostring(self):
        """
        return a nice string representation of this schema to print on stdout.
        """
        ret = ''
        for (xns, xstype) in self.types.items():
            ret += '%s => %s\n' % (xns, xstype)

        for (xns, xselem) in self.elements.items():
            ret += '%s => %s\n' % (xns, xselem)

        return ret

    def getElement(self, nameref):
        """
        Find an xsd-element instance by named reference in clark notation.
        
        @todo: this code is duplicated in XMLSchemaManager        
        """
        (xns, name) = clark2tuple(nameref)
        xmls = self.getSchema(xns)
        if name in xmls.elements:
            return xmls.elements[name]
        raise KeyError('Element %s in namespace %s not found' % (name, xns))

    def getType(self, nameref):
        """
        Find an xsd-type instance by named reference in clark notation.
        
        @todo: this code is duplicated in XMLSchemaManager
        """
        (xns, name) = clark2tuple(nameref)
        xmls = self.getSchema(xns)
        if name in xmls.types:
            return xmls.types[name]
        raise KeyError('Type %s in namespace %s not found' % (name, xns))

    def getAttribute(self, nameref):
        """
        Find an xsd-attribute instance by named reference in clark notation.
        
        @todo: this code is duplicated in XMLSchemaManager
        """
        (xns, name) = clark2tuple(nameref)
        xmls = self.getSchema(xns)
        if name in xmls.attributes:
            return xmls.attributes[name]
        raise KeyError('Attribute %s in namespace %s not found' % (name, xns))

    def getGroup(self, nameref):
        """
        Find an xsd-group instance by named reference in clark notation.
        
        @todo: this code is duplicated in XMLSchemaManager
        """
        (xns, name) = clark2tuple(nameref)
        xmls = self.getSchema(xns)
        if name in xmls.groups:
            return xmls.groups[name]
        raise KeyError('Group %s in namespace %s not found' % (name, xns))

    def getSchema(self, namespace):
        """
        Find a schema by namespace. If it is not this schema, ask the parent
        manager to retrieve it.
        """
        if self.targetnamespace == namespace:
            return self
        if self.manager:
            return self.manager.getSchema(namespace)
        raise KeyError('Schema %s not found' % namespace)