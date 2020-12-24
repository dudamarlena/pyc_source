# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \Ft\Xml\XPath\ParsedRelativeLocationPath.py
# Compiled at: 2005-02-09 06:10:54
__doc__ = '\nA parsed token that represents a relative location path in the parsed result tree.\n    \nCopyright 2005 Fourthought, Inc. (USA).\nDetailed license and copyright information: http://4suite.org/COPYRIGHT\nProject home, documentation, distributions: http://4suite.org/\n'

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