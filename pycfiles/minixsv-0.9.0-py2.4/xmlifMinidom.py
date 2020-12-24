# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\genxmlif\xmlifMinidom.py
# Compiled at: 2008-08-08 10:48:20
import string, urllib
from xml.dom import Node, XMLNS_NAMESPACE
from xml.dom.expatbuilder import ExpatBuilderNS
from xml.parsers.expat import ExpatError
from genxmlif import XMLIF_MINIDOM, GenXmlIfError
from xmlifUtils import convertToAbsUrl, NsNameTupleFactory
from xmlifDom import XmlInterfaceDom, InternalDomTreeWrapper, InternalDomElementWrapper, XmlIfBuilderExtensionDom

class XmlInterfaceMinidom(XmlInterfaceDom):
    """Derived interface class for handling of minidom parser.
    
    For description of the interface methods see xmlifbase.py.
    """
    __module__ = __name__

    def __init__(self, verbose, useCaching, processXInclude):
        XmlInterfaceDom.__init__(self, verbose, useCaching, processXInclude)
        self.xmlIfType = XMLIF_MINIDOM
        if self.verbose:
            print 'Using minidom interface module...'

    def createXmlTree(self, namespace, xmlRootTagName, attributeDict={}, publicId=None, systemId=None):
        from xml.dom.minidom import getDOMImplementation
        domImpl = getDOMImplementation()
        doctype = domImpl.createDocumentType(xmlRootTagName, publicId, systemId)
        domTree = domImpl.createDocument(namespace, xmlRootTagName, doctype)
        treeWrapper = self.treeWrapperClass(self, InternalMinidomTreeWrapper(domTree), self.useCaching)
        intRootNodeWrapper = InternalMinidomElementWrapper(domTree.documentElement, treeWrapper.getTree())
        rootNodeWrapper = self.elementWrapperClass(intRootNodeWrapper, treeWrapper, [])
        for (attrName, attrValue) in attributeDict.items():
            rootNodeWrapper.setAttribute(attrName, attrValue)

        return treeWrapper

    def parse(self, file, baseUrl='', internalOwnerDoc=None):
        absUrl = convertToAbsUrl(file, baseUrl)
        fp = urllib.urlopen(absUrl)
        try:
            builder = ExtExpatBuilderNS(file, absUrl, self)
            tree = builder.parseFile(fp)
            if self.processXInclude:
                if internalOwnerDoc == None:
                    internalOwnerDoc = builder.treeWrapper.getTree()
                self.xInclude(builder.treeWrapper.getRootNode(), absUrl, internalOwnerDoc)
            fp.close()
        except ExpatError, errInst:
            fp.close()
            raise GenXmlIfError, '%s: ExpatError: %s' % (file, str(errInst))

        return builder.treeWrapper

    def parseString(self, text, baseUrl='', internalOwnerDoc=None):
        absUrl = convertToAbsUrl('', baseUrl)
        try:
            builder = ExtExpatBuilderNS('', absUrl, self)
            builder.parseString(text)
            if self.processXInclude:
                if internalOwnerDoc == None:
                    internalOwnerDoc = builder.treeWrapper.getTree()
                self.xInclude(builder.treeWrapper.getRootNode(), absUrl, internalOwnerDoc)
        except ExpatError, errInst:
            raise GenXmlIfError, '%s: ExpatError: %s' % (baseUrl, str(errInst))

        return builder.treeWrapper


class InternalMinidomTreeWrapper(InternalDomTreeWrapper):
    """Internal wrapper for a minidom Document class.
    """
    __module__ = __name__

    def __init__(self, document):
        InternalDomTreeWrapper.__init__(self, document)
        self.internalElementWrapperClass = InternalMinidomElementWrapper


class InternalMinidomElementWrapper(InternalDomElementWrapper):
    """Internal Wrapper for a Dom Element class.
    """
    __module__ = __name__

    def xmlIfExtGetAttributeDict(self):
        """Return a dictionary with all attributes of this element."""
        attribDict = {}
        for (attrNameNS, attrNodeOrValue) in self.element.attributes.itemsNS():
            attribDict[NsNameTupleFactory(attrNameNS)] = attrNodeOrValue

        return attribDict


class ExtExpatBuilderNS(ExpatBuilderNS, XmlIfBuilderExtensionDom):
    """Extended Expat Builder class derived from ExpatBuilderNS.
    
    Extended to store related line numbers, file/URL names and 
    defined namespaces in the node object.
    """
    __module__ = __name__

    def __init__(self, filePath, absUrl, xmlIf):
        ExpatBuilderNS.__init__(self)
        internalMinidomTreeWrapper = InternalMinidomTreeWrapper(self.document)
        self.treeWrapper = xmlIf.treeWrapperClass(self, internalMinidomTreeWrapper, xmlIf.useCaching)
        XmlIfBuilderExtensionDom.__init__(self, filePath, absUrl, self.treeWrapper, xmlIf.elementWrapperClass)
        self.getParser().EndNamespaceDeclHandler = self.end_namespace_decl_handler
        self.curNamespaces = []

    def start_element_handler(self, name, attributes):
        ExpatBuilderNS.start_element_handler(self, name, attributes)
        attrList = []
        for i in range(0, len(attributes), 2):
            attrName = attributes[i]
            attrNameSplit = string.split(attrName, ' ')
            if len(attrNameSplit) > 1:
                attrName = (
                 attrNameSplit[0], attrNameSplit[1])
            attrList.extend([attrName, attributes[(i + 1)]])

        internalMinidomElementWrapper = InternalMinidomElementWrapper(self.curNode, self.treeWrapper.getTree())
        XmlIfBuilderExtensionDom.startElementHandler(self, internalMinidomElementWrapper, self.getParser().ErrorLineNumber, self.curNamespaces[:], attrList)
        if self.curNode.parentNode.nodeType == Node.DOCUMENT_NODE:
            for namespace in self.curNamespaces:
                if namespace[0] != None:
                    internalMinidomElementWrapper.xmlIfExtElementWrapper.attributeSequence.append((XMLNS_NAMESPACE, namespace[0]))
                else:
                    internalMinidomElementWrapper.xmlIfExtElementWrapper.attributeSequence.append('xmlns')

        return

    def end_element_handler(self, name):
        XmlIfBuilderExtensionDom.endElementHandler(self, self.curNode.xmlIfExtInternalWrapper, self.getParser().ErrorLineNumber)
        ExpatBuilderNS.end_element_handler(self, name)

    def start_namespace_decl_handler(self, prefix, uri):
        ExpatBuilderNS.start_namespace_decl_handler(self, prefix, uri)
        self.curNamespaces.insert(0, (prefix, uri))

    def end_namespace_decl_handler(self, prefix):
        assert self.curNamespaces.pop(0)[0] == prefix, 'implementation confused'