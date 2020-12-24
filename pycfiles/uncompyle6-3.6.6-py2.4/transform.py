# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/uncompyle6/semantics/transform.py
# Compiled at: 2020-04-18 17:55:36
from xdis import iscode
from uncompyle6.show import maybe_show_tree
from copy import copy
from spark_parser import GenericASTTraversal, GenericASTTraversalPruningException
from uncompyle6.semantics.helper import find_code_node
from uncompyle6.parsers.treenode import SyntaxTree
from uncompyle6.scanners.tok import NoneToken, Token
from uncompyle6.semantics.consts import RETURN_NONE

def is_docstring(node):
    if node == 'sstmt':
        node = node[0]
    try:
        return node.kind == 'assign' and node[1][0].pattr == '__doc__'
    except:
        return False


def is_not_docstring(call_stmt_node):
    try:
        return call_stmt_node == 'call_stmt' and call_stmt_node[0][0] == 'LOAD_STR' and call_stmt_node[1] == 'POP_TOP'
    except:
        return False


class TreeTransform(GenericASTTraversal, object):
    __module__ = __name__

    def __init__(self, version, show_ast=None, is_pypy=False):
        self.version = version
        self.showast = show_ast
        self.is_pypy = is_pypy

    def maybe_show_tree(self, ast):
        if isinstance(self.showast, dict) and self.showast:
            maybe_show_tree(self, ast)

    def preorder(self, node=None):
        """Walk the tree in roughly 'preorder' (a bit of a lie explained below).
        For each node with typestring name *name* if the
        node has a method called n_*name*, call that before walking
        children.

        In typical use a node with children can call "preorder" in any
        order it wants which may skip children or order then in ways
        other than first to last.  In fact, this this happens.  So in
        this sense this function not strictly preorder.
        """
        if node is None:
            node = self.ast
        try:
            name = 'n_' + self.typestring(node)
            if hasattr(self, name):
                func = getattr(self, name)
                node = func(node)
        except GenericASTTraversalPruningException:
            return

        for (i, kid) in enumerate(node):
            node[i] = self.preorder(kid)

        return node

    def n_mkfunc(self, node):
        """If the function has a docstring (this is found in the code
        constants), pull that out and make it part of the syntax
        tree. When generating the source string that AST node rather
        than the code field is seen and used.
        """
        if self.version >= 3.7:
            code_index = -3
        else:
            code_index = -2
        code = find_code_node(node, code_index).attr
        if node[(-1)].pattr != 'closure' and len(code.co_consts) > 0 and code.co_consts[0] is not None:
            docstring_node = SyntaxTree('docstring', [Token('LOAD_STR', has_arg=True, pattr=code.co_consts[0])])
            docstring_node.transformed_by = 'n_mkfunc'
            node = SyntaxTree('mkfunc', node[:-1] + [docstring_node, node[(-1)]])
            node.transformed_by = 'n_mkfunc'
        return node

    def n_ifstmt(self, node):
        """Here we check if we can turn an `ifstmt` or 'iflaststmtl` into
           some kind of `assert` statement"""
        testexpr = node[0]
        if testexpr not in ('testexpr', 'testexprl'):
            return node
        if node.kind in ('ifstmt', 'ifstmtl'):
            ifstmts_jump = node[1]
            if ifstmts_jump == '_ifstmts_jumpl' and ifstmts_jump[0] == '_ifstmts_jump':
                ifstmts_jump = ifstmts_jump[0]
            elif ifstmts_jump not in ('_ifstmts_jump', '_ifstmts_jumpl', 'ifstmts_jumpl'):
                return node
            stmts = ifstmts_jump[0]
        else:
            stmts = node[1]
        if stmts in ('c_stmts', 'stmts', 'stmts_opt') and len(stmts) == 1:
            raise_stmt = stmts[0]
            if raise_stmt != 'raise_stmt1' and len(raise_stmt) > 0:
                raise_stmt = raise_stmt[0]
            testtrue_or_false = testexpr[0]
            if raise_stmt.kind == 'raise_stmt1' and 1 <= len(testtrue_or_false) <= 2 and raise_stmt.first_child().pattr == 'AssertionError':
                if testtrue_or_false in ('testtrue', 'testtruel'):
                    assert_expr = testtrue_or_false[0]
                    jump_cond = NoneToken
                else:
                    assert testtrue_or_false in ('testfalse', 'testfalsel')
                    assert_expr = testtrue_or_false[0]
                    if assert_expr in ('testfalse_not_and', 'and_not'):
                        return node
                    jump_cond = testtrue_or_false[1]
                    assert_expr.kind = 'assert_expr'
                expr = raise_stmt[0]
                RAISE_VARARGS_1 = raise_stmt[1]
                call = expr[0]
                if call == 'call':
                    if jump_cond in ('jmp_true', NoneToken):
                        kind = 'assert2'
                    else:
                        if jump_cond == 'jmp_false':
                            return node
                        kind = 'assert2not'
                    LOAD_ASSERT = call[0].first_child()
                    if LOAD_ASSERT not in ('LOAD_ASSERT', 'LOAD_GLOBAL'):
                        return node
                    if isinstance(call[1], SyntaxTree):
                        expr = call[1][0]
                        node = SyntaxTree(kind, [
                         assert_expr, jump_cond, LOAD_ASSERT, expr, RAISE_VARARGS_1])
                        node.transformed_by = 'n_ifstmt'
                else:
                    if jump_cond in ('jmp_true', NoneToken):
                        if self.is_pypy:
                            kind = 'assert0_pypy'
                        else:
                            kind = 'assert'
                    else:
                        assert jump_cond == 'jmp_false'
                        kind = 'assertnot'
                    LOAD_ASSERT = expr[0]
                    node = SyntaxTree(kind, [assert_expr, jump_cond, LOAD_ASSERT, RAISE_VARARGS_1])
                node.transformed_by = ('n_ifstmt', )
        return node

    n_ifstmtl = n_iflaststmtl = n_ifstmt

    def n_ifelsestmt(self, node, preprocess=False):
        """
        Transformation involving if..else statments.
        For example

          if ...
          else
             if ..

        into:

          if ..
          elif ...

          [else ...]

        where appropriate.
        """
        else_suite = node[3]
        n = else_suite[0]
        old_stmts = None
        else_suite_index = 1
        len_n = len(n)
        if len_n == 1 == len(n[0]) and n[0] == 'stmt':
            n = n[0][0]
        elif len_n == 0:
            return node
        elif n[0].kind in ('lastc_stmt', 'lastl_stmt'):
            n = n[0]
            if n[0].kind in ('ifstmt', 'iflaststmt', 'iflaststmtl', 'ifelsestmtl',
                             'ifelsestmtc', 'ifpoplaststmtl'):
                n = n[0]
                if n.kind == 'ifpoplaststmtl':
                    old_stmts = n[2]
                    else_suite_index = 2
        else:
            if len_n > 1 and isinstance(n[0], SyntaxTree) and 1 == len(n[0]) and n[0] == 'stmt' and n[1].kind == 'stmt':
                else_suite_stmts = n[0]
            elif len_n == 1:
                else_suite_stmts = n
            else:
                return node
            if else_suite_stmts[0].kind in ('ifstmt', 'iflaststmt', 'ifelsestmt', 'ifelsestmtl'):
                old_stmts = n
                n = else_suite_stmts[0]
            else:
                return node
        if n.kind in ('ifstmt', 'iflaststmt', 'iflaststmtl', 'ifpoplaststmtl'):
            node.kind = 'ifelifstmt'
            n.kind = 'elifstmt'
        elif n.kind in ('ifelsestmtr', ):
            node.kind = 'ifelifstmt'
            n.kind = 'elifelsestmtr'
        elif n.kind in ('ifelsestmt', 'ifelsestmtc', 'ifelsestmtl'):
            node.kind = 'ifelifstmt'
            self.n_ifelsestmt(n, preprocess=True)
            if n == 'ifelifstmt':
                n.kind = 'elifelifstmt'
            elif n.kind in ('ifelsestmt', 'ifelsestmtc', 'ifelsestmtl'):
                n.kind = 'elifelsestmt'
        if not preprocess:
            if old_stmts:
                if n.kind == 'elifstmt':
                    trailing_else = SyntaxTree('stmts', old_stmts[1:])
                    if len(trailing_else):
                        elifelse_stmt = SyntaxTree('elifelsestmtr', [n[0], n[else_suite_index], trailing_else])
                        node[3] = elifelse_stmt
                    else:
                        elif_stmt = SyntaxTree('elifstmt', [n[0], n[else_suite_index]])
                        node[3] = elif_stmt
                    node.transformed_by = 'n_ifelsestmt'
            return node
        return

    n_ifelsestmtc = n_ifelsestmtl = n_ifelsestmt

    def n_import_from37(self, node):
        importlist37 = node[3]
        assert importlist37 == 'importlist37'
        if len(importlist37) == 1:
            alias37 = importlist37[0]
            store = alias37[1]
            assert store == 'store'
            alias_name = store[0].attr
            import_name_attr = node[2]
            assert import_name_attr == 'IMPORT_NAME_ATTR'
            dotted_names = import_name_attr.attr.split('.')
            if len(dotted_names) > 1 and dotted_names[(-1)] == alias_name:
                node = SyntaxTree('import_as37', [node[0], node[1], import_name_attr, store, node[(-1)]])
                node.transformed_by = 'n_import_from37'
        return node

    def n_list_for(self, list_for_node):
        expr = list_for_node[0]
        if expr == 'expr':
            if expr[0] == 'get_iter':
                pass
            else:
                raise expr[0][0] == 'expr' or AssertionError
            list_for_node[0] = expr[0][0]
            list_for_node.transformed_by = ('n_list_for', )
        return list_for_node

    def n_stmts(self, node):
        if node.first_child() == 'SETUP_ANNOTATIONS':
            prev = node[0][0]
            new_stmts = [node[0]]
            for (i, sstmt) in enumerate(node[1:]):
                ann_assign = sstmt[0][0]
                if sstmt[0] == 'stmt' and ann_assign == 'ann_assign' and prev == 'assign':
                    annotate_var = ann_assign[(-2)]
                    if annotate_var.attr == prev[(-1)][0].attr:
                        del new_stmts[-1]
                        sstmt[0][0] = SyntaxTree('ann_assign_init', [ann_assign[0], prev[0], annotate_var])
                        sstmt[0][0].transformed_by = 'n_stmts'
                new_stmts.append(sstmt)
                prev = ann_assign

            node.data = new_stmts
        return node

    def traverse(self, node, is_lambda=False):
        node = self.preorder(node)
        return node

    def transform(self, ast):
        self.maybe_show_tree(ast)
        self.ast = copy(ast)
        self.ast = self.traverse(self.ast, is_lambda=False)
        try:
            call_stmt = ast[0][0]
            if is_not_docstring(call_stmt):
                call_stmt.kind = 'string_at_beginning'
                call_stmt.transformed_by = 'transform'
        except:
            pass

        try:
            for i in range(len(self.ast)):
                sstmt = ast[i]
                if len(sstmt) == 1 and sstmt == 'sstmt':
                    ast[i] = ast[i][0]
                if is_docstring(self.ast[i]):
                    docstring_ast = SyntaxTree('docstring', [
                     Token('LOAD_STR', has_arg=True, offset=0, attr=self.ast[i][0][0].attr, pattr=self.ast[i][0][0].pattr)])
                    docstring_ast.transformed_by = 'transform'
                    del self.ast[i]
                    self.ast.insert(0, docstring_ast)
                    break

            if self.ast[(-1)] == RETURN_NONE:
                self.ast.pop()
        except:
            pass

        return self.ast