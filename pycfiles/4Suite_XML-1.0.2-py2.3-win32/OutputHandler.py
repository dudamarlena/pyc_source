# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Ft\Xml\Xslt\OutputHandler.py
# Compiled at: 2006-08-22 11:28:12
"""
Manages XSLT output parameters governed by the xsl:output instruction
See also Ft.Xml.Xslt.OutputParameters

Copyright 2004 Fourthought, Inc. (USA).
Detailed license and copyright information: http://4suite.org/COPYRIGHT
Project home, documentation, distributions: http://4suite.org/
"""
from Ft.Xml import EMPTY_NAMESPACE
from Ft.Xml.Lib.XmlString import IsXmlSpace
from Ft.Xml.Xslt import NullWriter, PlainTextWriter, HtmlWriter, XmlWriter
from Ft.Xml.Xslt import XsltException, Error
from Ft.Xml.XPath import FT_EXT_NAMESPACE
_TEXT_METHOD = (
 EMPTY_NAMESPACE, 'text')
_HTML_METHOD = (EMPTY_NAMESPACE, 'html')
_XML_METHOD = (EMPTY_NAMESPACE, 'xml')
_XHTML_METHOD = (FT_EXT_NAMESPACE, 'xhtml')
_C14N_METHOD = (FT_EXT_NAMESPACE, 'c14n')

class OutputHandler(NullWriter.NullWriter):
    __module__ = __name__
    _methods = {_TEXT_METHOD: PlainTextWriter.PlainTextWriter, _HTML_METHOD: HtmlWriter.HtmlWriter, _XML_METHOD: XmlWriter.XmlWriter}

    def __init__(self, outputParams, stream, notifyFunc=None):
        NullWriter.NullWriter.__init__(self, outputParams)
        self._stream = stream
        self._stack = []
        return

    def _finalize(self, method):
        try:
            writerClass = self._methods[method]
        except KeyError:
            if method[0] is None:
                method = method[1]
            raise XsltException(Error.UNKNOWN_OUTPUT_METHOD, str(method))
        else:
            self._outputParams.setDefault('method', method)

        if writerClass is XmlWriter.XmlWriter and self._outputParams.cdataSectionElements:
            writerClass = XmlWriter.CdataSectionXmlWriter
        (stream, stack) = (self._stream, self._stack)
        del self._stream
        del self._stack
        self.__class__ = writerClass
        writerClass.__init__(self, self._outputParams, stream)
        self.startDocument()
        newline = 0
        for (cmd, args, kw) in stack:
            if newline:
                self.text('\n')
            else:
                newline = 1
            getattr(self, cmd)(*args, **kw)

        return
        return

    def getStream(self):
        return self._stream

    def getResult(self):
        return ''

    def startDocument(self):
        method = self._outputParams.method
        if method:
            self._finalize(method)
        return

    def endDocument(self, *args, **kw):
        self._stack.append(('endDocument', args, kw))
        self._finalize(_XML_METHOD)
        return

    def text(self, *args, **kw):
        self._stack.append(('text', args, kw))
        if not IsXmlSpace(args[0]):
            self._finalize(_XML_METHOD)
        return

    def processingInstruction(self, *args, **kw):
        self._stack.append(('processingInstruction', args, kw))
        return

    def comment(self, *args, **kw):
        self._stack.append(('comment', args, kw))
        return

    def startElement(self, name, namespace=None, *args, **kw):
        self._stack.append(('startElement', (name, namespace) + args, kw))
        if name.lower() == 'html' and namespace is EMPTY_NAMESPACE:
            self._finalize(_HTML_METHOD)
        else:
            self._finalize(_XML_METHOD)
        return