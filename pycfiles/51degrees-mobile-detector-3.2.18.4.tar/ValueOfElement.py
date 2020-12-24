# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \Ft\Xml\Xslt\ValueOfElement.py
# Compiled at: 2005-04-06 18:05:47
__doc__ = '\nImplementation of the xsl:value-of element.\n\nCopyright 2005 Fourthought, Inc. (USA).\nDetailed license and copyright information: http://4suite.org/COPYRIGHT\nProject home, documentation, distributions: http://4suite.org/\n'
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