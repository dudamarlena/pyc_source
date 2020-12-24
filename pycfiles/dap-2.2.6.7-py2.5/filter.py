# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/dap/util/filter.py
# Compiled at: 2008-03-31 07:43:21
import sys, inspect, compiler
from urllib import quote
from dap.lib import encode_atom

class ASTVisitor(compiler.visitor.ASTVisitor):

    def __init__(self, scope, seq):
        compiler.visitor.ASTVisitor.__init__(self)
        self.scope = scope
        self.seq = seq
        self.filters = []

    def visitGenExprFor(self, node):
        if self.eval(node.iter) == self.seq:
            self.scope[node.assign.name] = self.seq
        self.visit(node.assign)
        self.visit(node.iter)
        for if_ in node.ifs:
            self.visit(if_)

    def visitListCompFor(self, node):
        if self.eval(node.list) == self.seq:
            self.scope[node.assign.name] = self.seq
        self.visit(node.assign)
        self.visit(node.list)
        for if_ in node.ifs:
            self.visit(if_)

    def visitCompare(self, node):
        if len(node.ops) > 1:
            left = node.expr
            out = []
            for op in node.ops:
                out.append(compiler.ast.Compare(left, [op]))
                left = op[1]

            new_node = compiler.ast.And(out)
            self.visit(new_node)
        else:
            (a, op, b) = node.getChildren()
            ops = ['<', '>', '==', '!=', '<=', '>=']
            if op in ops:
                a = self.eval(a)
                b = self.eval(b)
                if hasattr(a, 'id'):
                    a = a.id
                else:
                    a = quote(encode_atom(a))
                if hasattr(b, 'id'):
                    b = b.id
                else:
                    b = quote(encode_atom(b))
                if op == '==':
                    op = '='
                filter_ = '%s%s%s' % (a, op, b)
                self.filters.append(filter_)

    def visitOr(self, node):
        raise Exception('OR not supported by the DAP spec!')

    def eval(self, node):
        """
        Eval node.

        This is done by converting the node to bytecode and
        eval()ing the bytecode in the instance scope.
        """
        ast = compiler.ast.Expression(node)
        ast.filename = 'dummy'
        c = compiler.pycodegen.ExpressionCodeGenerator(ast)
        obj = eval(c.getCode(), self.scope)
        return obj


def get_filters(seq):
    frame = sys._getframe(2)
    (fname, lineno, func, src, index) = inspect.getframeinfo(frame)
    scope = frame.f_globals
    if src:
        src = src[0].strip()
        if src.endswith(':'):
            src = '%s pass' % src
    visitor = ASTVisitor(scope, seq)
    try:
        ast = compiler.parse(src)
        compiler.walk(ast, visitor)
    except:
        pass

    return visitor.filters