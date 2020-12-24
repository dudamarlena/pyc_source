# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \Ft\Xml\Xslt\ProcessingInstructionElement.py
# Compiled at: 2005-04-06 18:05:47
__doc__ = '\nImplementation of the XSLT Spec processing-instruction stylesheet element.\nWWW: http://4suite.org/4XSLT        e-mail: support@4suite.org\n\nCopyright (c) 1999-2001 Fourthought Inc, USA.   All Rights Reserved.\nSee  http://4suite.org/COPYRIGHT  for license and copyright information\n'
from Ft.Xml.Xslt import XsltElement, XsltRuntimeException, Error
from Ft.Xml.Xslt import CategoryTypes, ContentInfo, AttributeInfo

class ProcessingInstructionElement(XsltElement):
    __module__ = __name__
    category = CategoryTypes.INSTRUCTION
    content = ContentInfo.Template
    legalAttrs = {'name': AttributeInfo.NCNameAvt(required=1)}

    def instantiate(self, context, processor):
        context.processorNss = self.namespaces
        context.currentInstruction = self
        target = self._name.evaluate(context)
        if target.lower() == 'xml':
            raise XsltRuntimeException(Error.ILLEGAL_XML_PI, self)
        processor.pushResultString()
        had_nontext = 0
        try:
            for child in self.children:
                child.instantiate(context, processor)
                if processor.writers[(-1)].had_nontext:
                    had_nontext = 1

        finally:
            if had_nontext:
                raise XsltRuntimeException(Error.NONTEXT_IN_PI, self)
            content = processor.popResult()
        data = content.replace('?>', '? >')
        processor.writers[(-1)].processingInstruction(target, data)
        return