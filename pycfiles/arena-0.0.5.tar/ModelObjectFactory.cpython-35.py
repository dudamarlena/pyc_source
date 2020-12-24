# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /tmp/pip-install-ncu5lfw4/arelle/arelle/ModelObjectFactory.py
# Compiled at: 2018-08-09 04:11:41
# Size of source mod 2**32: 8302 bytes
__doc__ = '\nCreated on Jun 10, 2011\nRefactored on Jun 11, 2011 to ModelDtsObject, ModelInstanceObject, ModelTestcaseObject\n\n@author: Mark V Systems Limited\n(c) Copyright 2011 Mark V Systems Limited, All rights reserved.\n'
from arelle.ModelObject import ModelObject, init as moduleObject_init
elementSubstitutionModelClass = {}
from lxml import etree
from arelle import XbrlConst, XmlUtil
from arelle.ModelValue import qnameNsLocalName
from arelle.ModelDtsObject import ModelConcept, ModelAttribute, ModelAttributeGroup, ModelType, ModelGroupDefinition, ModelAll, ModelChoice, ModelSequence, ModelAny, ModelAnyAttribute, ModelEnumeration, ModelRoleType, ModelLocator, ModelLink, ModelResource
ModelDocument = ModelFact = None
from arelle.ModelRssItem import ModelRssItem
from arelle.ModelTestcaseObject import ModelTestcaseVariation
from arelle.ModelVersObject import ModelAssignment, ModelAction, ModelNamespaceRename, ModelRoleChange, ModelVersObject, ModelConceptUseChange, ModelConceptDetailsChange, ModelRelationshipSetChange, ModelRelationshipSet, ModelRelationships

def parser(modelXbrl, baseUrl, target=None):
    moduleObject_init()
    parser = etree.XMLParser(recover=True, huge_tree=True, target=target)
    return setParserElementClassLookup(parser, modelXbrl, baseUrl)


def setParserElementClassLookup(parser, modelXbrl, baseUrl=None):
    classLookup = DiscoveringClassLookup(modelXbrl, baseUrl)
    nsNameLookup = KnownNamespacesModelObjectClassLookup(modelXbrl, fallback=classLookup)
    parser.set_element_class_lookup(nsNameLookup)
    return (
     parser, nsNameLookup, classLookup)


SCHEMA = 1
LINKBASE = 2
VERSIONINGREPORT = 3
RSSFEED = 4

class KnownNamespacesModelObjectClassLookup(etree.CustomElementClassLookup):

    def __init__(self, modelXbrl, fallback=None):
        super(KnownNamespacesModelObjectClassLookup, self).__init__(fallback)
        self.modelXbrl = modelXbrl
        self.type = None

    def lookup(self, node_type, document, ns, ln):
        if node_type == 'element':
            if ns == XbrlConst.xsd:
                if self.type is None:
                    self.type = SCHEMA
                if ln == 'element':
                    return ModelConcept
                if ln == 'attribute':
                    return ModelAttribute
                if ln == 'attributeGroup':
                    return ModelAttributeGroup
                if ln == 'complexType' or ln == 'simpleType':
                    return ModelType
                if ln == 'group':
                    return ModelGroupDefinition
                if ln == 'sequence':
                    return ModelSequence
                if ln == 'choice' or ln == 'all':
                    return ModelChoice
                if ln == 'all':
                    return ModelAll
                if ln == 'any':
                    return ModelAny
                if ln == 'anyAttribute':
                    return ModelAnyAttribute
                if ln == 'enumeration':
                    return ModelEnumeration
            else:
                if ns == XbrlConst.link:
                    if self.type is None:
                        self.type = LINKBASE
                    if ln == 'roleType' or ln == 'arcroleType':
                        return ModelRoleType
                elif ns == 'http://edgar/2009/conformance':
                    if ln == 'variation':
                        return ModelTestcaseVariation
                    else:
                        return ModelObject
        if ln == 'testcase' and (ns is None or ns in ('http://edgar/2009/conformance', ) or ns.startswith('http://xbrl.org/')):
            return ModelObject
        if ln == 'variation' and (ns is None or ns in ('http://edgar/2009/conformance', ) or ns.startswith('http://xbrl.org/')):
            return ModelTestcaseVariation
        if ln == 'testGroup' and ns == 'http://www.w3.org/XML/2004/xml-schema-test-suite/':
            return ModelTestcaseVariation
        if ln == 'test-case' and ns == 'http://www.w3.org/2005/02/query-test-XQTSCatalog':
            return ModelTestcaseVariation
        if ns == XbrlConst.ver:
            if self.type is None:
                self.type = VERSIONINGREPORT
        elif ns == 'http://dummy':
            return etree.ElementBase
        if self.type is None and ln == 'rss':
            self.type = RSSFEED
        else:
            if self.type == RSSFEED:
                if ln == 'item':
                    return ModelRssItem
                return ModelObject
            return self.modelXbrl.matchSubstitutionGroup(qnameNsLocalName(ns, ln), elementSubstitutionModelClass)
        if node_type == 'comment':
            from arelle.ModelObject import ModelComment
            return ModelComment
        if node_type == 'PI':
            return etree.PIBase
        if node_type == 'entity':
            return etree.EntityBase


class DiscoveringClassLookup(etree.PythonElementClassLookup):

    def __init__(self, modelXbrl, baseUrl, fallback=None):
        global ModelDocument
        global ModelFact
        super(DiscoveringClassLookup, self).__init__(fallback)
        self.modelXbrl = modelXbrl
        self.streamingOrSkipDTS = modelXbrl.skipDTS or getattr(modelXbrl, 'isStreamingMode', False)
        self.baseUrl = baseUrl
        self.discoveryAttempts = set()
        if ModelDocument is None:
            from arelle import ModelDocument
        if self.streamingOrSkipDTS and ModelFact is None:
            from arelle.ModelInstanceObject import ModelFact

    def lookup(self, document, proxyElement):
        ns, sep, ln = proxyElement.tag.partition('}')
        if sep:
            ns = ns[1:]
        else:
            ln = ns
            ns = None
        if ns and ns not in self.discoveryAttempts and ns not in self.modelXbrl.namespaceDocs:
            relativeUrl = XmlUtil.schemaLocation(proxyElement, ns)
            self.discoveryAttempts.add(ns)
            if relativeUrl:
                doc = ModelDocument.loadSchemalocatedSchema(self.modelXbrl, proxyElement, relativeUrl, ns, self.baseUrl)
        modelObjectClass = self.modelXbrl.matchSubstitutionGroup(qnameNsLocalName(ns, ln), elementSubstitutionModelClass)
        if modelObjectClass is not None:
            return modelObjectClass
        if self.streamingOrSkipDTS and ns not in (XbrlConst.xbrli, XbrlConst.link):
            ancestor = proxyElement.getparent() or getattr(self.modelXbrl, 'makeelementParentModelObject', None)
            while ancestor is not None:
                tag = ancestor.tag
                if tag.startswith('{http://www.xbrl.org/2003/instance}') or tag.startswith('{http://www.xbrl.org/2003/linkbase}'):
                    if tag == '{http://www.xbrl.org/2003/instance}xbrl':
                        return ModelFact
                    break
                ancestor = ancestor.getparent()

        xlinkType = proxyElement.get('{http://www.w3.org/1999/xlink}type')
        if xlinkType == 'extended':
            return ModelLink
        if xlinkType == 'locator':
            return ModelLocator
        if xlinkType == 'resource':
            return ModelResource
        return ModelObject