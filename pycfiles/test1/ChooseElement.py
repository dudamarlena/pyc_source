# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Ft\Xml\Xslt\ChooseElement.py
# Compiled at: 2005-04-06 18:05:47
"""
Implementation of the XSLT Spec choose instruction
WWW: http://4suite.org/4XSLT        e-mail: support@4suite.org

Copyright (c) 1999-2001 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.org/COPYRIGHT  for license and copyright information
"""
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