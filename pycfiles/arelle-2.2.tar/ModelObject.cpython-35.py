# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-ncu5lfw4/arelle/arelle/ModelObject.py
# Compiled at: 2018-08-09 04:11:41
# Size of source mod 2**32: 15818 bytes
"""
Created on Oct 5, 2010
Refactored on Jun 11, 2011 to ModelDtsObject, ModelInstanceObject, ModelTestcaseObject

@author: Mark V Systems Limited
(c) Copyright 2010 Mark V Systems Limited, All rights reserved.
"""
from lxml import etree
from collections import namedtuple
from arelle import Locale
XmlUtil = None
VALID_NO_CONTENT = None
emptySet = set()

def init():
    global VALID_NO_CONTENT
    global XmlUtil
    if XmlUtil is None:
        from arelle import XmlUtil
        from arelle.XmlValidate import VALID_NO_CONTENT


class ModelObject(etree.ElementBase):
    __doc__ = "ModelObjects represent the XML elements within a document, and are implemented as custom \n    lxml proxy objects.  Each modelDocument has a parser with the parser objects in ModelObjectFactory.py, \n    to determine the type of model object to correspond to a proxied lxml XML element.  \n    Both static assignment of class, by namespace and local name, and dynamic assignment, by dynamic \n    resolution of element namespace and local name according to the dynamically loaded schemas, are \n    used in the ModelObjectFactory.\n    \n    ModelObjects are grouped into Python modules to ensure minimal inter-package references \n    (which causes a performance impact).  ModelDtsObjects collects DTS objects (schema and linkbase), \n    ModelInstanceObjects collects instance objects (facts, contexts, dimensions, and units), \n    ModelTestcaseObject collects testcase and variation objects, ModelVersioningObject has specialized \n    objects representing versioning report contents, and ModelRssItem represents the item objects in an \n    RSS feed.   \n    \n    The ModelObject custom lxml proxy object is implemented as a specialization of etree.ElementBase, \n    and used as the superclass of discovered and created objects in XML-based objects in Arelle.  \n    ModelObject is also used as a phantom proxy object, for non-XML objects that are resolved \n    from modelDocument objects, such as the ModelRelationship object.  ModelObjects persistent \n    with their owning ModelDocument, due to reference by modelObject list in modelDocument object.\n    \n    (The attributes and methods for ModelObject are in addition to those for lxml base class, _ElementBase.)\n\n\n        .. attribute:: modelDocument        \n        Owning ModelDocument object\n        \n        .. attribute:: modelXbrl\n        modelDocument's owning ModelXbrl object\n        \n        .. attribute:: localName\n        W3C DOM localName\n        \n        .. attribute:: prefixedName\n        Prefix by ancestor xmlns and localName of element\n        \n        .. attribute:: namespaceURI\n        W3C DOM namespaceURI (overridden for schema elements)\n        \n        .. attribute:: elementNamespaceURI\n        W3C DOM namespaceURI (not overridden by subclasses)\n        \n        .. attribute:: qname\n        QName of element (overridden for schema elements)\n        \n        .. attribute:: elementQname\n        QName of element (not overridden by subclasses)\n        \n        .. attribute:: parentQname\n        QName of parent element\n        \n        .. attribute:: id\n        Id attribute or None\n        \n        .. attribute:: elementAttributesTuple\n        Python tuple of (tag, value) of specified attributes of element, where tag is in Clark notation\n        \n        .. attribute:: elementAttributesStr\n        String of tag=value[,tag=value...] of specified attributes of element\n        \n        .. attribute:: xValid\n        XmlValidation.py validation state enumeration\n        \n        .. attribute:: xValue\n        PSVI value (for formula processing)\n        \n        .. attribute:: sValue\n        s-equals value (for s-equality)\n        \n        .. attribute:: xAttributes\n        Dict by attrTag of ModelAttribute objects (see below) of specified and default attributes of this element.\n    "

    def _init(self):
        self.isChanged = False
        parent = self.getparent()
        if parent is not None and hasattr(parent, 'modelDocument'):
            self.init(parent.modelDocument)

    def clear(self):
        self.__dict__.clear()
        super(ModelObject, self).clear()

    def init(self, modelDocument):
        self.modelDocument = modelDocument
        self.objectIndex = len(modelDocument.modelXbrl.modelObjects)
        modelDocument.modelXbrl.modelObjects.append(self)
        id = self.get('id')
        if id:
            modelDocument.idObjects[id] = self

    def objectId(self, refId=''):
        """Returns a string surrogate representing the object index of the model document, 
        prepended by the refId string.
        :param refId: A string to prefix the refId for uniqueless (such as to use in tags for tkinter)
        :type refId: str
        """
        return '_{0}_{1}'.format(refId, self.objectIndex)

    @property
    def modelXbrl(self):
        try:
            return self.modelDocument.modelXbrl
        except AttributeError:
            return

    def attr(self, attrname):
        return self.get(attrname)

    @property
    def slottedAttributesNames(self):
        return emptySet

    def setNamespaceLocalName(self):
        ns, sep, self._localName = self.tag.rpartition('}')
        if sep:
            self._namespaceURI = ns[1:]
        else:
            self._namespaceURI = None
        if self.prefix:
            self._prefixedName = self.prefix + ':' + self.localName
        else:
            self._prefixedName = self.localName

    def getStripped(self, attrName):
        attrValue = self.get(attrName)
        if attrValue is not None:
            return attrValue.strip()
        return attrValue

    @property
    def localName(self):
        try:
            return self._localName
        except AttributeError:
            self.setNamespaceLocalName()
            return self._localName

    @property
    def prefixedName(self):
        try:
            return self._prefixedName
        except AttributeError:
            self.setNamespaceLocalName()
            return self._prefixedName

    @property
    def namespaceURI(self):
        try:
            return self._namespaceURI
        except AttributeError:
            self.setNamespaceLocalName()
            return self._namespaceURI

    @property
    def elementNamespaceURI(self):
        try:
            return self._namespaceURI
        except AttributeError:
            self.setNamespaceLocalName()
            return self._namespaceURI

    @property
    def qname(self):
        try:
            return self._elementQname
        except AttributeError:
            self._elementQname = QName(self.prefix, self.namespaceURI, self.localName)
            return self._elementQname

    @property
    def elementQname(self):
        try:
            return self._elementQname
        except AttributeError:
            self._elementQname = qname(self)
            return self._elementQname

    def vQname(self, validationModelXbrl=None):
        if validationModelXbrl is not None and validationModelXbrl != self.modelXbrl:
            return self.elementQname
        return self.qname

    def elementDeclaration(self, validationModelXbrl=None):
        elementModelXbrl = self.modelXbrl
        if validationModelXbrl is not None and validationModelXbrl != elementModelXbrl:
            return validationModelXbrl.qnameConcepts.get(self.elementQname)
        return elementModelXbrl.qnameConcepts.get(self.qname)

    @property
    def parentQname(self):
        try:
            return self._parentQname
        except AttributeError:
            parentObj = self.getparent()
            self._parentQname = parentObj.elementQname if parentObj is not None else None
            return self._parentQname

    @property
    def id(self):
        return self.get('id')

    @property
    def stringValue(self):
        return ''.join(self._textNodes(recurse=True))

    @property
    def textValue(self):
        return ''.join(self._textNodes())

    def _textNodes(self, recurse=False):
        if self.text and getattr(self, 'xValid', 0) != VALID_NO_CONTENT:
            yield self.text
        for c in self.iterchildren():
            if recurse and isinstance(c, ModelObject):
                for nestedText in c._textNodes(recurse):
                    yield nestedText

            if c.tail and getattr(self, 'xValid', 0) != VALID_NO_CONTENT:
                yield c.tail

    @property
    def document(self):
        return self.modelDocument

    def prefixedNameQname(self, prefixedName):
        """Returns ModelValue.QName of prefixedName using this element and its ancestors' xmlns.
        
        :param prefixedName: A prefixed name string
        :type prefixedName: str
        :returns: QName -- the resolved prefixed name, or None if no prefixed name was provided
        """
        if prefixedName:
            return qnameEltPfxName(self, prefixedName)
        else:
            return

    @property
    def elementAttributesTuple(self):
        return tuple((name, value) for name, value in self.items())

    @property
    def elementAttributesStr(self):
        return ', '.join(["{0}='{1}'".format(name, value) for name, value in self.items()])

    def resolveUri(self, hrefObject=None, uri=None, dtsModelXbrl=None):
        """Returns the modelObject within modelDocment that resolves a URI based on arguments relative
        to this element
        
        :param hrefObject: an optional tuple of (hrefElement, modelDocument, id), or
        :param uri: An (element scheme pointer), and dtsModelXbrl (both required together if for a multi-instance href)
        :type uri: str
        :param dtsModelXbrl: DTS of href resolution (default is the element's own modelXbrl)
        :type dtsModelXbrl: ModelXbrl
        :returns: ModelObject -- Document node corresponding to the href or resolved uri
        """
        if dtsModelXbrl is None:
            dtsModelXbrl = self.modelXbrl
        doc = None
        if hrefObject:
            hrefElt, doc, id = hrefObject
        else:
            if uri:
                from arelle import UrlUtil
                url, id = UrlUtil.splitDecodeFragment(uri)
                if url == '':
                    doc = self.modelDocument
            else:
                normalizedUrl = self.modelXbrl.modelManager.cntlr.webCache.normalizeUrl(url, self.modelDocument.baseForElement(self))
                doc = dtsModelXbrl.urlDocs.get(normalizedUrl)
        from arelle import ModelDocument
        if isinstance(doc, ModelDocument.ModelDocument):
            if id is None:
                return doc
            if id in doc.idObjects:
                return doc.idObjects[id]
            from arelle.XmlUtil import xpointerElement
            xpointedElement = xpointerElement(doc, id)
            for docModelObject in doc.xmlRootElement.iter():
                if docModelObject == xpointedElement:
                    doc.idObjects[id] = docModelObject
                    return docModelObject

    def genLabel(self, role=None, fallbackToQname=False, fallbackToXlinkLabel=False, lang=None, strip=False, linkrole=None):
        from arelle import XbrlConst
        if role is None:
            role = XbrlConst.genStandardLabel
        if role == XbrlConst.conceptNameLabelRole:
            return str(self.qname)
        labelsRelationshipSet = self.modelXbrl.relationshipSet(XbrlConst.elementLabel, linkrole)
        if labelsRelationshipSet:
            label = labelsRelationshipSet.label(self, role, lang)
            if label is not None:
                if strip:
                    return label.strip()
                return Locale.rtlString(label, lang=lang)
        if fallbackToQname:
            return str(self.qname)
        else:
            if fallbackToXlinkLabel and hasattr(self, 'xlinkLabel'):
                return self.xlinkLabel
            return

    def viewText(self, labelrole=None, lang=None):
        return self.stringValue

    @property
    def propertyView(self):
        return (('QName', self.elementQname),) + tuple((XmlUtil.clarkNotationToPrefixedName(self, _tag, isAttribute=True), _value) for _tag, _value in self.items())

    def __repr__(self):
        return '{0}[{1}, {2} line {3})'.format(type(self).__name__, self.objectIndex, self.modelDocument.basename, self.sourceline)


