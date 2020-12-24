# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jishaku/repl/walkers.py
# Compiled at: 2020-03-05 23:53:06
# Size of source mod 2**32: 6227 bytes
"""
jishaku.repl.walkers
~~~~~~~~~~~~~~~~~~~~

AST walkers for code transformation and analysis.

:copyright: (c) 2020 Devon (Gorialis) R
:license: MIT, see LICENSE for more details.

"""
import ast

class KeywordTransformer(ast.NodeTransformer):
    __doc__ = '\n    This transformer:\n    - Converts return-with-value into yield & return\n    - Converts bare deletes into conditional global pops\n    '

    def visit_FunctionDef(self, node):
        return node

    def visit_AsyncFunctionDef(self, node):
        return node

    def visit_ClassDef(self, node):
        return node

    def visit_Return(self, node):
        if node.value is None:
            return node
        else:
            return ast.If(test=ast.NameConstant(value=True,
              lineno=(node.lineno),
              col_offset=(node.col_offset)),
              body=[
             ast.Expr(value=ast.Yield(value=(node.value),
               lineno=(node.lineno),
               col_offset=(node.col_offset)),
               lineno=(node.lineno),
               col_offset=(node.col_offset)),
             ast.Return(value=None,
               lineno=(node.lineno),
               col_offset=(node.col_offset))],
              orelse=[],
              lineno=(node.lineno),
              col_offset=(node.col_offset))

    def visit_Delete(self, node):
        """
        This converter replaces bare deletes with conditional global pops.

        It is roughly equivalent to transforming:

        .. code:: python

            del foobar

        into:

        .. code:: python

            if 'foobar' in globals():
                globals().pop('foobar')
            else:
                del foobar

        This thus makes deletions in retain mode work more-or-less as intended.
        """
        return ast.If(test=ast.NameConstant(value=True,
          lineno=(node.lineno),
          col_offset=(node.col_offset)),
          body=[ast.If(test=ast.Compare(left=ast.Str(s=(target.id), lineno=(node.lineno), col_offset=(node.col_offset)), ops=[ast.In(lineno=(node.lineno), col_offset=(node.col_offset))], comparators=[self.globals_call(node)], lineno=(node.lineno), col_offset=(node.col_offset)), body=[ast.Expr(value=ast.Call(func=ast.Attribute(value=(self.globals_call(node)), attr='pop', ctx=(ast.Load()), lineno=(node.lineno), col_offset=(node.col_offset)), args=[ast.Str(s=(target.id), lineno=(node.lineno), col_offset=(node.col_offset))], keywords=[], lineno=(node.lineno), col_offset=(node.col_offset)), lineno=(node.lineno), col_offset=(node.col_offset))], orelse=[ast.Delete(targets=[target], lineno=(node.lineno), col_offset=(node.col_offset))], lineno=(node.lineno), col_offset=(node.col_offset)) if isinstance(target, ast.Name) else ast.Delete(targets=[target], lineno=(node.lineno), col_offset=(node.col_offset)) for target in node.targets],
          orelse=[],
          lineno=(node.lineno),
          col_offset=(node.col_offset))

    def globals_call(self, node):
        """
        Creates an AST node that calls globals().
        """
        return ast.Call(func=ast.Name(id='globals',
          ctx=(ast.Load()),
          lineno=(node.lineno),
          col_offset=(node.col_offset)),
          args=[],
          keywords=[],
          lineno=(node.lineno),
          col_offset=(node.col_offset))