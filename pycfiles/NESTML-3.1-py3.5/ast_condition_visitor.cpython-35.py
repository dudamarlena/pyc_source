# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/visitors/ast_condition_visitor.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 4952 bytes
"""
rhs : condition=rhs '?' ifTrue=rhs ':' ifNot=rhs
"""
from pynestml.symbols.error_type_symbol import ErrorTypeSymbol
from pynestml.symbols.predefined_types import PredefinedTypes
from pynestml.symbols.unit_type_symbol import UnitTypeSymbol
from pynestml.utils.error_strings import ErrorStrings
from pynestml.utils.logger import Logger, LoggingLevel
from pynestml.utils.messages import MessageCode
from pynestml.visitors.ast_visitor import ASTVisitor

class ASTConditionVisitor(ASTVisitor):
    __doc__ = '\n    This visitor is used to derive the correct type of a ternary operator, i.e., of all its subexpressions.\n    '

    def visit_expression(self, node):
        """
        Visits an rhs consisting of the ternary operator and updates its type.
        :param node: a single rhs
        :type node: ast_expression
        """
        condition = node.get_condition().type
        if_true = node.get_if_true().type
        if_not = node.get_if_not().type
        condition.referenced_object = node.get_condition()
        if_true.referenced_object = node.get_if_true()
        if_not.referenced_object = node.get_if_not()
        if not condition.equals(PredefinedTypes.get_boolean_type()):
            error_msg = ErrorStrings.message_ternary(self, node.get_source_position())
            node.type = ErrorTypeSymbol()
            Logger.log_message(message=error_msg, error_position=node.get_source_position(), code=MessageCode.TYPE_DIFFERENT_FROM_EXPECTED, log_level=LoggingLevel.ERROR)
            return
        if if_true.equals(if_not) or if_true.differs_only_in_magnitude(if_not) or if_true.is_castable_to(if_not):
            node.type = if_true
            return
        if isinstance(if_true, UnitTypeSymbol) and isinstance(if_not, UnitTypeSymbol):
            error_msg = ErrorStrings.message_ternary_mismatch(self, if_true.print_symbol(), if_not.print_symbol(), node.get_source_position())
            node.type = PredefinedTypes.get_real_type()
            Logger.log_message(message=error_msg, code=MessageCode.TYPE_DIFFERENT_FROM_EXPECTED, error_position=if_true.referenced_object.get_source_position(), log_level=LoggingLevel.WARNING)
            return
        if isinstance(if_true, UnitTypeSymbol) and if_not.is_numeric_primitive() or isinstance(if_not, UnitTypeSymbol) and if_true.is_numeric_primitive():
            if isinstance(if_true, UnitTypeSymbol):
                unit_type = if_true
            else:
                unit_type = if_not
            error_msg = ErrorStrings.message_ternary_mismatch(self, str(if_true), str(if_not), node.get_source_position())
            node.type = unit_type
            Logger.log_message(message=error_msg, code=MessageCode.TYPE_DIFFERENT_FROM_EXPECTED, error_position=if_true.referenced_object.get_source_position(), log_level=LoggingLevel.WARNING)
            return
        if if_true.is_numeric_primitive() and if_not.is_numeric_primitive():
            node.type = PredefinedTypes.get_real_type()
            return
        error_msg = ErrorStrings.message_ternary_mismatch(self, str(if_true), str(if_not), node.get_source_position())
        node.type = ErrorTypeSymbol()
        Logger.log_message(message=error_msg, error_position=node.get_source_position(), code=MessageCode.TYPE_DIFFERENT_FROM_EXPECTED, log_level=LoggingLevel.ERROR)