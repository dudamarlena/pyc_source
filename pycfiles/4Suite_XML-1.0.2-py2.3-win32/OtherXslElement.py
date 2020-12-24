# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Ft\Xml\Xslt\OtherXslElement.py
# Compiled at: 2006-01-12 23:26:09
"""
Non-template instructions from the XSLT spec
WWW: http://4suite.org/4XSLT        e-mail: support@4suite.org

Copyright (c) 1999-2001 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.org/COPYRIGHT  for license and copyright information
"""
from Ft.Xml import EMPTY_NAMESPACE
from Ft.Xml.Xslt import XsltElement, XsltException, Error, XSL_NAMESPACE
from Ft.Xml.Xslt import CategoryTypes, ContentInfo, AttributeInfo

class DecimalFormatElement(XsltElement):
    __module__ = __name__
    category = CategoryTypes.TOP_LEVEL_ELEMENT
    content = ContentInfo.Empty
    legalAttrs = {'name': AttributeInfo.QName(), 'decimal-separator': AttributeInfo.Char(default='.'), 'grouping-separator': AttributeInfo.Char(default=','), 'infinity': AttributeInfo.String(default='Infinity'), 'minus-sign': AttributeInfo.Char(default='-'), 'NaN': AttributeInfo.String(default='NaN'), 'percent': AttributeInfo.Char(default='%'), 'per-mille': AttributeInfo.Char(default=unichr(8240)), 'zero-digit': AttributeInfo.Char(default='0'), 'digit': AttributeInfo.Char(default='#'), 'pattern-separator': AttributeInfo.Char(default=';')}

    def getFormatInfo(self):
        format = (
         self._decimal_separator, self._grouping_separator, self._infinity, self._minus_sign, self._NaN, self._percent, self._per_mille, self._zero_digit, self._digit, self._pattern_separator)
        return (
         self._name, format)


class FallbackElement(XsltElement):
    __module__ = __name__
    category = CategoryTypes.INSTRUCTION
    content = ContentInfo.Template
    legalAttrs = {}

    def instantiate(self, context, processor):
        return


class ImportElement(XsltElement):
    __module__ = __name__
    category = None
    content = ContentInfo.Empty
    legalAttrs = {'href': AttributeInfo.UriReference(required=1)}


class IncludeElement(XsltElement):
    __module__ = __name__
    category = CategoryTypes.TOP_LEVEL_ELEMENT
    content = ContentInfo.Empty
    legalAttrs = {'href': AttributeInfo.UriReference(required=1)}


class KeyElement(XsltElement):
    __module__ = __name__
    category = CategoryTypes.TOP_LEVEL_ELEMENT
    content = ContentInfo.Empty
    legalAttrs = {'name': AttributeInfo.QName(required=1), 'match': AttributeInfo.Pattern(required=1), 'use': AttributeInfo.Expression(required=1)}

    def getKeyInfo(self):
        return (
         self._name, (self._match, self._use, self.namespaces))


class NamespaceAliasElement(XsltElement):
    __module__ = __name__
    category = CategoryTypes.TOP_LEVEL_ELEMENT
    content = ContentInfo.Empty
    legalAttrs = {'stylesheet-prefix': AttributeInfo.Prefix(required=1), 'result-prefix': AttributeInfo.Prefix(required=1)}


class OutputElement(XsltElement):
    __module__ = __name__
    category = CategoryTypes.TOP_LEVEL_ELEMENT
    content = ContentInfo.Empty
    legalAttrs = {'method': AttributeInfo.QName(), 'version': AttributeInfo.NMToken(), 'encoding': AttributeInfo.String(), 'omit-xml-declaration': AttributeInfo.YesNo(), 'standalone': AttributeInfo.YesNo(), 'doctype-public': AttributeInfo.String(), 'doctype-system': AttributeInfo.String(), 'cdata-section-elements': AttributeInfo.QNames(), 'indent': AttributeInfo.YesNo(), 'media-type': AttributeInfo.String(), 'f:utfbom': AttributeInfo.YesNo(default='no', description="Whether to force output of a byte order mark (BOM).  Usually used to generate a UTF-8 BOM.  Do not use unless you're sure you know what you're doing")}