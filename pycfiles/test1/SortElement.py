# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Ft\Xml\Xslt\SortElement.py
# Compiled at: 2005-02-09 06:21:20
"""
xsl:sort implementation
    
Copyright 2005 Fourthought, Inc. (USA).
Detailed license and copyright information: http://4suite.org/COPYRIGHT
Project home, documentation, distributions: http://4suite.org/
"""
from Ft.Lib import number
from Ft.Xml import EMPTY_NAMESPACE
from Ft.Xml.XPath import Conversions
from Ft.Xml.Xslt import XsltElement
from Ft.Xml.Xslt import CategoryTypes, ContentInfo, AttributeInfo

class SortElement(XsltElement):
    __module__ = __name__
    category = None
    content = ContentInfo.Empty
    legalAttrs = {'select': AttributeInfo.StringExpression(default='.'), 'lang': AttributeInfo.NMTokenAvt(), 'data-type': AttributeInfo.ChoiceAvt(['text', 'number'], default='text'), 'order': AttributeInfo.ChoiceAvt(['ascending', 'descending'], default='ascending'), 'case-order': AttributeInfo.ChoiceAvt(['upper-first', 'lower-first'])}
    doesSetup = 1

    def setup(self):
        if self._data_type.isConstant() and self._order.isConstant() and self._case_order.isConstant():
            self._comparer = self.makeComparer(self._order.evaluate(None), self._data_type.evaluate(None), self._case_order.evaluate(None))
        else:
            self._comparer = None
        return
        return

    def makeComparer(self, order, data_type, case_order):
        if data_type == 'number':
            comparer = FloatCompare
        elif case_order == 'lower-first':
            comparer = LowerFirstCompare
        elif case_order == 'upper-first':
            comparer = UpperFirstCompare
        else:
            comparer = cmp
        if order == 'descending':
            comparer = Descending(comparer)
        return comparer

    def getComparer(self, context):
        if self._comparer:
            return self._comparer
        data_type = self._data_type.evaluate(context)
        order = self._order.evaluate(context)
        case_order = self._case_order and self._case_order.evaluate(context)
        return self.makeComparer(order, data_type, case_order)

    def evaluate(self, context):
        return Conversions.StringValue(self._select.evaluate(context))


class Descending:
    __module__ = __name__

    def __init__(self, comparer):
        self.comparer = comparer

    def __call__(self, a, b):
        return self.comparer(b, a)


def FloatCompare(a, b):
    a = float(a or 0)
    b = float(b or 0)
    if number.isnan(a):
        if number.isnan(b):
            return 0
        else:
            return -1
    elif number.isnan(b):
        return 1
    return cmp(a, b)


def LowerFirstCompare(a, b):
    if a.lower() == b.lower():
        for i in xrange(len(a)):
            if a[i] != b[i]:
                return a[i].islower() and -1 or 1

        return 0
    else:
        return cmp(a, b)


def UpperFirstCompare(a, b):
    if a.lower() == b.lower():
        for i in xrange(len(a)):
            if a[i] != b[i]:
                return a[i].isupper() and -1 or 1

        return 0
    else:
        return cmp(a, b)