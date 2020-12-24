# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Ft\Xml\Xslt\CopyElement.py
# Compiled at: 2006-07-29 13:08:55
"""
Implementation of the XSLT Spec copy stylesheet element.
WWW: http://4suite.org/4XSLT        e-mail: support@4suite.org

Copyright (c) 1999-2001 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.org/COPYRIGHT  for license and copyright information
"""
from xml.dom import Node
from Ft.Xml import XMLNS_NAMESPACE, EMPTY_NAMESPACE
from Ft.Xml.Xslt import XsltElement, XsltRuntimeException, Error, XSL_NAMESPACE
from Ft.Xml.Xslt import CategoryTypes, ContentInfo, AttributeInfo
from Ft.Xml.XPath import Conversions, NAMESPACE_NODE

class CopyElement(XsltElement):
    __module__ = __name__
    category = CategoryTypes.INSTRUCTION
    content = ContentInfo.Template
    legalAttrs = {'use-attribute-sets': AttributeInfo.QNames()}

    def instantiate(self, context, processor):
        context.processorNss = self.namespaces
        node = context.node
        if node.nodeType == Node.TEXT_NODE:
            processor.writers[(-1)].text(node.data)
        elif node.nodeType == Node.ELEMENT_NODE:
            extraNss = {}
            for ((namespace, local), attr) in node.attributes.items():
                if namespace == XMLNS_NAMESPACE:
                    extraNss[local] = attr.value

            processor.writers[(-1)].startElement(node.nodeName, node.namespaceURI, extraNss)
            for attr_set_name in self._use_attribute_sets:
                try:
                    attr_set = processor.attributeSets[attr_set_name]
                except KeyError:
                    raise XsltRuntimeException(Error.UNDEFINED_ATTRIBUTE_SET, self, attr_set_name)

                attr_set.instantiate(context, processor)

            for child in self.children:
                child.instantiate(context, processor)

            processor.writers[(-1)].endElement(node.nodeName, node.namespaceURI)
        elif node.nodeType == Node.DOCUMENT_NODE:
            for child in self.children:
                child.instantiate(context, processor)

        elif node.nodeType == Node.ATTRIBUTE_NODE:
            if node.namespaceURI != XMLNS_NAMESPACE:
                processor.writers[(-1)].attribute(node.nodeName, node.nodeValue, node.namespaceURI)
        elif node.nodeType == Node.PROCESSING_INSTRUCTION_NODE:
            processor.writers[(-1)].processingInstruction(node.target, node.data)
        elif node.nodeType == Node.COMMENT_NODE:
            processor.writers[(-1)].comment(node.data)
        elif node.nodeType == NAMESPACE_NODE:
            processor.writers[(-1)]._namespaces[(-1)][node.nodeName] = node.nodeValue
        else:
            raise Exception('Unknown Node Type %d' % node.nodeType)
        return