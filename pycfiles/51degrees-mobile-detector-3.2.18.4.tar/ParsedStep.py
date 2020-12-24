# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \Ft\Xml\XPath\ParsedStep.py
# Compiled at: 2005-08-02 17:43:00
__doc__ = '\nA parsed token that represents a step.\n\nCopyright 2004 Fourthought, Inc. (USA).\nDetailed license and copyright information: http://4suite.org/COPYRIGHT\nProject home, documentation, distributions: http://4suite.org/\n'
from xml.dom import Node
from Ft.Xml.XPath import XPathTypes as Types

class ParsedStep:
    __module__ = __name__

    def __init__(self, axis, nodeTest, predicates=None):
        self._axis = axis
        self._nodeTest = nodeTest
        self._predicates = predicates
        return

    def evaluate(self, context):
        """
        Select a set of nodes from the axis, then filter through the node
        test and the predicates.
        """
        (node_set, reverse) = self._axis.select(context, self._nodeTest.match)
        if self._predicates and len(node_set):
            node_set = self._predicates.filter(node_set, context, reverse)
        return node_set

    select = evaluate

    def pprint(self, indent=''):
        print indent + str(self)
        self._axis.pprint(indent + '  ')
        self._nodeTest.pprint(indent + '  ')
        self._predicates and self._predicates.pprint(indent + '  ')

    def __str__(self):
        return '<Step at %x: %s>' % (id(self), repr(self))

    def __repr__(self):
        result = repr(self._axis) + '::' + repr(self._nodeTest)
        if self._predicates:
            result = result + repr(self._predicates)
        return result


class ParsedAbbreviatedStep:
    __module__ = __name__

    def __init__(self, parent):
        self.parent = parent

    def evaluate(self, context):
        if self.parent:
            if context.node.nodeType == Node.ATTRIBUTE_NODE:
                return [context.node.ownerElement]
            return context.node.parentNode and [context.node.parentNode] or []
        return [context.node]

    select = evaluate

    def pprint(self, indent=''):
        print indent + str(self)

    def __str__(self):
        return '<AbbreviatedStep at %x: %s>' % (id(self), repr(self))

    def __repr__(self):
        return self.parent and '..' or '.'


class ParsedNodeSetFunction:
    __module__ = __name__

    def __init__(self, function, predicates=None):
        self._function = function
        self._predicates = predicates
        return

    def evaluate(self, context):
        """
        Select a set of nodes from the node-set function then filter
        through the predicates.
        """
        nodeset = self._function.evaluate(context)
        if not isinstance(nodeset, Types.NodesetType):
            raise TypeError('%s must be a node-set, not a %s' % (repr(self._function),
             Types.g_xpathPrimitiveTypes.get(type(nodeset), type(nodeset).__name__)))
        if self._predicates and len(nodeset):
            reverse = 0
            nodeset = self._predicates.filter(nodeset, context, reverse)
        return nodeset

    select = evaluate

    def pprint(self, indent=''):
        print indent + str(self)
        self._function.pprint(indent + '  ')
        self._predicates and self._predicates.pprint(indent + '  ')

    def __str__(self):
        return '<Step at %x: %s>' % (id(self), repr(self))

    def __repr__(self):
        result = repr(self._function)
        if self._predicates:
            result = result + repr(self._predicates)
        return result