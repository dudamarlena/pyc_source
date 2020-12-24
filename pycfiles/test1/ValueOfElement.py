# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Ft\Xml\Xslt\ValueOfElement.py
# Compiled at: 2005-04-06 18:05:47
"""
Implementation of the xsl:value-of element.

Copyright 2005 Fourthought, Inc. (USA).
Detailed license and copyright information: http://4suite.org/COPYRIGHT
Project home, documentation, distributions: http://4suite.org/
"""
from Ft.Xml.Xslt import XsltElement
from Ft.Xml.Xslt import CategoryTypes, ContentInfo, AttributeInfo
from Ft.Xml.XPath import Conversions

class ValueOfElement(XsltElement):
    __module__ = __name__
    category = CategoryTypes.INSTRUCTION
    content = ContentInfo.Empty
    legalAttrs = {'select': AttributeInfo.StringExpression(required=1), 'disable-output-escaping': AttributeInfo.YesNo(default='no')}

    def instantiate(self, context, processor):
        context.processorNss = self.namespaces
        context.currentInstruction = self
        text = Conversions.StringValue(self._select.evaluate(context))
        if text:
            if self._disable_output_escaping:
                processor.writers[(-1)].text(text, escapeOutput=False)
            else:
                processor.writers[(-1)].text(text)
        return