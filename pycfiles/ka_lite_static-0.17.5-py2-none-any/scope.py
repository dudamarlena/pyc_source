# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/slimit/slimit/scope.py
# Compiled at: 2018-07-11 18:15:31
__author__ = 'Ruslan Spivak <ruslan.spivak@gmail.com>'
import itertools
try:
    from collections import OrderedDict
except ImportError:
    from odict import odict as OrderedDict

from slimit.lexer import Lexer
ID_CHARS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

def powerset(iterable):
    """powerset('abc') -> a b c ab ac bc abc"""
    s = list(iterable)
    for chars in itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(1, len(s) + 1)):
        yield ('').join(chars)


class SymbolTable(object):

    def __init__(self):
        self.globals = GlobalScope()


class Scope(object):

    def __init__(self, enclosing_scope=None):
        self.symbols = OrderedDict()
        self.mangled = {}
        self.rev_mangled = {}
        self.refs = {}
        self.has_eval = False
        self.has_with = False
        self.enclosing_scope = enclosing_scope
        self.children = []
        if enclosing_scope is not None:
            self.enclosing_scope.add_child(self)
        self.base54 = powerset(ID_CHARS)
        return

    def __contains__(self, sym):
        return sym.name in self.symbols

    def add_child(self, scope):
        self.children.append(scope)

    def define(self, sym):
        self.symbols[sym.name] = sym
        sym.scope = self

    def resolve(self, name):
        sym = self.symbols.get(name)
        if sym is not None:
            return sym
        else:
            if self.enclosing_scope is not None:
                return self.enclosing_scope.resolve(name)
            return

    def get_enclosing_scope(self):
        return self.enclosing_scope

    def _get_scope_with_mangled(self, name):
        """Return a scope containing passed mangled name."""
        scope = self
        while True:
            parent = scope.get_enclosing_scope()
            if parent is None:
                return
            if name in parent.rev_mangled:
                return parent
            scope = parent

        return

    def _get_scope_with_symbol(self, name):
        """Return a scope containing passed name as a symbol name."""
        scope = self
        while True:
            parent = scope.get_enclosing_scope()
            if parent is None:
                return
            if name in parent.symbols:
                return parent
            scope = parent

        return

    def get_next_mangled_name(self):
        """
        1. Do not shadow a mangled name from a parent scope
           if we reference the original name from that scope
           in this scope or any sub-scope.

        2. Do not shadow an original name from a parent scope
           if it's not mangled and we reference it in this scope
           or any sub-scope.

        """
        while True:
            mangled = self.base54.next()
            ancestor = self._get_scope_with_mangled(mangled)
            if ancestor is not None and self.refs.get(ancestor.rev_mangled[mangled]) is ancestor:
                continue
            ancestor = self._get_scope_with_symbol(mangled)
            if ancestor is not None and self.refs.get(mangled) is ancestor and mangled not in ancestor.mangled:
                continue
            if mangled.upper() in Lexer.keywords:
                continue
            return mangled

        return


class GlobalScope(Scope):
    pass


class LocalScope(Scope):
    pass


class Symbol(object):

    def __init__(self, name):
        self.name = name
        self.scope = None
        return


class VarSymbol(Symbol):
    pass


class FuncSymbol(Symbol, Scope):
    """Function symbol is both a symbol and a scope for arguments."""

    def __init__(self, name, enclosing_scope):
        Symbol.__init__(self, name)
        Scope.__init__(self, enclosing_scope)