# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \Ft\Xml\XPath\ParsedAbbreviatedAbsoluteLocationPath.py
# Compiled at: 2005-03-06 21:25:58
__doc__ = '\nA parsed token that represents an abbreviated absolute location path.\n\nCopyright 2005 Fourthought, Inc. (USA).\nDetailed license and copyright information: http://4suite.org/COPYRIGHT\nProject home, documentation, distributions: http://4suite.org/\n'
from xml.dom import Node
from Ft.Lib.Set import Unique

class ParsedAbbreviatedAbsoluteLocationPath:
    __module__ = __name__

    def __init__(self, rel):
        self._rel = rel
        return

    def _descendants(self, context, nodeset):
        for child in context.node.childNodes:
            context.node = child
            results = self._rel.select(context)
            if results:
                nodeset.extend(results)
                nodeset = Unique(nodeset)
            if child.nodeType == Node.ELEMENT_NODE:
                nodeset = self._descendants(context, nodeset)

        return nodeset

    def evaluate(self, context):
        state = context.copy()
        context.node = context.node.rootNode
        nodeset = self._descendants(context, self._rel.select(context))
        context.set(state)
        return nodeset

    select = evaluate

    def pprint(self, indent=''):
        print indent + str(self)
        self._rel.pprint(indent + '  ')

    def __str__(self):
        return '<AbbreviatedAbsoluteLocationPath at %x: %s>' % (id(self), repr(self))

    def __repr__(self):
        return '//%r' % self._rel