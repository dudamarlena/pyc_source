# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Ft\Xml\XPath\ParsedRelativeLocationPath.py
# Compiled at: 2005-02-09 06:10:54
"""
A parsed token that represents a relative location path in the parsed result tree.
    
Copyright 2005 Fourthought, Inc. (USA).
Detailed license and copyright information: http://4suite.org/COPYRIGHT
Project home, documentation, distributions: http://4suite.org/
"""

class ParsedRelativeLocationPath:
    __module__ = __name__

    def __init__(self, left, right):
        self._left = left
        self._right = right
        return

    def evaluate(self, context):
        nodeset = self._left.select(context)
        state = context.copy()
        result = []
        size = len(nodeset)
        for pos in xrange(size):
            (context.node, context.position, context.size) = (
             nodeset[pos], pos + 1, size)
            result.extend(self._right.select(context))

        context.set(state)
        return result

    select = evaluate

    def pprint(self, indent=''):
        print indent + str(self)
        self._left.pprint(indent + '  ')
        self._right.pprint(indent + '  ')

    def __str__(self):
        return '<RelativeLocationPath at %x: %s>' % (id(self), repr(self))

    def __repr__(self):
        return repr(self._left) + '/' + repr(self._right)