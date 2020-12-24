# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/codegeneration/legacy_expression_printer.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 4552 bytes
from pynestml.codegeneration.expressions_pretty_printer import ExpressionsPrettyPrinter
from pynestml.codegeneration.i_reference_converter import IReferenceConverter
from pynestml.codegeneration.idempotent_reference_converter import IdempotentReferenceConverter
from pynestml.meta_model.ast_expression import ASTExpression
from pynestml.meta_model.ast_simple_expression import ASTSimpleExpression

class LegacyExpressionPrinter(ExpressionsPrettyPrinter):
    __doc__ = '\n    An adjusted version of the pretty printer which does not print units with literals.\n    '

    def __init__(self, reference_converter=None):
        """
        Standard constructor.
        :param reference_converter: a single reference converter object.
        :type reference_converter: IReferenceConverter
        """
        from pynestml.codegeneration.expressions_pretty_printer import TypesPrinter
        super(LegacyExpressionPrinter, self).__init__(reference_converter)
        if reference_converter is not None:
            self.reference_converter = reference_converter
        else:
            self.reference_converter = IdempotentReferenceConverter()
        self.types_printer = TypesPrinter()

    def do_print(self, node):
        """
        Prints a single rhs.
        :param node: a single rhs.
        :type node: ASTExpression or ASTSimpleExpression.
        :return: string representation of the rhs
        :rtype: str
        """
        if isinstance(node, ASTSimpleExpression):
            if node.is_numeric_literal():
                return self.types_printer.pretty_print(node.get_numeric_literal())
            if node.is_inf_literal:
                return self.reference_converter.convert_constant('inf')
            if node.is_string():
                return self.types_printer.pretty_print(node.get_string())
            if node.is_boolean_true:
                return self.types_printer.pretty_print(True)
            if node.is_boolean_false:
                return self.types_printer.pretty_print(False)
            if node.is_variable():
                return self.reference_converter.convert_name_reference(node.get_variable())
            if node.is_function_call():
                return self.print_function_call(node.get_function_call())
        else:
            if isinstance(node, ASTExpression):
                if node.is_unary_operator():
                    op = self.reference_converter.convert_unary_op(node.get_unary_operator())
                    rhs = self.print_expression(node.get_expression())
                    return op % rhs
                if node.is_encapsulated:
                    return self.reference_converter.convert_encapsulated() % self.print_expression(node.get_expression())
                if node.is_logical_not:
                    op = self.reference_converter.convert_logical_not()
                    rhs = self.print_expression(node.get_expression())
                    return op % rhs
                if node.is_compound_expression():
                    lhs = self.print_expression(node.get_lhs())
                    op = self.reference_converter.convert_binary_op(node.get_binary_operator())
                    rhs = self.print_expression(node.get_rhs())
                    return op % (lhs, rhs)
                if node.is_ternary_operator():
                    condition = self.print_expression(node.get_condition())
                    if_true = self.print_expression(node.get_if_true())
                    if_not = self.print_expression(node.if_not)
                    return self.reference_converter.convert_ternary_operator() % (condition, if_true, if_not)
            else:
                raise RuntimeError('Unsupported rhs in rhs pretty printer (%s)!' % str(node))