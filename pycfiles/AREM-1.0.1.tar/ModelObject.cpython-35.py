# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /tmp/pip-install-ncu5lfw4/arelle/arelle/ModelObject.py
# Compiled at: 2018-08-09 04:11:41
# Size of source mod 2**32: 15818 bytes
__doc__ = '\nCreated on Oct 5, 2010\nRefactored on Jun 11, 2011 to ModelDtsObject, ModelInstanceObject, ModelTestcaseObject\n\n@author: Mark V Systems Limited\n(c) Copyright 2010 Mark V Systems Limited, All rights reserved.\n'
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
    """ModelObject"""

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
        return (
         (
          'QName', self.elementQname),) + tuple((XmlUtil.clarkNotationToPrefixedName(self, _tag, isAttribute=True), _value) for _tag, _value in self.items())

    def __repr__(self):
        return '{0}[{1}, {2} line {3})'.format(type(self).__name__, self.objectIndex, self.modelDocument.basename, self.sourceline)


from arelle.ModelValue import qname, qnameEltPfxName, QName

class ModelComment(etree.CommentBase):
    """ModelComment"""

    def _init(self):
        self.isChanged = False
        parent = self.getparent()
        if parent is not None and hasattr(parent, 'modelDocument'):
            self.init(parent.modelDocument)

    def init(self, modelDocument):
        self.modelDocument = modelDocument


class ModelProcessingInstruction(etree.PIBase):
    """ModelProcessingInstruction"""

    def _init(self):
        pass


class ModelAttribute:
    """ModelAttribute"""
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