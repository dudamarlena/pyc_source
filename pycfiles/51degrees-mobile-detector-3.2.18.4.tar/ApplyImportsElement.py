# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \Ft\Xml\Xslt\ApplyImportsElement.py
# Compiled at: 2005-04-06 18:05:47
__doc__ = '\nImplementation of the XSLT Spec apply-imports stylesheet element.\nWWW: http://4suite.org/4XSLT        e-mail: support@4suite.org\n\nCopyright (c) 1999-2001 Fourthought Inc, USA.   All Rights Reserved.\nSee  http://4suite.org/COPYRIGHT  for license and copyright information\n'
from Ft.Xml.Xslt import XsltElement, XSL_NAMESPACE, XsltRuntimeException, Error
from Ft.Xml.Xslt import CategoryTypes, AttributeInfo, ContentInfo

class ApplyImportsElement(XsltElement):
    __module__ = __name__
    category = CategoryTypes.INSTRUCTION
    content = ContentInfo.Empty
    legalAttrs = {}

    def instantiate(self, context, processor):
        if not context.stylesheet:
            raise XsltRuntimeException(Error.APPLYIMPORTS_WITH_NULL_CURRENT_TEMPLATE, self)
        context.stylesheet.applyTemplates(context, processor, maxImport=self.importIndex)
        return