# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/visitors/ast_data_type_visitor.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 6205 bytes
from astropy import units
from pynestml.meta_model.ast_unit_type import ASTUnitType
from pynestml.symbols.predefined_types import PredefinedTypes
from pynestml.symbols.predefined_units import PredefinedUnits
from pynestml.symbols.unit_type_symbol import UnitTypeSymbol
from pynestml.utils.unit_type import UnitType
from pynestml.visitors.ast_visitor import ASTVisitor

class ASTDataTypeVisitor(ASTVisitor):
    __doc__ = '\n    This class represents a visitor which inspects a handed over data type, checks if correct typing has been used\n    (e.g., no computation between primitive and non primitive data types etc.) and finally updates the type symbols\n    of the datatype meta_model.\n    '

    def __init__(self):
        super(ASTDataTypeVisitor, self).__init__()
        self.symbol = None
        self.result = None

    def visit_data_type(self, node):
        """
        Visits a single data type meta_model node and updates, checks correctness and updates its type symbol.
        This visitor can also be used to derive the original name of the unit.
        :param node: a single datatype node.
        :type node: ast_data_type
        """
        if node.is_integer:
            self.symbol = PredefinedTypes.get_integer_type()
            node.set_type_symbol(self.symbol)
        else:
            if node.is_real:
                self.symbol = PredefinedTypes.get_real_type()
                node.set_type_symbol(self.symbol)
            else:
                if node.is_string:
                    self.symbol = PredefinedTypes.get_string_type()
                    node.set_type_symbol(self.symbol)
                else:
                    if node.is_boolean:
                        self.symbol = PredefinedTypes.get_boolean_type()
                        node.set_type_symbol(self.symbol)
                    elif node.is_void:
                        self.symbol = PredefinedTypes.get_void_type()
                        node.set_type_symbol(self.symbol)

    def endvisit_data_type(self, node):
        if node.is_unit_type():
            node.set_type_symbol(node.get_unit_type().get_type_symbol())
        if self.symbol is not None:
            self.result = self.symbol.get_symbol_name()
        else:
            raise RuntimeError('ASTDataType type symbol could not be derived!')

    def visit_unit_type(self, node):
        """
        Visits a single unit type element, checks for correct usage of units and builds the corresponding combined 
        unit.
        :param node: a single unit type meta_model.
        :type node: ASTUnitType
        :return: a new type symbol representing this unit type.
        :rtype: type_symbol
        """
        if node.is_simple_unit():
            type_s = PredefinedTypes.get_type(node.unit)
            if type_s is None:
                raise RuntimeError('Unknown atomic unit %s.' % node.unit)
        else:
            node.set_type_symbol(type_s)
            self.symbol = type_s

    def endvisit_unit_type(self, node):
        if node.is_encapsulated:
            node.set_type_symbol(node.compound_unit.get_type_symbol())
        else:
            if node.is_pow:
                base_symbol = node.base.get_type_symbol()
                exponent = node.exponent
                astropy_unit = base_symbol.astropy_unit ** exponent
                res = handle_unit(astropy_unit)
                node.set_type_symbol(res)
                self.symbol = res
            else:
                if node.is_div:
                    if isinstance(node.get_lhs(), ASTUnitType):
                        lhs = node.get_lhs().get_type_symbol().astropy_unit
                    else:
                        lhs = node.get_lhs()
                    rhs = node.get_rhs().get_type_symbol().astropy_unit
                    res = lhs / rhs
                    res = handle_unit(res)
                    node.set_type_symbol(res)
                    self.symbol = res
                elif node.is_times:
                    if isinstance(node.get_lhs(), ASTUnitType):
                        lhs = node.get_lhs().get_type_symbol().astropy_unit
                    else:
                        lhs = node.get_lhs()
                    rhs = node.get_rhs().get_type_symbol().astropy_unit
                    res = lhs * rhs
                    res = handle_unit(res)
                    node.set_type_symbol(res)
                    self.symbol = res


def handle_unit(unit_type):
    """
    Handles a handed over unit by creating the corresponding unit-type, storing it in the list of predefined
    units, creating a type symbol and returning it.
    :param unit_type: astropy unit object
    :type unit_type: astropy.units.core.Unit
    :return: a new type symbol
    :rtype: TypeSymbol
    """
    if isinstance(unit_type, units.Quantity) and unit_type.value == 1.0:
        to_process = unit_type.unit
    else:
        to_process = unit_type
    if str(to_process) not in PredefinedUnits.get_units().keys():
        unit_type_t = UnitType(name=str(to_process), unit=to_process)
        PredefinedUnits.register_unit(unit_type_t)
    if PredefinedTypes.get_type(str(to_process)) is None:
        type_symbol = UnitTypeSymbol(unit=PredefinedUnits.get_unit(str(to_process)))
        PredefinedTypes.register_type(type_symbol)
    return PredefinedTypes.get_type(name=str(to_process))