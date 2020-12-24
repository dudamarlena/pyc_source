# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \Ft\Xml\Lib\XmlPrettyPrinter.py
# Compiled at: 2005-02-09 04:11:13
__doc__ = '\nThis module supports formatted document serialization in XML syntax.\n\nCopyright 2005 Fourthought, Inc. (USA).\nDetailed license and copyright information: http://4suite.org/COPYRIGHT\nProject home, documentation, distributions: http://4suite.org/\n'
from XmlPrinter import XmlPrinter

class XmlPrettyPrinter(XmlPrinter):
    """
    An XmlPrettyPrinter instance provides functions for serializing an
    XML or XML-like document to a stream, based on SAX-like event calls
    initiated by an Ft.Xml.Lib.Print.PrintVisitor instance.

    The methods in this subclass of XmlPrinter produce the same output
    as the base class, but with extra whitespace added for visual
    formatting. The indent attribute is the string used for each level
    of indenting. It defaults to 2 spaces.
    """
    __module__ = __name__
    indent = '  '

    def __init__(self, stream, encoding):
        XmlPrinter.__init__(self, stream, encoding)
        self._level = 0
        self._canIndent = False
        return

    def startElement(self, namespaceUri, tagName, namespaces, attributes):
        if self._inElement:
            self.writeAscii('>')
            self._inElement = False
        if self._canIndent:
            self.writeAscii('\n' + self.indent * self._level)
        XmlPrinter.startElement(self, namespaceUri, tagName, namespaces, attributes)
        self._level += 1
        self._canIndent = True
        return

    def endElement(self, namespaceUri, tagName):
        self._level -= 1
        if self._canIndent and not self._inElement:
            self.writeAscii('\n' + self.indent * self._level)
        XmlPrinter.endElement(self, namespaceUri, tagName)
        self._canIndent = True
        return

    def text(self, data, disableEscaping=0):
        XmlPrinter.text(self, data, disableEscaping)
        self._canIndent = False
        return

    def cdataSection(self, data):
        XmlPrinter.cdataSection(self, data)
        self._canIndent = False
        return

    def processingInstruction(self, target, data):
        if self._inElement:
            self.writeAscii('>')
            self._inElement = False
        if self._canIndent:
            self.writeAscii('\n' + self.indent * self._level)
        XmlPrinter.processingInstruction(self, target, data)
        self._canIndent = True
        return

    def comment(self, data):
        if self._inElement:
            self.writeAscii('>')
            self._inElement = False
        if self._canIndent:
            self.writeAscii('\n' + self.indent * self._level)
        XmlPrinter.comment(self, data)
        self._canIndent = True
        return