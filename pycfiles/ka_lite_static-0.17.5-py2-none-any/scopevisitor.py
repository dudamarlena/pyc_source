# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/slimit/slimit/visitors/scopevisitor.py
# Compiled at: 2018-07-11 18:15:31
__author__ = 'Ruslan Spivak <ruslan.spivak@gmail.com>'
from slimit import ast
from slimit.scope import VarSymbol, FuncSymbol, LocalScope, SymbolTable

class Visitor(object):

    def visit(self, node):
        method = 'visit_%s' % node.__class__.__name__
        return getattr(self, method, self.generic_visit)(node)

    def generic_visit(self, node):
        if node is None:
            return
        else:
            if isinstance(node, list):
                for child in node:
                    self.visit(child)

            else:
                for child in node.children():
                    self.visit(child)

            return


class ScopeTreeVisitor(Visitor):
    """Builds scope tree."""

    def __init__(self, sym_table):
        self.sym_table = sym_table
        self.current_scope = sym_table.globals

    def visit_VarDecl(self, node):
        ident = node.identifier
        symbol = VarSymbol(name=ident.value)
        if symbol not in self.current_scope:
            self.current_scope.define(symbol)
        ident.scope = self.current_scope
        self.visit(node.initializer)

    def visit_Identifier(self, node):
        node.scope = self.current_scope

    def visit_FuncDecl(self, node):
        if node.identifier is not None:
            name = node.identifier.value
            self.visit_Identifier(node.identifier)
        else:
            name = None
        func_sym = FuncSymbol(name=name, enclosing_scope=self.current_scope)
        if name is not None:
            self.current_scope.define(func_sym)
            node.scope = self.current_scope
        self.current_scope = func_sym
        for ident in node.parameters:
            self.current_scope.define(VarSymbol(ident.value))
            ident.scope = self.current_scope

        for element in node.elements:
            self.visit(element)

        self.current_scope = self.current_scope.get_enclosing_scope()
        return

    visit_FuncExpr = visit_FuncDecl

    def visit_Catch(self, node):
        ident = node.identifier
        existing_symbol = self.current_scope.symbols.get(ident.value)
        if existing_symbol is None:
            self.current_scope.define(VarSymbol(ident.value))
        ident.scope = self.current_scope
        for element in node.elements:
            self.visit(element)

        return


class RefVisitor(Visitor):
    """Fill 'ref' attribute in scopes."""

    def visit_Identifier(self, node):
        if self._is_id_in_expr(node):
            self._fill_scope_refs(node.value, node.scope)

    @staticmethod
    def _is_id_in_expr(node):
        """Return True if Identifier node is part of an expression."""
        return getattr(node, 'scope', None) is not None and getattr(node, '_in_expression', False)

    @staticmethod
    def _fill_scope_refs(name, scope):
        """Put referenced name in 'ref' dictionary of a scope.

        Walks up the scope tree and adds the name to 'ref' of every scope
        up in the tree until a scope that defines referenced name is reached.
        """
        symbol = scope.resolve(name)
        if symbol is None:
            return
        else:
            orig_scope = symbol.scope
            scope.refs[name] = orig_scope
            while scope is not orig_scope:
                scope = scope.get_enclosing_scope()
                scope.refs[name] = orig_scope

            return


def mangle_scope_tree(root, toplevel):
    """Walk over a scope tree and mangle symbol names.

    Args:
        toplevel: Defines if global scope should be mangled or not.
    """

    def mangle(scope):
        if scope.get_enclosing_scope() is None and not toplevel:
            return
        else:
            for name in scope.symbols:
                mangled_name = scope.get_next_mangled_name()
                scope.mangled[name] = mangled_name
                scope.rev_mangled[mangled_name] = name

            return

    def visit(node):
        mangle(node)
        for child in node.children:
            visit(child)

    visit(root)


def fill_scope_references(tree):
    """Fill 'ref' scope attribute with values."""
    visitor = RefVisitor()
    visitor.visit(tree)


class NameManglerVisitor(Visitor):
    """Mangles names.

    Walks over a parsed tree and changes ID values to corresponding
    mangled names.
    """

    @staticmethod
    def _is_mangle_candidate(id_node):
        """Return True if Identifier node is a candidate for mangling.

        There are 5 cases when Identifier is a mangling candidate:
        1. Function declaration identifier
        2. Function expression identifier
        3. Function declaration/expression parameter
        4. Variable declaration identifier
        5. Identifier is a part of an expression (primary_expr_no_brace rule)
        """
        return getattr(id_node, '_mangle_candidate', False)

    def visit_Identifier(self, node):
        """Mangle names."""
        if not self._is_mangle_candidate(node):
            return
        else:
            name = node.value
            symbol = node.scope.resolve(node.value)
            if symbol is None:
                return
            mangled = symbol.scope.mangled.get(name)
            if mangled is not None:
                node.value = mangled
            return