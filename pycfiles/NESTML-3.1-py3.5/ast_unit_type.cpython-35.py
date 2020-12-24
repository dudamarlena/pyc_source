# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/meta_model/ast_unit_type.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 6841 bytes
from pynestml.meta_model.ast_node import ASTNode

class ASTUnitType(ASTNode):
    __doc__ = "\n    This class stores information regarding unit types and their properties.\n    ASTUnitType. Represents an unit datatype. It can be a plain datatype as 'mV' or a\n    complex data type as 'mV/s'\n  \n    unitType : leftParentheses='(' unitType rightParentheses=')'\n               | base=unitType powOp='**' exponent=UNSIGNED_INTEGER\n               | left=unitType (timesOp='*' | divOp='/') right=unitType\n               | unitlessLiteral=UNSIGNED_INTEGER divOp='/' right=unitType\n               | unit=NAME;\n    Attributes:\n        # encapsulated or not\n        is_encapsulated = False\n        compound_unit = None\n        # pow rhs\n        base = None\n        is_pow = False\n        exponent = None\n        # arithmetic combination case\n        lhs = None\n        is_times = False\n        is_div = False\n        rhs = None\n        # simple case, just a name\n        unit = None\n        # the corresponding symbol\n        type_symbol = None\n    "

    def __init__(self, is_encapsulated=False, compound_unit=None, base=None, is_pow=False, exponent=None, lhs=None, rhs=None, is_div=False, is_times=False, _unit=None, source_position=None):
        """
        Standard constructor of ASTUnitType.
        :param compound_unit: a unit encapsulated in brackets
        :type compound_unit: ASTUnitType
        :param base: the base rhs
        :type base: ASTUnitType
        :param is_pow: is a power rhs
        :type is_pow: bool
        :param exponent: the exponent rhs
        :type exponent: int
        :param lhs: the left-hand side rhs
        :type lhs: ASTUnitType or Integer
        :param rhs: the right-hand side rhs
        :type rhs: ASTUnitType
        :param is_div: is a division rhs
        :type is_div: bool
        :param is_times: is a times rhs
        :type is_times: bool
        :param _unit: is a single unit, e.g. mV
        :type _unit: string
        """
        super(ASTUnitType, self).__init__(source_position)
        self.is_encapsulated = is_encapsulated
        self.compound_unit = compound_unit
        self.base = base
        self.is_pow = is_pow
        self.exponent = exponent
        self.lhs = lhs
        self.is_times = is_times
        self.is_div = is_div
        self.rhs = rhs
        self.unit = _unit
        self.type_symbol = None

    def is_simple_unit(self):
        """
        Returns whether the rhs is a simple unit, e.g., mV.
        :return: True if simple unit, otherwise False.
        :rtype: bool
        """
        return self.unit is not None

    def is_arithmetic_expression(self):
        """
        Returns whether the rhs is a arithmetic combination, e.g, mV/mS.
        :return: True if arithmetic rhs, otherwise false.
        :rtype: bool
        """
        return self.lhs is not None and self.rhs is not None and (self.is_div or self.is_times)

    def get_lhs(self):
        """
        Returns the left-hand side rhs if present.
        :return: ASTUnitType instance if present, otherwise None.
        :rtype: ASTUnitType
        """
        return self.lhs

    def get_rhs(self):
        """
        Returns the right-hand side rhs if present.
        :return: ASTUnitType instance if present, otherwise None.
        :rtype: ASTUnitType
        """
        return self.rhs

    def get_type_symbol(self):
        return self.type_symbol

    def set_type_symbol(self, type_symbol):
        self.type_symbol = type_symbol

    def get_parent(self, ast):
        """
        Indicates whether a this node contains the handed over node.
        :param ast: an arbitrary meta_model node.
        :type ast: AST_
        :return: AST if this or one of the child nodes contains the handed over element.
        :rtype: AST_ or None
        """
        if self.is_encapsulated:
            if self.compound_unit is ast:
                return self
            if self.compound_unit.get_parent(ast) is not None:
                pass
            return self.compound_unit.get_parent(ast)
        if self.is_pow:
            if self.base is ast:
                return self
            if self.base.get_parent(ast) is not None:
                pass
            return self.base.get_parent(ast)
        if self.is_arithmetic_expression():
            if isinstance(self.get_lhs(), ASTUnitType):
                if self.get_lhs() is ast:
                    return self
                if self.get_lhs().get_parent(ast) is not None:
                    pass
                return self.get_lhs().get_parent(ast)
            if self.get_rhs() is ast:
                return self
            if self.get_rhs().get_parent(ast) is not None:
                pass
            return self.get_rhs().get_parent(ast)

    def equals(self, other):
        """
        The equals method.
        :param other: a different object.
        :type other: object
        :return: True if equal, otherwise False.
        :rtype: bool
        """
        if not isinstance(other, ASTUnitType):
            return False
        if self.is_encapsulated + other.is_encapsulated == 1:
            return False
        if self.is_encapsulated and other.is_encapsulated and not self.compound_unit.equals(other.compound_unit):
            return False
        if self.is_pow + other.is_pow == 1:
            return False
        if self.is_pow and other.is_pow and not (self.base.equals(other.base) and self.exponent == other.exponent):
            return False
        if self.is_arithmetic_expression() + other.is_arithmetic_expression() == 1:
            return False
        if self.is_arithmetic_expression() and other.is_arithmetic_expression() and not (self.get_lhs().equals(other.lhs) and self.rhs.equals(other.rhs) and self.is_times == other.is_times and self.is_div == other.is_div):
            return False
        if self.is_simple_unit() + other.is_simple_unit() == 1:
            return False
        if self.is_simple_unit() and other.is_simple_unit() and not self.unit == other.unit:
            return False
        return True