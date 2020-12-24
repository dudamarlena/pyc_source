# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Ft\Xml\Xslt\ApplyImportsElement.py
# Compiled at: 2005-04-06 18:05:47
"""
Implementation of the XSLT Spec apply-imports stylesheet element.
WWW: http://4suite.org/4XSLT        e-mail: support@4suite.org

Copyright (c) 1999-2001 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.org/COPYRIGHT  for license and copyright information
"""
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