# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \Ft\Xml\Xslt\CommentElement.py
# Compiled at: 2006-12-10 21:49:28
__doc__ = '\nxsl:comment instruction implementation\n\nCopyright 2006 Fourthought, Inc. (USA).\nDetailed license and copyright information: http://4suite.org/COPYRIGHT\nProject home, documentation, distributions: http://4suite.org/\n'
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