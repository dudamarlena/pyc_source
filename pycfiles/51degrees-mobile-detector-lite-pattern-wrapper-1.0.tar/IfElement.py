# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \Ft\Xml\Xslt\IfElement.py
# Compiled at: 2005-04-06 18:05:47
__doc__ = '\nImplementation of the XSLT Spec if instruction\nWWW: http://4suite.org/4XSLT        e-mail: support@4suite.org\n\nCopyright (c) 1999-2001 Fourthought Inc, USA.   All Rights Reserved.\nSee  http://4suite.org/COPYRIGHT  for license and copyright information\n'
from Ft.Xml.Xslt import XsltElement, XSL_NAMESPACE
from Ft.Xml.XPath import Conversions
from Ft.Xml.Xslt import CategoryTypes
from Ft.Xml.Xslt import ContentInfo, AttributeInfo

class IfElement(XsltElement):
    __module__ = __name__
    category = CategoryTypes.INSTRUCTION
    content = ContentInfo.Template
    legalAttrs = {'test': AttributeInfo.BooleanExpression(required=1)}

    def instantiate(self, context, processor, new_level=1):
        context.processorNss = self.namespaces
        context.currentInstruction = self
        if Conversions.BooleanValue(self._test.evaluate(context)):
            for child in self.children:
                child.instantiate(context, processor)

        return