from arelle.ModelValue import qname, qnameEltPfxName, QName

class ModelComment(etree.CommentBase):
    __doc__ = 'ModelConcept is a custom proxy objects for etree.\n    '

    def _init(self):
        self.isChanged = False
        parent = self.getparent()
        if parent is not None and hasattr(parent, 'modelDocument'):
            self.init(parent.modelDocument)

    def init(self, modelDocument):
        self.modelDocument = modelDocument


class ModelProcessingInstruction(etree.PIBase):
    __doc__ = 'ModelProcessingInstruction is a custom proxy object for etree.\n    '

    def _init(self):
        pass


class ModelAttribute:
    __doc__ = '\n    .. class:: ModelAttribute(modelElement, attrTag, xValid, xValue, sValue, text)\n    \n    ModelAttribute is a class of slot-based instances to store PSVI attribute values for each ModelObject\n    that has been validated.  It does not correspond to, or proxy, any lxml object.\n    \n    :param modelElement: owner element of attribute node\n    :type modelElement: ModelObject\n    :param attrTag: Clark notation attribute tag (from lxml)\n    :type attrTag: str\n    :param xValid: XmlValidation.py validation state enumeration\n    :param xValue: PSVI value (for formula processing)\n    :param sValue: s-equals value (for s-equality)\n    '
    __slots__ = ('modelElement', 'attrTag', 'xValid', 'xValue', 'sValue', 'text')

    def __init__(self, modelElement, attrTag, xValid, xValue, sValue, text):
        self.modelElement = modelElement
        self.attrTag = attrTag
        self.xValid = xValid
        self.xValue = xValue
        self.sValue = sValue
        self.text = text


class ObjectPropertyViewWrapper:
    __slots__ = ('modelObject', 'extraProperties')

    def __init__(self, modelObject, extraProperties=()):
        self.modelObject = modelObject
        self.extraProperties = extraProperties

    @property
    def propertyView(self):
        return self.modelObject.propertyView + self.extraProperties

    def __repr__(self):
        return 'objectPropertyViewWrapper({}, extraProperties={})'.format(self.modelObject, self.extraProperties)