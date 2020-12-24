# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/xooof/xmlstruct/domutils.py
# Compiled at: 2008-10-01 10:41:00
from xml.dom.minidom import Node
from xml.sax.handler import feature_namespaces, feature_namespace_prefixes, property_dom_node, property_lexical_handler, property_declaration_handler
from xml.sax.xmlreader import XMLReader, AttributesImpl, AttributesNSImpl
XML_NAMESPACE = 'http://www.w3.org/XML/1998/namespace'
XMLNS_NAMESPACE = 'http://www.w3.org/2000/xmlns/'
XSI_NAMESPACE = 'http://www.w3.org/2001/XMLSchema-instance'
try:
    import xml.dom.ext.reader.Sax2

    def makeXmlDomGenerator(ownerDocument=None):
        handler = xml.dom.ext.reader.Sax2.XmlDomGenerator()
        handler.initState(ownerDoc=ownerDocument)
        return handler


except ImportError:
    _no_xmlplus = '_xmlplus package not installed'

    def makeXmlDomGenerator(ownerDocument=None):
        raise RuntimeError, _no_xmlplus


class DOMReader(XMLReader):
    __module__ = __name__

    def __init__(self):
        XMLReader.__init__(self)
        self.__parsing = 0
        self.__ns = 0
        self.__nspfx = 0
        self.__curNode = None
        self.__lex_handler = None
        self.__decl_handler = None
        return

    def setFeature(self, name, state):
        if name == feature_namespaces:
            if not self.__parsing:
                self.__ns = state
            else:
                raise RuntimeError, 'feature is readonly while parsing'
        elif name == feature_namespace_prefixes:
            if not self.__parsing:
                self.__nspfx = state
            else:
                raise RuntimeError, 'feature is readonly while parsing'
        else:
            XMLReader.setFeature(self, name, state)

    def getFeature(self, name):
        if name == feature_namespaces:
            return self.__ns
        elif name == feature_namespace_prefixes:
            return self.__nspfx
        else:
            XMLReader.getFeature(self, name)

    def setProperty(self, name, value):
        if name == property_dom_node:
            if not self.__parsing:
                self.__curNode = value
            else:
                raise RuntimeError, 'property is readonly while parsing'
        elif name == property_lexical_handler:
            self.__lex_handler = value
        elif name == property_declaration_handler:
            self.__decl_handler = value
        else:
            return XMLReader.setProperty(self, name, value)

    def getProperty(self, name):
        if name == property_dom_node:
            return self.__curNode
        elif name == property_lexical_handler:
            return self.__lex_handler
        elif name == property_declaration_handler:
            return self.__decl_handler
        else:
            return XMLReader.getProperty(self, name)

    def parse(self, node):
        self.__parsing = 1
        try:
            self._parse(node)
        finally:
            self.__parsing = 0

    def _parse(self, node):
        """Source must be a DOM node."""
        prevNode = self.__curNode
        try:
            self.__curNode = node
            if node.nodeType == Node.ELEMENT_NODE:
                if self.__ns:
                    attsNameValue = {}
                    attsNameQName = {}
                    prefixesToPop = []
                    for attNode in node.attributes.values():
                        if attNode.namespaceURI != XMLNS_NAMESPACE:
                            attsNameValue[(attNode.namespaceURI, attNode.localName)] = attNode.value
                            attsNameQName[(attNode.namespaceURI, attNode.localName)] = attNode.nodeName
                        else:
                            prefix = attNode.localName or None
                            prefixesToPop.append(prefix)
                            self._cont_handler.startPrefixMapping(prefix, attNode.value)

                    self._cont_handler.startElementNS((node.namespaceURI, node.localName), node.tagName, AttributesNSImpl(attsNameValue, attsNameQName))
                    for childNode in node.childNodes:
                        self._parse(childNode)

                    self._cont_handler.endElementNS((node.namespaceURI, node.localName), node.tagName)
                    for prefix in prefixesToPop:
                        self._cont_handler.endPrefixMapping(prefix)

                else:
                    attsNameValue = {}
                    for attNode in node.attributes.values():
                        attsNameValue[attNode.nodeName] = attNode.value

                    self._cont_handler.startElement(node.tagName, AttributesImpl(attsNameValue))
                    for childNode in node.childNodes:
                        self._parse(childNode)

                    self._cont_handler.endElement(node.tagName)
            elif node.nodeType == Node.ATTRIBUTE_NODE:
                raise RuntimeError, 'Cannot process attribute nodes'
            elif node.nodeType == Node.TEXT_NODE:
                self._cont_handler.characters(node.data)
            elif node.nodeType == Node.CDATA_SECTION_NODE:
                if self.__lex_handler:
                    self.__lex_handler.startCDATA()
                self._cont_handler.characters(node.data)
                if self.__lex_handler:
                    self.__lex_handler.endCDATA()
            elif node.nodeType == Node.PROCESSING_INSTRUCTION_NODE:
                self._cont_handler.processingInstruction(node.target, node.data)
            elif node.nodeType == Node.COMMENT_NODE:
                if self.__lex_handler:
                    self.__lex_handler.comment(node.data)
            elif node.nodeType == Node.DOCUMENT_NODE:
                self._cont_handler.startDocument()
                for childNode in node.childNodes:
                    self._parse(childNode)

                self._cont_handler.endDocument()
            elif node.nodeType == Node.DOCUMENT_FRAGMENT_NODE:
                for childNode in node.childNodes:
                    self._parse(childNode)

            else:
                raise RuntimeError, 'Not implemented: node type %s' % node.__class__
        finally:
            self.__curNode = prevNode
        return