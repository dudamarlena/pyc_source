# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Ft\Xml\Lib\HtmlPrettyPrinter.py
# Compiled at: 2005-02-09 04:12:06
"""
This module supports formatted document serialization in HTML syntax.

Copyright 2005 Fourthought, Inc. (USA).
Detailed license and copyright information: http://4suite.org/COPYRIGHT
Project home, documentation, distributions: http://4suite.org/
"""
from Ft.Xml import EMPTY_NAMESPACE
from HtmlPrinter import HtmlPrinter

class HtmlPrettyPrinter(HtmlPrinter):
    """
    An HtmlPrettyPrinter instance provides functions for serializing an
    XML or XML-like document to a stream, based on SAX-like event calls
    initiated by an Ft.Xml.Lib.Print.PrintVisitor instance.

    The methods in this subclass of HtmlPrinter attempt to emit a
    document conformant to the HTML 4.01 syntax, with extra whitespace
    added for visual formatting. The indent attribute is the string used
    for each level of indenting. It defaults to 2 spaces.
    """
    __module__ = __name__
    indent = '  '

    def __init__(self, stream, encoding):
        HtmlPrinter.__init__(self, stream, encoding)
        self._level = 0
        self._isInline = [
         1]
        self._inNoIndent = [0]
        self._indentForbidden = 0
        self._indentEndTag = False
        return

    def startElement(self, namespaceUri, tagName, namespaces, attributes):
        if self._inElement:
            self.writeAscii('>')
            self._inElement = False
        key = (
         namespaceUri, tagName.lower())
        inline = key in self.inlineElements
        if not inline and not self._isInline[(-1)] and not self._indentForbidden:
            self.writeAscii('\n' + self.indent * self._level)
        HtmlPrinter.startElement(self, namespaceUri, tagName, namespaces, attributes)
        self._isInline.append(inline)
        self._inNoIndent.append(key in self.noIndentElements)
        self._indentForbidden += self._inNoIndent[(-1)]
        self._level += 1
        self._indentEndTag = False
        return

    def endElement(self, namespaceUri, tagName):
        self._level -= 1
        inline = self._isInline.pop()
        if self._inElement:
            self.writeAscii('/>')
            self._inElement = False
        else:
            if not inline and not self._indentForbidden and self._indentEndTag:
                self.writeAscii('\n' + self.indent * self._level)
            HtmlPrinter.endElement(self, namespaceUri, tagName)
        self._indentForbidden -= self._inNoIndent.pop()
        self._indentEndTag = not inline
        return

    def processingInstruction(self, target, data):
        if self._inElement:
            self.writeAscii('>')
            self._inElement = False
        self._indentEndTag = True
        if not self._isInline[(-1)] and not self._indentForbidden:
            self.writeAscii('\n' + self.indent * self._level)
        HtmlPrinter.processingInstruction(self, target, data)
        return

    def comment(self, data):
        if self._inElement:
            self.writeAscii('>')
            self._inElement = False
        self._indentEndTag = True
        if not self._isInline[(-1)] and not self._indentForbidden:
            self.writeAscii('\n' + self.indent * self._level)
        HtmlPrinter.comment(self, data)
        return

    inlineElements = {}
    for name in ['tt', 'i', 'b', 'u', 's', 'strike', 'big', 'small', 'em', 'strong', 'dfn', 'code', 'samp', 'kbd', 'var', 'cite', 'abbr', 'acronym', 'a', 'img', 'applet', 'object', 'font', 'basefont', 'script', 'map', 'q', 'sub', 'sup', 'span', 'bdo', 'iframe', 'input', 'select', 'textarea', 'label', 'button']:
        inlineElements[(EMPTY_NAMESPACE, name)] = True

    noIndentElements = {}
    for name in ['script', 'style', 'pre', 'textarea', 'xmp']:
        noIndentElements[(EMPTY_NAMESPACE, name)] = True

    del name