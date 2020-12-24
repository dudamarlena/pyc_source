# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \Ft\Xml\XPath\ParsedAbbreviatedRelativeLocationPath.py
# Compiled at: 2005-08-02 17:43:00
__doc__ = '\nA parsed token that represents a abbreviated relative location path.\n\nCopyright 2005 Fourthought, Inc. (USA).\nDetailed license and copyright information: http://4suite.org/COPYRIGHT\nProject home, documentation, distributions: http://4suite.org/\n'
from xml.dom import Node
from Ft.Lib.Set import Unique
from Ft.Xml.XPath import XPathTypes as Types

class ParsedAbbreviatedRelativeLocationPath:
    __module__ = __name__

    def __init__(self, left, right):
        """
        left can be a step or a relative location path
        right is only a step
        """
        self._left = left
        self._right = right
        return

    def _descendants(self, context, nodeset):
        for child in context.node.childNodes:
            context.node = child
            results = self._right.select(context)
            if not isinstance(results, Types.NodesetType):
                raise TypeError('%r must be a node-set, not a %s' % (self._right,
                 Types.g_xpathPrimitiveTypes.get(type(results), type(results).__name__)))
            if results:
                nodeset.extend(results)
            if child.nodeType == Node.ELEMENT_NODE:
                nodeset = self._descendants(context, nodeset)

        return nodeset

    def evaluate(self, context):
        """Returns a node-set"""
        left = self._left.select(context)
        if not isinstance(left, Types.NodesetType):
            raise TypeError('%r must be a node-set, not a %s' % (self._left,
             Types.g_xpathPrimitiveTypes.get(type(left), type(left).__name__)))
        state = context.copy()
        results = []
        for node in left:
            context.node = node
            nodeset = self._right.select(context)
            if not isinstance(nodeset, Types.NodesetType):
                raise TypeError('%r must be a node-set, not a %s' % (self._right,
                 Types.g_xpathPrimitiveTypes.get(type(nodeset), type(nodeset).__name__)))
            results.extend(self._descendants(context, nodeset))

        results = Unique(results)
        context.set(state)
        return results

    select = evaluate

    def pprint(self, indent=''):
        print indent + str(self)
        self._left.pprint(indent + '  ')
        self._right.pprint(indent + '  ')

    def __str__(self):
        return '<AbbreviatedRelativeLocationPath at %x: %s>' % (id(self), repr(self))

    def __repr__(self):
        return repr(self._left) + '//' + repr(self._right)