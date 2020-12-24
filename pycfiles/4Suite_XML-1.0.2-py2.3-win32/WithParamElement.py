# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Ft\Xml\Xslt\WithParamElement.py
# Compiled at: 2005-04-03 01:47:13
"""
Implementation of the XSLT Spec with-param stylesheet element.
WWW: http://4suite.org/4XSLT        e-mail: support@4suite.org

Copyright (c) 1999-2001 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.org/COPYRIGHT  for license and copyright information
"""
from Ft.Xml import EMPTY_NAMESPACE
from Ft.Xml.Xslt import XsltElement, XSL_NAMESPACE
from Ft.Xml.Xslt import AttributeInfo, ContentInfo
from Ft.Xml.Xslt.XPathExtensions import RtfExpr

class WithParamElement(XsltElement):
    __module__ = __name__
    category = None
    content = ContentInfo.Template
    legalAttrs = {'name': AttributeInfo.QName(required=1), 'select': AttributeInfo.Expression()}
    doesSetup = 1

    def setup(self):
        if not self._select:
            self._select = RtfExpr(self.children)
        return