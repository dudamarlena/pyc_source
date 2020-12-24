# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Ft\Xml\Lib\XmlPrettyPrinter.py
# Compiled at: 2005-02-09 04:11:13
"""
This module supports formatted document serialization in XML syntax.

Copyright 2005 Fourthought, Inc. (USA).
Detailed license and copyright information: http://4suite.org/COPYRIGHT
Project home, documentation, distributions: http://4suite.org/
"""
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