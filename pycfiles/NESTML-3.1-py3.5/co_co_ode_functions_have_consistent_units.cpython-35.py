# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/cocos/co_co_ode_functions_have_consistent_units.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 2144 bytes
from pynestml.cocos.co_co import CoCo
from pynestml.utils.logger import LoggingLevel, Logger
from pynestml.utils.messages import Messages
from pynestml.visitors.ast_visitor import ASTVisitor
from pynestml.symbols.symbol import SymbolKind
from astropy import units

class CoCoOdeFunctionsHaveConsistentUnits(CoCo):
    __doc__ = '\n    This coco ensures that whenever an ODE function is defined, the physical unit of the left-hand side variable matches that of the right-hand side expression.\n    '

    @classmethod
    def check_co_co(cls, node):
        """
        Ensures the coco for the handed over neuron.
        :param node: a single neuron instance.
        :type node: ast_neuron
        """
        node.accept(OdeFunctionConsistentUnitsVisitor())


class OdeFunctionConsistentUnitsVisitor(ASTVisitor):

    def visit_ode_function(self, node):
        """
        Checks the coco.
        :param node: A single ode equation.
        :type node: ast_ode_equation
        """
        declared_type = node.get_data_type().type_symbol
        expression_type = node.get_expression().type
        if not expression_type.is_castable_to(declared_type):
            code, message = Messages.get_ode_function_needs_consistent_units(node.get_variable_name(), declared_type, expression_type)
            Logger.log_message(error_position=node.get_source_position(), code=code, message=message, log_level=LoggingLevel.ERROR)