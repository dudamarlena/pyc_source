# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Ft\Xml\XPath\ParsedAbbreviatedAbsoluteLocationPath.py
# Compiled at: 2005-03-06 21:25:58
"""
A parsed token that represents an abbreviated absolute location path.

Copyright 2005 Fourthought, Inc. (USA).
Detailed license and copyright information: http://4suite.org/COPYRIGHT
Project home, documentation, distributions: http://4suite.org/
"""
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