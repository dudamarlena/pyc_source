# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/symbol_table/symbol_table.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 3054 bytes
from pynestml.symbol_table.scope import Scope, ScopeType

class SymbolTable(object):
    __doc__ = '\n    This class is used to store a single symbol table, consisting of scope and symbols.\n    \n    Attributes:\n        name2neuron_scope A dict from the name of a neuron to the corresponding scope. Type str->Scope\n        sourcePosition The source position of the overall compilation unit. Type ASTSourceLocation\n    '
    name2neuron_scope = {}
    source_location = None

    @classmethod
    def initialize_symbol_table(cls, source_position):
        """
        Standard initializer.
        """
        cls.source_location = source_position
        cls.name2neuron_scope = {}

    @classmethod
    def add_neuron_scope(cls, name, scope):
        """
        Adds a single neuron scope to the set of stored scopes.
        :return: a single scope element.
        :rtype: Scope
        """
        assert isinstance(scope, Scope), '(PyNestML.SymbolTable.SymbolTable) No or wrong type of scope provided (%s)!' % type(scope)
        assert scope.get_scope_type() == ScopeType.GLOBAL, '(PyNestML.SymbolTable.SymbolTable) Only global scopes can be added!'
        assert isinstance(name, str), '(PyNestML.SymbolTable.SymbolTable) No or wrong type of name provided (%s)!' % type(name)
        if name not in cls.name2neuron_scope.keys():
            cls.name2neuron_scope[name] = scope

    @classmethod
    def delete_neuron_scope(cls, name):
        """
        Deletes a single neuron scope from the set of stored scopes.
        :return: the name of the scope to delete.
        :rtype: Scope
        """
        if name in cls.name2neuron_scope.keys():
            del cls.name2neuron_scope[name]

    @classmethod
    def clean_up_table(cls):
        """
        Deletes all entries as stored in the symbol table.
        """
        del cls.name2neuron_scope
        cls.name2neuron_scope = {}

    @classmethod
    def print_symbol_table(cls):
        """
        Prints the content of this symbol table.
        """
        ret = ''
        for _name in cls.name2neuron_scope.keys():
            ret += '--------------------------------------------------\n'
            ret += _name + ':\n'
            ret += cls.name2neuron_scope[_name].print_scope()

        return ret