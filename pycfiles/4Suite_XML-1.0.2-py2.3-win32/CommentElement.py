# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Ft\Xml\Xslt\CommentElement.py
# Compiled at: 2006-12-10 21:49:28
"""
xsl:comment instruction implementation

Copyright 2006 Fourthought, Inc. (USA).
Detailed license and copyright information: http://4suite.org/COPYRIGHT
Project home, documentation, distributions: http://4suite.org/
"""
from Ft.Xml.Xslt import XSL_NAMESPACE, XsltElement
from Ft.Xml.Xslt import XsltRuntimeException, Error
from Ft.Xml.Xslt import CategoryTypes, ContentInfo

class CommentElement(XsltElement):
    __module__ = __name__
    category = CategoryTypes.INSTRUCTION
    content = ContentInfo.Template
    legalAttrs = {}

    def instantiate(self, context, processor):
        context.processorNss = self.namespaces
        context.currentInstruction = self
        processor.pushResultString()
        had_nontext = 0
        try:
            for child in self.children:
                child.instantiate(context, processor)
                if processor.writers[(-1)].had_nontext:
                    had_nontext = 1

        finally:
            if had_nontext:
                raise XsltRuntimeException(Error.NONTEXT_IN_COMMENT, self)
            content = processor.popResult()
        content = content.replace('--', '- -')
        if content[-1:] == '-':
            content += ' '
        processor.writers[(-1)].comment(content)
        return