# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \Ft\Xml\XPath\ParsedPredicateList.py
# Compiled at: 2005-08-02 17:43:00
__doc__ = '\nA parsed token that represents a predicate list.\n\nCopyright 2005 Fourthought, Inc. (USA).\nDetailed license and copyright information: http://4suite.org/COPYRIGHT\nProject home, documentation, distributions: http://4suite.org/\n'
from Ft.Lib import number
from Ft.Xml.XPath import Conversions
from Ft.Xml.XPath.XPathTypes import NumberTypes, g_xpathPrimitiveTypes
__all__ = [
 'ParsedPredicateList']

class ParsedPredicateList:
    __module__ = __name__

    def __init__(self, preds):
        if isinstance(preds, tuple):
            preds = list(preds)
        elif not isinstance(preds, list):
            raise TypeError('Invalid Predicates: %s' % str(preds))
        self._predicates = preds
        self._length = len(preds)

    def append(self, pred):
        self._predicates.append(pred)
        self._length += 1

    def filter(self, nodeList, context, reverse):
        if self._length:
            state = context.copy()
            for pred in self._predicates:
                size = len(nodeList)
                ctr = 0
                current = nodeList
                nodeList = []
                for node in current:
                    position = reverse and size - ctr or ctr + 1
                    (context.node, context.position, context.size) = (node, position, size)
                    res = pred.evaluate(context)
                    if type(res) in NumberTypes:
                        if not number.isnan(res) and res == position:
                            nodeList.append(node)
                    elif Conversions.BooleanValue(res):
                        nodeList.append(node)
                    ctr += 1

            context.set(state)
        return nodeList

    def __getitem__(self, index):
        return self._predicates[index]

    def __len__(self):
        return self._length

    def pprint(self, indent=''):
        print indent + str(self)
        for pred in self._predicates:
            pred.pprint(indent + '  ')

    def __str__(self):
        return '<PredicateList at %x: %s>' % (id(self), repr(self) or '(empty)')

    def __repr__(self):
        return reduce(lambda result, pred: result + '[%s]' % repr(pred), self._predicates, '')