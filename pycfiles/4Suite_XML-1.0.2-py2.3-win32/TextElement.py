# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Ft\Xml\Xslt\TextElement.py
# Compiled at: 2005-04-06 18:05:47
"""
Implementation of the xsl:text element.

Copyright 2005 Fourthought, Inc. (USA).
Detailed license and copyright information: http://4suite.org/COPYRIGHT
Project home, documentation, distributions: http://4suite.org/
"""
from xml.dom import Node
from Ft.Xml import EMPTY_NAMESPACE
from Ft.Xml.Xslt import XsltElement, XsltException, Error, XSL_NAMESPACE
from Ft.Xml.Xslt import CategoryTypes, ContentInfo, AttributeInfo

class TextElement(XsltElement):
    __module__ = __name__
    category = CategoryTypes.INSTRUCTION
    content = ContentInfo.Text
    legalAttrs = {'disable-output-escaping': AttributeInfo.YesNo(default='no')}

    def instantiate(self, context, processor):
        if self.children:
            value = self.children[0].data
            if self._disable_output_escaping:
                processor.writers[(-1)].text(value, escapeOutput=False)
            else:
                processor.writers[(-1)].text(value)
        return