# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \Ft\Xml\Xslt\TextElement.py
# Compiled at: 2005-04-06 18:05:47
__doc__ = '\nImplementation of the xsl:text element.\n\nCopyright 2005 Fourthought, Inc. (USA).\nDetailed license and copyright information: http://4suite.org/COPYRIGHT\nProject home, documentation, distributions: http://4suite.org/\n'
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