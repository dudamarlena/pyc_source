# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Ft\Xml\Xslt\IfElement.py
# Compiled at: 2005-04-06 18:05:47
"""
Implementation of the XSLT Spec if instruction
WWW: http://4suite.org/4XSLT        e-mail: support@4suite.org

Copyright (c) 1999-2001 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.org/COPYRIGHT  for license and copyright information
"""
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