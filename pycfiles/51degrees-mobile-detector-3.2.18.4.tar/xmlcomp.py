# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \Ft\Xml\ThirdParty\Xvif\xmlcomp.py
# Compiled at: 2004-10-12 17:59:14
from xml.dom import XMLNS_NAMESPACE
import xml.dom
from string import *

def normalize_space(s):
    st = 1
    r = ''
    for c in s:
        if c in (' ', '\n', '\t', '\r'):
            if st == 2:
                st = 3
        else:
            if st == 3:
                r += ' '
            r += c
            st = 2

    return r


class XmlComp:
    """A "checkType" can be a DOM nodeType, ie "An integer representing the 
    node type. Symbolic constants for the types are on the Node object: 
    ELEMENT_NODE, ATTRIBUTE_NODE, TEXT_NODE, CDATA_SECTION_NODE(**), ENTITY_NODE(*), 
    PROCESSING_INSTRUCTION_NODE(*), COMMENT_NODE(*), DOCUMENT_NODE(*), 
    DOCUMENT_TYPE_NODE(*), NOTATION_NODE(*)" or the extra values: 
    "NAMESPACE_PREFIX,WHITESPACES, NAMESPACE_DECLARATION".

    (*): not supported (yet)
    (**): use TEXT_NODE instead.

    """
    __module__ = __name__
    NAMESPACE_PREFIX = complex(0.0, 1.0)
    NAMESPACE_DECLARATION = complex(0.0, 2.0)
    WHITESPACES = complex(0.0, 3.0)
    EMPTY_TEXT = complex(0.0, 4.0)
    _default_checks = [
     xml.dom.Node.ELEMENT_NODE, xml.dom.Node.ATTRIBUTE_NODE, xml.dom.Node.TEXT_NODE, NAMESPACE_PREFIX, NAMESPACE_DECLARATION, WHITESPACES]

    def __init__(self, d1=None, d2=None, checks=_default_checks):
        if d1 != None:
            self.setDocument1(d1)
        if d2 != None:
            self.setDocument2(d2)
        self.checks = checks
        return

    def setDocument1(self, d1):
        self.d1 = d1

    def setDocument2(self, d2):
        self.d2 = d2

    def addCheck(self, check):
        if not check in self.checks:
            self.checks.append(check)

    def removeCheck(self, check):
        i = 0
        for c in self.checks:
            if c == check:
                del self.checks[i]
                break
            i += 1

    def compare(self, d1=None, d2=None):
        if d1 != None:
            self.setDocument1(d1)
        if d2 != None:
            self.setDocument2(d2)
        return self.compareNodes(d1.childNodes, d2.childNodes)
        return

    def compareNodes(self, nodes1, nodes2):
        n1 = self.removeJunk(nodes1)
        n2 = self.removeJunk(nodes2)
        i = 0
        for node in n1:
            if len(n2) == i:
                return 'node %s from document 1 has no match in document 2.' % node
            test = self.compareNode(node, n2[i])
            if test:
                return test
            i += 1

        if len(n2) > i:
            return 'node %s from document 2 has no match in document 1.' % n2[i]
        return None
        return

    def removeJunk(self, nodes):
        res = []
        for node in nodes:
            if node.nodeType in self.checks or node.nodeType == xml.dom.Node.CDATA_SECTION_NODE and xml.dom.Node.TEXT_NODE in self.checks:
                if node.nodeType in (xml.dom.Node.TEXT_NODE, xml.dom.Node.CDATA_SECTION_NODE):
                    t = normalize_space(node.nodeValue)
                    if not XmlComp.EMPTY_TEXT in self.checks and t == '':
                        continue
                    if not XmlComp.WHITESPACES in self.checks:
                        node = node.ownerDocument.createTextNode(t)
                    else:
                        node = node.ownerDocument.createTextNode(node.nodeValue)
                res.append(node)

        return res

    def removeJunkFromNamedNodeMap(self, nodes):
        res = {}
        for (ns, name) in nodes.keys():
            node = nodes[(ns, name)]
            if node.nodeType == xml.dom.Node.ATTRIBUTE_NODE and ns == xml.dom.XMLNS_NAMESPACE:
                if XmlComp.NAMESPACE_DECLARATION in self.checks:
                    res[(ns, name)] = node
            elif node.nodeType in self.checks:
                res[(ns, name)] = node

        return res

    def compareNode(self, n1, n2):
        if n1.nodeType == n2.nodeType:
            return self.compareFunctions[n1.nodeType](self, n1, n2)
        else:
            return 'Node types do not match (%s vs %s)' % (n1, n2)

    def compareElements(self, n1, n2):
        if n1.localName != n2.localName:
            return 'Element names do not match ({%s}%s vs {%s}%s)' % (n1.namespaceURI, n1.localName, n2.namespaceURI, n2.localName)
        if n1.namespaceURI != n2.namespaceURI:
            return 'Element names do not match ({%s}%s vs {%s}%s)' % (n1.namespaceURI, n1.localName, n2.namespaceURI, n2.localName)
        if self.NAMESPACE_PREFIX in self.checks and n1.prefix != n2.prefix:
            return 'Element prefixes names do not match ({%s|%s:}%s vs {%s|%s:}%s)' % (n1.namespaceURI, n1.prefix, n1.localName, n2.namespaceURI, n2.prefix, n2.localName)
        attCmp = self.compareNamedNodeMaps(n1.attributes, n2.attributes)
        if attCmp:
            return attCmp
        return self.compareNodes(n1.childNodes, n2.childNodes)

    def compareAttributes(self, n1, n2):
        if n1.localName != n2.localName:
            return 'Attribute names do not match ({%s}%s vs {%s}%s)' % (n1.namespaceURI, n1.localName, n2.namespaceURI, n2.localName)
        if n1.namespaceURI != n2.namespaceURI:
            return 'Attribute names do not match ({%s}%s vs {%s}%s)' % (n1.namespaceURI, n1.localName, n2.namespaceURI, n2.localName)
        if self.NAMESPACE_PREFIX in self.checks and n1.prefix != n2.prefix:
            return 'Attribute prefixes names do not match ({%s|%s:}%s vs {%s|%s:}%s)' % (n1.namespaceURI, n1.prefix, n1.localName, n2.namespaceURI, n2.prefix, n2.localName)
        if n1.nodeValue != n2.nodeValue:
            return "Attribute values do not match ({%s|%s:}%s='%s' vs {%s|%s:}%s='%s')" % (n1.namespaceURI, n1.prefix, n1.localName, n1.nodeValue, n2.namespaceURI, n2.prefix, n2.localName, n2.nodeValue)
        return None
        return

    def compareText(self, n1, n2):
        if n1.nodeValue != n2.nodeValue:
            return 'Text values do not match (%s vs %s)' % (n1.nodeValue, n2.nodeValue)
        return None
        return

    def compareNamedNodeMaps(self, nodes1, nodes2):
        n1 = self.removeJunkFromNamedNodeMap(nodes1)
        n2 = self.removeJunkFromNamedNodeMap(nodes2)
        i = 0
        for (ns, name) in n1.keys():
            if n2.has_key((ns, name)):
                test = self.compareNode(n1[(ns, name)], n2[(ns, name)])
                if test:
                    return test
                del n2[(ns, name)]
            else:
                return 'node %s from document 1 has no match in document 2.' % n1[(ns, name)]

        if len(n2) > 0:
            for key in n2.keys():
                return 'node {%s}%s from document 2 has no match in document 1.' % key

        return None
        return

    compareFunctions = {xml.dom.Node.ELEMENT_NODE: compareElements, xml.dom.Node.TEXT_NODE: compareText, xml.dom.Node.ATTRIBUTE_NODE: compareAttributes}