# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/slimit/slimit/mangler.py
# Compiled at: 2018-07-11 18:15:31
__author__ = 'Ruslan Spivak <ruslan.spivak@gmail.com>'
from slimit.scope import SymbolTable
from slimit.visitors.scopevisitor import ScopeTreeVisitor, fill_scope_references, mangle_scope_tree, NameManglerVisitor

def mangle(tree, toplevel=False):
    """Mangle names.

    Args:
        toplevel: defaults to False. Defines if global
        scope should be mangled or not.
    """
    sym_table = SymbolTable()
    visitor = ScopeTreeVisitor(sym_table)
    visitor.visit(tree)
    fill_scope_references(tree)
    mangle_scope_tree(sym_table.globals, toplevel)
    mangler = NameManglerVisitor()
    mangler.visit(tree)