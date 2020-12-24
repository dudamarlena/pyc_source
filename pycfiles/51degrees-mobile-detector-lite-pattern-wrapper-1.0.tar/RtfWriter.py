# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \Ft\Xml\Xslt\RtfWriter.py
# Compiled at: 2006-08-22 11:28:12
__doc__ = '\nResult Tree Fragment writer for XSLT output\n\nCopyright 2005 Fourthought, Inc. (USA).\nDetailed license and copyright information: http://4suite.org/COPYRIGHT\nProject home, documentation, distributions: http://4suite.org/\n'
from Ft.Xml import XMLNS_NAMESPACE, EMPTY_NAMESPACE
from Ft.Xml.Domlette import implementation, Text
from Ft.Xml.Xslt.NullWriter import NullWriter

class RtfWriter(NullWriter):
    """
    A special, simple writer for capturing result-tree fragments
    """
    __module__ = __name__

    def __init__(self, outputParams, baseUri, implementation=implementation):
        """
        Note: The implementation must support createRootNode(baseUri).
        """
        NullWriter.__init__(self, outputParams)
        self._document = implementation.createRootNode(baseUri)
        self._destination_node = self._document
        self._characterData = []
        self._escapeOutput = True
        return

    def __completeTextNode(self):
        if self._characterData:
            data = ('').join(self._characterData)
            if self._escapeOutput:
                text = self._document.createTextNode(data)
            else:
                text = _UnescapedText(self._document, data)
            self._destination_node.appendChild(text)
            del self._characterData[:]
        return

    def getResult(self):
        self.__completeTextNode()
        assert self._destination_node is self._document, "endElement not called (top of stack: '%s')" % self._destination_node.nodeName
        return self._document

    def startElement(self, name, namespace=EMPTY_NAMESPACE, extraNss=None):
        self.__completeTextNode()
        element = self._document.createElementNS(namespace, name)
        self._destination_node.appendChild(element)
        namespaces = extraNss or {}
        for (prefix, uri) in namespaces.items():
            if prefix:
                nodeName = 'xmlns:' + prefix
            elif not uri:
                continue
            else:
                nodeName = 'xmlns'
            element.setAttributeNS(XMLNS_NAMESPACE, nodeName, uri)

        self._destination_node = element
        return

    def endElement(self, name, namespace=EMPTY_NAMESPACE):
        self.__completeTextNode()
        assert name == self._destination_node.nodeName, 'nodeName mismatch for startElement/endElement'
        self._destination_node = self._destination_node.parentNode
        return

    def attribute(self, name, value, namespace=EMPTY_NAMESPACE):
        if self._destination_node.attributes is not None and not self._destination_node.childNodes:
            self._destination_node.setAttributeNS(namespace, name, value)
        return
        return

    def text(self, data, escapeOutput=True):
        if self._escapeOutput != escapeOutput:
            self.__completeTextNode()
            self._escapeOutput = escapeOutput
        self._characterData.append(data)
        return

    def processingInstruction(self, target, data):
        self.__completeTextNode()
        node = self._document.createProcessingInstruction(target, data)
        self._destination_node.appendChild(node)
        return

    def comment(self, data):
        self.__completeTextNode()
        node = self._document.createComment(data)
        self._destination_node.appendChild(node)
        return


class _UnescapedText(Text):
    __module__ = __name__
    xsltOutputEscaping = False