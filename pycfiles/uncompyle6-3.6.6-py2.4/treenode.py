# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/uncompyle6/parsers/treenode.py
# Compiled at: 2020-04-20 22:50:15
import sys
from uncompyle6 import PYTHON3
from uncompyle6.scanners.tok import NoneToken
from spark_parser.ast import AST as spark_AST
if PYTHON3:
    intern = sys.intern

class SyntaxTree(spark_AST):
    __module__ = __name__

    def __init__(self, *args, **kwargs):
        spark_AST.__init__(self, *args, **kwargs)
        self.transformed_by = None
        return

    def isNone(self):
        """An SyntaxTree None token. We can't use regular list comparisons
        because SyntaxTree token offsets might be different"""
        return len(self.data) == 1 and NoneToken == self.data[0]

    def __repr__(self):
        return self.__repr1__('', None)

    def __repr1__(self, indent, sibNum=None):
        rv = str(self.kind)
        if sibNum is not None:
            rv = '%2d. %s' % (sibNum, rv)
        enumerate_children = False
        if len(self) > 1:
            rv += ' (%d)' % len(self)
            enumerate_children = True
        if self.transformed_by is not None:
            if self.transformed_by is True:
                rv += ' (transformed)'
            else:
                rv += ' (transformed by %s)' % self.transformed_by
        rv = indent + rv
        indent += '    '
        i = 0
        for node in self:
            if hasattr(node, '__repr1__'):
                if enumerate_children:
                    child = node.__repr1__(indent, i)
                else:
                    child = node.__repr1__(indent, None)
            else:
                inst = node.format(line_prefix='')
                if inst.startswith('\n'):
                    inst = inst[1:]
                if enumerate_children:
                    child = indent + '%2d. %s' % (i, inst)
                else:
                    child = indent + inst
            rv += '\n' + child
            i += 1

        return rv

    def first_child(self):
        if len(self) > 0:
            child = self[0]
            if not isinstance(child, SyntaxTree):
                return child
            return child.first_child()
        return self

    def last_child(self):
        if len(self) > 0:
            child = self[(-1)]
            if not isinstance(child, SyntaxTree):
                return child
            return child.last_child()
        return self