# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \Ft\Xml\Xslt\DomWriter.py
# Compiled at: 2005-03-28 05:04:20
__doc__ = '\nDOM DocumentFragment writer for XSLT output\n\nMuch inspired by RtfWriter.\n\nCopyright (c) 2000-2001 Alexandre Fayolle (France).\n\nPermission to use, copy, modify, and distribute this software and its\ndocumentation for any purpose and without fee is hereby granted,\nprovided that the above copyright notice appear in all copies and that\nboth that copyright notice and this permission notice appear in\nsupporting documentation.\n\nTHIS PROGRAM IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED\nOR IMPLIED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF\nMERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.\n'
from xml.dom import Node
from Ft.Xml import XMLNS_NAMESPACE, EMPTY_NAMESPACE
from Ft.Xml.Domlette import implementation
from Ft.Xml.Lib.XmlString import SplitQName
from Ft.Xml.Xslt import NullWriter

class DomWriter(NullWriter.NullWriter):
    __module__ = __name__

    def __init__(self, ownerDoc=None, implementation=implementation, outputParams=None):
        """
        Note: if no ownerDoc, there is no way to set the document's base URI.
        """
        NullWriter.NullWriter.__init__(self)
        if not ownerDoc:
            ownerDoc = implementation.createDocument(None, None, None)
            self._root = ownerDoc
        else:
            self._root = ownerDoc.createDocumentFragment()
        self._ownerDoc = ownerDoc
        self._nodeStack = [self._root]
        self._currElement = None
        self._currText = ''
        return
        return

    def _completeTextNode(self):
        if self._currText and len(self._nodeStack) and self._nodeStack[(-1)].nodeType != Node.DOCUMENT_NODE:
            new_text = self._ownerDoc.createTextNode(self._currText)
            self._nodeStack[(-1)].appendChild(new_text)
        self._currText = ''
        return

    def getResult(self):
        self._completeTextNode()
        return self._root

    def startElement(self, name, namespace=EMPTY_NAMESPACE, extraNss=None):
        self._completeTextNode()
        new_element = self._ownerDoc.createElementNS(namespace, name)
        self._nodeStack.append(new_element)
        extraNss = extraNss or {}
        (prefix, localName) = SplitQName(name)
        for prefix in extraNss.keys():
            if prefix:
                new_element.setAttributeNS(XMLNS_NAMESPACE, 'xmlns:' + prefix, extraNss[prefix])
            else:
                new_element.setAttributeNS(XMLNS_NAMESPACE, 'xmlns', extraNss[None] or '')

        return
        return

    def endElement(self, name, namespace=EMPTY_NAMESPACE):
        self._completeTextNode()
        new_element = self._nodeStack[(-1)]
        del self._nodeStack[-1]
        self._nodeStack[(-1)].appendChild(new_element)
        return

    def text(self, text, escapeOutput=True):
        """
        The escapeOutput parameter is ignored
        """
        self._currText = self._currText + text
        return

    def attribute(self, name, value, namespace=EMPTY_NAMESPACE):
        if self._nodeStack[(-1)].nodeType == Node.ELEMENT_NODE:
            self._nodeStack[(-1)].setAttributeNS(namespace, name, value)
        return

    def processingInstruction(self, target, data):
        self._completeTextNode()
        pi = self._ownerDoc.createProcessingInstruction(target, data)
        self._nodeStack[(-1)].appendChild(pi)
        return

    def comment(self, text):
        self._completeTextNode()
        comment = self._ownerDoc.createComment(text)
        self._nodeStack[(-1)].appendChild(comment)
        return