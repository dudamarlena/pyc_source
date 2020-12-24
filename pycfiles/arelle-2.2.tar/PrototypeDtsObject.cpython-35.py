# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-ncu5lfw4/arelle/arelle/PrototypeDtsObject.py
# Compiled at: 2018-08-09 04:11:41
# Size of source mod 2**32: 7318 bytes
from arelle import XmlUtil, XbrlConst
from arelle.ModelValue import QName
from arelle.XmlValidate import VALID
from collections import defaultdict
import decimal, os
ModelDocument = None

class PrototypeObject:

    def __init__(self, modelDocument, sourceElement=None):
        self.modelDocument = modelDocument
        self.sourceElement = sourceElement
        self.attributes = {}

    @property
    def sourceline(self):
        if self.sourceElement is not None:
            return self.sourceElement.sourceline

    def get(self, key, default=None):
        return self.attributes.get(key, default)

    def itersiblings(self, **kwargs):
        """Method proxy for itersiblings() of lxml arc element"""
        if self.sourceElement is not None:
            return self.sourceElement.itersiblings(**kwargs)
        return ()

    def getparent(self):
        """(_ElementBase) -- Method proxy for getparent() of lxml arc element"""
        if self.sourceElement is not None:
            return self.sourceElement.getparent()


class LinkPrototype(PrototypeObject):

    def __init__(self, modelDocument, parent, qname, role, sourceElement=None):
        super(LinkPrototype, self).__init__(modelDocument, sourceElement)
        self._parent = parent
        self.modelXbrl = modelDocument.modelXbrl
        self.qname = self.elementQname = qname
        self.namespaceURI = qname.namespaceURI
        self.localName = qname.localName
        self.role = role
        self.childElements = []
        self.text = self.textValue = None
        self.attributes = {'{http://www.w3.org/1999/xlink}type': 'extended'}
        if role:
            self.attributes['{http://www.w3.org/1999/xlink}role'] = role
        self.labeledResources = defaultdict(list)

    def clear(self):
        self.__dict__.clear()

    def __iter__(self):
        return iter(self.childElements)

    def getparent(self):
        return self._parent

    def iterchildren(self):
        return iter(self.childElements)

    def __getitem(self, key):
        return self.attributes[key]


class LocPrototype(PrototypeObject):

    def __init__(self, modelDocument, parent, label, locObject, role=None, sourceElement=None):
        super(LocPrototype, self).__init__(modelDocument, sourceElement)
        self._parent = parent
        self.modelXbrl = modelDocument.modelXbrl
        self.qname = self.elementQname = XbrlConst.qnLinkLoc
        self.namespaceURI = self.qname.namespaceURI
        self.localName = self.qname.localName
        self.text = self.textValue = None
        self.attributes = {'{http://www.w3.org/1999/xlink}type': 'locator', 
         '{http://www.w3.org/1999/xlink}label': label}
        if isinstance(locObject, _STR_BASE):
            self.attributes['{http://www.w3.org/1999/xlink}href'] = '#' + locObject
        if role:
            self.attributes['{http://www.w3.org/1999/xlink}role'] = role
        self.locObject = locObject

    def clear(self):
        self.__dict__.clear()

    @property
    def xlinkLabel(self):
        return self.attributes.get('{http://www.w3.org/1999/xlink}label')

    def dereference(self):
        if isinstance(self.locObject, _STR_BASE):
            return self.modelDocument.idObjects.get(self.locObject, None)
        else:
            return self.locObject

    def getparent(self):
        return self._parent

    def get(self, key, default=None):
        return self.attributes.get(key, default)

    def __getitem(self, key):
        return self.attributes[key]


class ArcPrototype(PrototypeObject):

    def __init__(self, modelDocument, parent, qname, fromLabel, toLabel, linkrole, arcrole, order='1', sourceElement=None):
        super(ArcPrototype, self).__init__(modelDocument, sourceElement)
        self._parent = parent
        self.modelXbrl = modelDocument.modelXbrl
        self.qname = self.elementQname = qname
        self.namespaceURI = qname.namespaceURI
        self.localName = qname.localName
        self.linkrole = linkrole
        self.arcrole = arcrole
        self.order = order
        self.text = self.textValue = None
        self.attributes = {'{http://www.w3.org/1999/xlink}type': 'arc', 
         '{http://www.w3.org/1999/xlink}from': fromLabel, 
         '{http://www.w3.org/1999/xlink}to': toLabel, 
         '{http://www.w3.org/1999/xlink}arcrole': arcrole}
        self.xValid = VALID
        self.xValue = self.sValue = None
        self.xAttributes = {}

    @property
    def orderDecimal(self):
        return decimal.Decimal(self.order)

    def clear(self):
        self.__dict__.clear()

    @property
    def arcElement(self):
        if self.sourceElement is not None:
            return self.sourceElement

    def getparent(self):
        return self._parent

    def get(self, key, default=None):
        return self.attributes.get(key, default)

    def items(self):
        return self.attributes.items()

    def __getitem(self, key):
        return self.attributes[key]


class DocumentPrototype:

    def __init__(self, modelXbrl, uri, base=None, referringElement=None, isEntry=False, isDiscovered=False, isIncluded=None, namespace=None, reloadCache=False, **kwargs):
        global ModelDocument
        if ModelDocument is None:
            from arelle import ModelDocument
        self.modelXbrl = modelXbrl
        self.skipDTS = modelXbrl.skipDTS
        self.modelDocument = self
        if referringElement is not None:
            if referringElement.localName == 'schemaRef':
                self.type = ModelDocument.Type.SCHEMA
            else:
                if referringElement.localName == 'linkbaseRef':
                    self.type = ModelDocument.Type.LINKBASE
                else:
                    self.type = ModelDocument.Type.UnknownXML
        else:
            self.type = ModelDocument.Type.UnknownXML
        normalizedUri = modelXbrl.modelManager.cntlr.webCache.normalizeUrl(uri, base)
        self.filepath = modelXbrl.modelManager.cntlr.webCache.getfilename(normalizedUri, filenameOnly=True)
        self.uri = modelXbrl.modelManager.cntlr.webCache.normalizeUrl(self.filepath)
        self.basename = os.path.basename(self.filepath)
        self.targetNamespace = None
        self.referencesDocument = {}
        self.hrefObjects = []
        self.schemaLocationElements = set()
        self.referencedNamespaces = set()
        self.inDTS = False
        self.xmlRootElement = None

    def clear(self):
        self.__dict__.clear()