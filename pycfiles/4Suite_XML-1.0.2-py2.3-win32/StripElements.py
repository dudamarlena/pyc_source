# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Ft\Xml\Lib\StripElements.py
# Compiled at: 2005-05-07 21:49:18
from xml.dom import Node
from Ft.Xml import XML_NAMESPACE, EMPTY_NAMESPACE
from Ft.Xml.Lib.XmlString import IsXmlSpace

def StripElements(node, stripElements, stripState=0):
    if node.nodeType == Node.DOCUMENT_NODE:
        for c in node.childNodes:
            StripElements(c, stripElements, stripState)

    elif node.nodeType == Node.ELEMENT_NODE:
        if node.getAttributeNS(XML_NAMESPACE, 'space') == 'preserve':
            stripState = 0
        else:
            if node.getAttributeNS(XML_NAMESPACE, 'space'):
                stripState = 1
            for (uri, local, strip) in stripElements:
                if (uri, local) in [(node.namespaceURI, node.localName), (EMPTY_NAMESPACE, '*'), (node.namespaceURI, '*')]:
                    stripState = strip
                    break

        for c in node.childNodes:
            StripElements(c, stripElements, stripState)

    elif node.nodeType == Node.TEXT_NODE:
        if stripState and IsXmlSpace(node.data):
            node.parentNode.removeChild(node)