# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \Ft\Xml\Xslt\WhitespaceElements.py
# Compiled at: 2001-12-27 15:25:58
from Ft.Xml.Xslt import XsltElement, XsltException, Error, XSL_NAMESPACE
from Ft.Xml.Xslt import CategoryTypes
from Ft.Xml.Xslt import ContentInfo, AttributeInfo

class WhitespaceElement(XsltElement):
    __module__ = __name__
    category = CategoryTypes.TOP_LEVEL_ELEMENT
    content = ContentInfo.Empty
    legalAttrs = {'elements': AttributeInfo.Tokens(required=1)}
    _strip_whitespace = None

    def getWhitespaceInfo(self):
        return (
         self._strip_whitespace, self._elements)


class PreserveSpaceElement(WhitespaceElement):
    __module__ = __name__
    _strip_whitespace = 0


class StripSpaceElement(WhitespaceElement):
    __module__ = __name__
    _strip_whitespace = 1