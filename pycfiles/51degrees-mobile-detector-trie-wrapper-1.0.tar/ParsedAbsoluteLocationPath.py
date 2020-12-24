# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \Ft\Xml\XPath\ParsedAbsoluteLocationPath.py
# Compiled at: 2003-01-19 00:08:29
__doc__ = '\nA Parsed Token that represents a absolute location path in the parsed tree.\nWWW: http://4suite.org/XPATH        e-mail: support@4suite.org\n\nCopyright (c) 2000-2001 Fourthought Inc, USA.   All Rights Reserved.\nSee  http://4suite.org/COPYRIGHT  for license and copyright information\n'

class ParsedAbsoluteLocationPath:
    __module__ = __name__

    def __init__(self, child):
        self._child = child

    def evaluate(self, context):
        root = context.node.rootNode
        if self._child is None:
            return [root]
        state = context.copy()
        (context.node, context.position, context.size) = (
         root, 1, 1)
        nodeset = self._child.select(context)
        context.set(state)
        return nodeset
        return

    select = evaluate

    def pprint(self, indent=''):
        print indent + str(self)
        self._child and self._child.pprint(indent + '  ')

    def __str__(self):
        return '<AbsoluteLocationPath at %x: %s>' % (id(self), repr(self))

    def __repr__(self):
        return '/' + (self._child and repr(self._child) or '')