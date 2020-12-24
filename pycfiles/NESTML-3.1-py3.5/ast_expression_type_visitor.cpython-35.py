# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/visitors/ast_expression_type_visitor.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 9021 bytes
from pynestml.meta_model import ast_arithmetic_operator, ast_bit_operator, ast_comparison_operator, ast_logical_operator
from pynestml.meta_model.ast_expression import ASTExpression
from pynestml.meta_model.ast_simple_expression import ASTSimpleExpression
from pynestml.visitors.ast_binary_logic_visitor import ASTBinaryLogicVisitor
from pynestml.visitors.ast_boolean_literal_visitor import ASTBooleanLiteralVisitor
from pynestml.visitors.ast_comparison_operator_visitor import ASTComparisonOperatorVisitor
from pynestml.visitors.ast_condition_visitor import ASTConditionVisitor
from pynestml.visitors.ast_dot_operator_visitor import ASTDotOperatorVisitor
from pynestml.visitors.ast_function_call_visitor import ASTFunctionCallVisitor
from pynestml.visitors.ast_inf_visitor import ASTInfVisitor
from pynestml.visitors.ast_line_operation_visitor import ASTLineOperatorVisitor
from pynestml.visitors.ast_logical_not_visitor import ASTLogicalNotVisitor
from pynestml.visitors.ast_no_semantics_visitor import ASTNoSemanticsVisitor
from pynestml.visitors.ast_numeric_literal_visitor import ASTNumericLiteralVisitor
from pynestml.visitors.ast_parentheses_visitor import ASTParenthesesVisitor
from pynestml.visitors.ast_power_visitor import ASTPowerVisitor
from pynestml.visitors.ast_string_literal_visitor import ASTStringLiteralVisitor
from pynestml.visitors.ast_unary_visitor import ASTUnaryVisitor
from pynestml.visitors.ast_variable_visitor import ASTVariableVisitor
from pynestml.visitors.ast_visitor import ASTVisitor

class ASTExpressionTypeVisitor(ASTVisitor):
    __doc__ = '\n    This is the main visitor as used to derive the type of an expression. By using different sub-visitors and\n    real-self it is possible to adapt to different types of sub-expressions.\n    '
    unary_visitor = ASTUnaryVisitor()
    pow_visitor = ASTPowerVisitor()
    parentheses_visitor = ASTParenthesesVisitor()
    logical_not_visitor = ASTLogicalNotVisitor()
    dot_operator_visitor = ASTDotOperatorVisitor()
    line_operator_visitor = ASTLineOperatorVisitor()
    no_semantics = ASTNoSemanticsVisitor()
    comparison_operator_visitor = ASTComparisonOperatorVisitor()
    binary_logic_visitor = ASTBinaryLogicVisitor()
    condition_visitor = ASTConditionVisitor()
    function_call_visitor = ASTFunctionCallVisitor()
    boolean_literal_visitor = ASTBooleanLiteralVisitor()
    numeric_literal_visitor = ASTNumericLiteralVisitor()
    string_literal_visitor = ASTStringLiteralVisitor()
    variable_visitor = ASTVariableVisitor()
    inf_visitor = ASTInfVisitor()

    def handle(self, _node):
        """
        Handles the handed over node and executes the required sub routines.
        :param _node: a meta_model node.
        :type _node: AST_
        """
        self.traverse(_node)
        self.get_real_self().visit(_node)
        self.get_real_self().endvisit(_node)

    def traverse_simple_expression(self, node):
        """
        Traverses a simple expression and invokes required subroutines.
        :param node: a single node.
        :type node: ASTSimpleExpression
        """
        assert node is not None and isinstance(node, ASTSimpleExpression), '(PyNestML.ASTExpressionTypeVisitor) No or wrong type of simple-expression provided (%s)!' % type(node)
        if isinstance(node, ASTSimpleExpression):
            if node.get_function_call() is not None:
                self.set_real_self(self.function_call_visitor)
                return
            if node.get_numeric_literal() is not None or node.get_numeric_literal() is not None and node.get_variable() is not None:
                self.set_real_self(self.numeric_literal_visitor)
                return
            if node.get_variable() is not None:
                self.set_real_self(self.variable_visitor)
                return
            if node.is_boolean_true or node.is_boolean_false:
                self.set_real_self(self.boolean_literal_visitor)
                return
            if node.is_inf_literal:
                self.set_real_self(self.inf_visitor)
                return
            if node.is_string():
                self.set_real_self(self.string_literal_visitor)
                return

    def traverse_expression(self, _node):
        """
        Traverses an expression and executes the required sub-routines.
        :param _node: a single meta_model node
        :type _node: ASTExpression
        """
        assert _node is not None and isinstance(_node, ASTExpression), '(PyNestML.ASTExpressionTypeVisitor) No or wrong type of expression provided (%s)!' % type(_node)
        if _node.get_expression() is not None and _node.get_unary_operator() is not None:
            _node.get_expression().accept(self)
            self.set_real_self(self.unary_visitor)
            return
        if _node.get_expression() is not None:
            _node.get_expression().accept(self)
            if _node.is_encapsulated:
                self.set_real_self(self.parentheses_visitor)
                return
            if _node.is_logical_not:
                self.set_real_self(self.logical_not_visitor)
                return
        if _node.get_binary_operator() is not None:
            bin_op = _node.get_binary_operator()
            if _node.get_lhs() is not None:
                _node.get_lhs().accept(self)
            if _node.get_rhs() is not None:
                _node.get_rhs().accept(self)
            if isinstance(bin_op, ast_arithmetic_operator.ASTArithmeticOperator):
                pass
            if bin_op.is_pow_op:
                self.set_real_self(self.pow_visitor)
                return
            if bin_op.is_times_op or bin_op.is_div_op or bin_op.is_modulo_op:
                self.set_real_self(self.dot_operator_visitor)
                return
            if bin_op.is_plus_op or bin_op.is_minus_op:
                self.set_real_self(self.line_operator_visitor)
                return
            if isinstance(bin_op, ast_bit_operator.ASTBitOperator):
                self.set_real_self(self.no_semantics)
                return
            if isinstance(bin_op, ast_comparison_operator.ASTComparisonOperator):
                self.set_real_self(self.comparison_operator_visitor)
                return
            if isinstance(bin_op, ast_logical_operator.ASTLogicalOperator):
                self.set_real_self(self.binary_logic_visitor)
                return
        if _node.get_condition() is not None and _node.get_if_true() is not None and _node.get_if_not() is not None:
            _node.get_condition().accept(self)
            _node.get_if_true().accept(self)
            _node.get_if_not().accept(self)
            self.set_real_self(self.condition_visitor)
            return