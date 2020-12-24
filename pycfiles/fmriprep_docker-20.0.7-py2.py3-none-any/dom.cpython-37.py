# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-aejasjrz/pip/pip/_vendor/html5lib/treewalkers/dom.py
# Compiled at: 2020-05-05 12:41:47
# Size of source mod 2**32: 1413 bytes
from __future__ import absolute_import, division, unicode_literals
from xml.dom import Node
from . import base

class TreeWalker(base.NonRecursiveTreeWalker):

    def getNodeDetails(self, node):
        if node.nodeType == Node.DOCUMENT_TYPE_NODE:
            return (
             base.DOCTYPE, node.name, node.publicId, node.systemId)
        if node.nodeType in (Node.TEXT_NODE, Node.CDATA_SECTION_NODE):
            return (
             base.TEXT, node.nodeValue)
        if node.nodeType == Node.ELEMENT_NODE:
            attrs = {}
            for attr in list(node.attributes.keys()):
                attr = node.getAttributeNode(attr)
                if attr.namespaceURI:
                    attrs[(attr.namespaceURI, attr.localName)] = attr.value
                else:
                    attrs[(None, attr.name)] = attr.value

            return (
             base.ELEMENT, node.namespaceURI, node.nodeName,
             attrs, node.hasChildNodes())
        if node.nodeType == Node.COMMENT_NODE:
            return (
             base.COMMENT, node.nodeValue)
        if node.nodeType in (Node.DOCUMENT_NODE, Node.DOCUMENT_FRAGMENT_NODE):
            return (
             base.DOCUMENT,)
        return (
         base.UNKNOWN, node.nodeType)

    def getFirstChild(self, node):
        return node.firstChild

    def getNextSibling(self, node):
        return node.nextSibling

    def getParentNode(self, node):
        return node.parentNode