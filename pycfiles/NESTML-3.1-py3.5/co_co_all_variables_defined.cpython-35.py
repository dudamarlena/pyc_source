# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/cocos/co_co_all_variables_defined.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 6632 bytes
from pynestml.cocos.co_co import CoCo
from pynestml.meta_model.ast_declaration import ASTDeclaration
from pynestml.symbols.symbol import SymbolKind
from pynestml.symbols.variable_symbol import BlockType
from pynestml.utils.logger import Logger, LoggingLevel
from pynestml.utils.messages import Messages
from pynestml.visitors.ast_visitor import ASTVisitor

class CoCoAllVariablesDefined(CoCo):
    __doc__ = '\n    This class represents a constraint condition which ensures that all elements as used in expressions have been\n    previously defined.\n    Not allowed:\n        state:\n            V_m mV = V_m + 10mV # <- recursive definition\n            V_m mV = V_n # <- not defined reference\n        end\n    '

    @classmethod
    def check_co_co(cls, node):
        """
        Checks if this coco applies for the handed over neuron. Models which use not defined elements are not
        correct.
        :param node: a single neuron instance.
        :type node: ast_neuron
        """
        expression_collector_visitor = ASTExpressionCollectorVisitor()
        node.accept(expression_collector_visitor)
        expressions = expression_collector_visitor.ret
        for expr in expressions:
            for var in expr.get_variables():
                symbol = var.get_scope().resolve_to_symbol(var.get_complete_name(), SymbolKind.VARIABLE)
                expr_par = node.get_parent(expr)
                if symbol is None:
                    symbol = var.get_scope().resolve_to_symbol(var.get_complete_name(), SymbolKind.TYPE)
                    if symbol is None:
                        code, message = Messages.get_variable_not_defined(var.get_name())
                        Logger.log_message(neuron=node, code=code, message=message, log_level=LoggingLevel.ERROR, error_position=var.get_source_position())
                else:
                    if isinstance(expr_par, ASTDeclaration) and expr_par.get_invariant() == expr:
                        continue
                    elif not symbol.is_predefined and symbol.block_type != BlockType.INPUT_BUFFER_CURRENT and symbol.block_type != BlockType.INPUT_BUFFER_SPIKE and not symbol.get_referenced_object().get_source_position().is_added_source_position():
                        if not symbol.get_referenced_object().get_source_position().before(var.get_source_position()) and symbol.block_type != BlockType.PARAMETERS:
                            code, message = Messages.get_variable_used_before_declaration(var.get_name())
                            Logger.log_message(neuron=node, message=message, error_position=var.get_source_position(), code=code, log_level=LoggingLevel.ERROR)
                        if symbol.get_referenced_object().get_source_position().encloses(var.get_source_position()) and not symbol.get_referenced_object().get_source_position().is_added_source_position():
                            code, message = Messages.get_variable_defined_recursively(var.get_name())
                            Logger.log_message(code=code, message=message, error_position=symbol.get_referenced_object().get_source_position(), log_level=LoggingLevel.ERROR, neuron=node)

        vis = ASTAssignedVariableDefinedVisitor(node)
        node.accept(vis)


class ASTAssignedVariableDefinedVisitor(ASTVisitor):

    def __init__(self, neuron):
        super(ASTAssignedVariableDefinedVisitor, self).__init__()
        self.neuron = neuron

    def visit_assignment(self, node):
        symbol = node.get_scope().resolve_to_symbol(node.get_variable().get_complete_name(), SymbolKind.VARIABLE)
        if symbol is None:
            code, message = Messages.get_variable_not_defined(node.get_variable().get_complete_name())
            Logger.log_message(code=code, message=message, error_position=node.get_source_position(), log_level=LoggingLevel.ERROR, neuron=self.neuron)


class ASTExpressionCollectorVisitor(ASTVisitor):

    def __init__(self):
        super(ASTExpressionCollectorVisitor, self).__init__()
        self.ret = list()

    def visit_expression(self, node):
        self.ret.append(node)

    def traverse_expression(self, node):
        pass

    def visit_simple_expression(self, node):
        self.ret.append(node)

    def traverse_simple_expression(self, node):
        pass