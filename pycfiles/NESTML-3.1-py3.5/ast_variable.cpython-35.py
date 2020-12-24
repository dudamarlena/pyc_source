# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/meta_model/ast_variable.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 5669 bytes
from copy import copy
from pynestml.meta_model.ast_node import ASTNode
from pynestml.utils.either import Either

class ASTVariable(ASTNode):
    __doc__ = "\n    This class is used to store a single variable.\n    \n    ASTVariable Provides a 'marker' AST node to identify variables used in expressions.\n    Grammar:\n        variable : NAME (differentialOrder=''')*;\n    Attributes:\n        name = None\n        differential_order = None\n        # the corresponding type symbol\n        type_symbol = None\n    "

    def __init__(self, name, differential_order=0, source_position=None):
        """
        Standard constructor.
        :param name: the name of the variable
        :type name: str
        :param differential_order: the differential order of the variable.
        :type differential_order: int
        :param source_position: the position of this element in the source file.
        :type source_position: ASTSourceLocation.
        """
        assert isinstance(differential_order, int), '(PyNestML.AST.Variable) No or wrong type of differential order provided (%s)!' % type(differential_order)
        assert differential_order >= 0, '(PyNestML.AST.Variable) Differential order must be at least 0, is %d!' % differential_order
        assert isinstance(name, str), '(PyNestML.AST.Variable) No or wrong type of name provided (%s)!' % type(name)
        super(ASTVariable, self).__init__(source_position=source_position)
        self.name = name
        self.differential_order = differential_order
        self.type_symbol = None

    def resolve_in_own_scope(self):
        from pynestml.symbols.symbol import SymbolKind
        assert self.get_scope() is not None
        return self.get_scope().resolve_to_symbol(self.get_complete_name(), SymbolKind.VARIABLE)

    def get_name(self):
        """
        Returns the name of the variable.
        :return: the name of the variable.
        :rtype: str
        """
        return self.name

    def set_name(self, name):
        """
        Sets the name of the variable.
        :name: the name to set.
        """
        self.name = name

    def get_differential_order(self):
        """
        Returns the differential order of the variable.
        :return: the differential order.
        :rtype: int
        """
        return self.differential_order

    def get_complete_name(self):
        """
        Returns the complete name, consisting of the name and the differential order.
        :return: the complete name.
        :rtype: str
        """
        return self.get_name() + "'" * self.get_differential_order()

    def get_name_of_lhs(self):
        """
        Returns the complete name but with differential order reduced by one.
        :return: the name.
        :rtype: str
        """
        if self.get_differential_order() > 0:
            return self.get_name() + "'" * (self.get_differential_order() - 1)
        else:
            return self.get_name()

    def get_type_symbol(self):
        """
        Returns the type symbol of this rhs.
        :return: a single type symbol.
        :rtype: type_symbol
        """
        return copy(self.type_symbol)

    def set_type_symbol(self, type_symbol):
        """
        Updates the current type symbol to the handed over one.
        :param type_symbol: a single type symbol object.
        :type type_symbol: type_symbol
        """
        assert type_symbol is not None and isinstance(type_symbol, Either), '(PyNestML.AST.Variable) No or wrong type of type symbol provided (%s)!' % type(type_symbol)
        self.type_symbol = type_symbol

    def get_parent(self, node):
        """
        Indicates whether a this node contains the handed over node.
        :param node: an arbitrary meta_model node.
        :type node: ASTNode
        :return: AST if this or one of the child nodes contains the handed over element.
        :rtype: ASTNode or None
        """
        pass

    def is_unit_variable(self):
        """
        Provided on-the-fly information whether this variable represents a unit-variable, e.g., nS.
        Caution: It assumes that the symbol table has already been constructed.
        :return: True if unit-variable, otherwise False.
        :rtype: bool
        """
        from pynestml.symbols.predefined_types import PredefinedTypes
        if self.get_name() in PredefinedTypes.get_types():
            return True
        else:
            return False

    def equals(self, other):
        """
        The equals method.
        :param other: a different object.
        :type other: object
        :return: True if equals, otherwise False.
        :rtype: bool
        """
        if not isinstance(other, ASTVariable):
            return False
        return self.get_name() == other.get_name() and self.get_differential_order() == other.get_differential_order()