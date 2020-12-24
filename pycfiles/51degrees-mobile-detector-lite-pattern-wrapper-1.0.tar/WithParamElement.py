# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \Ft\Xml\Xslt\WithParamElement.py
# Compiled at: 2005-04-03 02:47:13
__doc__ = '\nImplementation of the XSLT Spec with-param stylesheet element.\nWWW: http://4suite.org/4XSLT        e-mail: support@4suite.org\n\nCopyright (c) 1999-2001 Fourthought Inc, USA.   All Rights Reserved.\nSee  http://4suite.org/COPYRIGHT  for license and copyright information\n'
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