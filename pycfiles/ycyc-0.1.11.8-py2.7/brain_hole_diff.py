# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/tools/brain_hole_diff.py
# Compiled at: 2016-02-25 04:17:16
import ast, astunparse

class BrainHoleDiff(ast.NodeTransformer):

    def has_symbol(self, node):
        return node.id == 'x'

    def expr_parse(self, expr):
        node = ast.parse(expr)
        return node.body[0].value

    def visit_Call(self, node):
        func_name = node.func.id
        if not self.has_symbol(node.args[0]):
            return self.generic_visit(node)
        if func_name == 'sin':
            node.func.id = 'cos'
        elif func_name == 'cos':
            node = self.expr_parse('-sin(x)')
        elif func_name == 'ln':
            node = self.expr_parse('1.0/x')
        elif func_name == 'pow':
            times = node.args[1].n
            node = self.expr_parse('%s*pow(x, %s)' % (times, times - 1))
        return node

    def __call__(self, expr):
        ast_node = ast.parse(expr)
        ast_node = self.visit(ast_node)
        return astunparse.unparse(ast_node)


diff = BrainHoleDiff()
print diff('3*sin(x)-cos(x)')
print diff('ln(x)')
print diff('3*ln(x)+sin(x)-pow(x, 2)+cos(x)')
print eval(diff('pow(x, 3)-pow(x, 2)'), {'x': 1})