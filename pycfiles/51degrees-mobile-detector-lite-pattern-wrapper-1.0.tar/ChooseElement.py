# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \Ft\Xml\Xslt\ChooseElement.py
# Compiled at: 2005-04-06 18:05:47
__doc__ = '\nImplementation of the XSLT Spec choose instruction\nWWW: http://4suite.org/4XSLT        e-mail: support@4suite.org\n\nCopyright (c) 1999-2001 Fourthought Inc, USA.   All Rights Reserved.\nSee  http://4suite.org/COPYRIGHT  for license and copyright information\n'
from Ft.Xml.Xslt import XsltElement, XsltException, Error, XSL_NAMESPACE
from Ft.Xml.Xslt import CategoryTypes
from Ft.Xml.Xslt import ContentInfo, AttributeInfo
from Ft.Xml.XPath import Conversions

class WhenElement(XsltElement):
    __module__ = __name__
    category = None
    content = ContentInfo.Template
    legalAttrs = {'test': AttributeInfo.BooleanExpression(required=1)}


class OtherwiseElement(XsltElement):
    __module__ = __name__
    category = None
    content = ContentInfo.Template
    legalAttrs = {}


class ChooseElement(XsltElement):
    __module__ = __name__
    category = CategoryTypes.INSTRUCTION
    content = ContentInfo.Seq(ContentInfo.Rep1(ContentInfo.QName(XSL_NAMESPACE, 'xsl:when')), ContentInfo.Opt(ContentInfo.QName(XSL_NAMESPACE, 'xsl:otherwise')))
    legalAttrs = {}
    doesSetup = 1

    def setup(self):
        if not self.children:
            raise XsltException(Error.CHOOSE_REQUIRES_WHEN)
        return

    def instantiate(self, context, processor):
        chosen = None
        for child in self.children:
            context.processorNss = child.namespaces
            context.currentInstruction = child
            if isinstance(child, WhenElement):
                if Conversions.BooleanValue(child._test.evaluate(context)):
                    chosen = child
                    break
            else:
                chosen = child

        if chosen:
            for child in chosen.children:
                child.instantiate(context, processor)

        return
        return