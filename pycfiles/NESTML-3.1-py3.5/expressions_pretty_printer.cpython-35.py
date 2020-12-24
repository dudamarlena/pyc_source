# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/codegeneration/expressions_pretty_printer.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 7433 bytes
from pynestml.codegeneration.i_reference_converter import IReferenceConverter
from pynestml.codegeneration.idempotent_reference_converter import IdempotentReferenceConverter
from pynestml.meta_model.ast_expression import ASTExpression
from pynestml.meta_model.ast_expression_node import ASTExpressionNode
from pynestml.meta_model.ast_function_call import ASTFunctionCall
from pynestml.meta_model.ast_simple_expression import ASTSimpleExpression
from pynestml.symbols.predefined_functions import PredefinedFunctions
from pynestml.utils.ast_utils import ASTUtils

class ExpressionsPrettyPrinter(object):
    __doc__ = '\n    Converts expressions to the executable platform dependent code. By using different\n    referenceConverters for the handling of variables, names, and functions can be adapted. For this,\n    implement own IReferenceConverter specialisation.\n    This class is used to transform only parts of the procedural language and not nestml in whole.\n    '

    def __init__(self, reference_converter=None, types_printer=None):
        if reference_converter is not None:
            self.reference_converter = reference_converter
        else:
            self.reference_converter = IdempotentReferenceConverter()
        if types_printer is not None:
            self.types_printer = types_printer
        else:
            self.types_printer = TypesPrinter()

    def print_expression(self, node, prefix=''):
        """Print an expression.

        Parameters
        ----------
        node : ASTExpressionNode
            The expression node to print.
        prefix : str
            *See documentation for the function print_function_call().*

        Returns
        -------
        s : str
            The expression string.
        """
        if node.get_implicit_conversion_factor() is not None:
            return str(node.get_implicit_conversion_factor()) + ' * (' + self._ExpressionsPrettyPrinter__do_print(node) + ')'
        else:
            return self._ExpressionsPrettyPrinter__do_print(node, prefix=prefix)

    def __do_print(self, node, prefix=''):
        if isinstance(node, ASTSimpleExpression):
            if node.has_unit():
                return self.types_printer.pretty_print(node.get_numeric_literal()) + '*' + self.reference_converter.convert_name_reference(node.get_variable())
            if node.is_numeric_literal():
                return str(node.get_numeric_literal())
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
                return self.print_function_call(node.get_function_call(), prefix=prefix)
        else:
            if isinstance(node, ASTExpression):
                if node.is_unary_operator():
                    op = self.reference_converter.convert_unary_op(node.get_unary_operator())
                    rhs = self.print_expression(node.get_expression(), prefix=prefix)
                    return op % rhs
                if node.is_encapsulated:
                    return self.reference_converter.convert_encapsulated() % self.print_expression(node.get_expression(), prefix=prefix)
                if node.is_logical_not:
                    op = self.reference_converter.convert_logical_not()
                    rhs = self.print_expression(node.get_expression(), prefix=prefix)
                    return op % rhs
                if node.is_compound_expression():
                    lhs = self.print_expression(node.get_lhs(), prefix=prefix)
                    op = self.reference_converter.convert_binary_op(node.get_binary_operator())
                    rhs = self.print_expression(node.get_rhs(), prefix=prefix)
                    return op % (lhs, rhs)
                if node.is_ternary_operator():
                    condition = self.print_expression(node.get_condition(), prefix=prefix)
                    if_true = self.print_expression(node.get_if_true(), prefix=prefix)
                    if_not = self.print_expression(node.if_not, prefix=prefix)
                    return self.reference_converter.convert_ternary_operator() % (condition, if_true, if_not)
            else:
                raise RuntimeError('Unsupported rhs in rhs pretty printer!')

    def print_function_call(self, function_call, prefix=''):
        """Print a function call, including bracketed arguments list.

        Parameters
        ----------
        node : ASTFunctionCall
            The function call node to print.
        prefix : str
            Optional string that will be prefixed to the function call. For example, to refer to a function call in the class "node", use a prefix equal to "node." or "node->".

            Predefined functions will not be prefixed.

        Returns
        -------
        s : str
            The function call string.
        """
        function_name = self.reference_converter.convert_function_call(function_call, prefix=prefix)
        if ASTUtils.needs_arguments(function_call):
            return function_name.format(*self.print_function_call_argument_list(function_call, prefix=prefix))
        else:
            return function_name

    def print_function_call_argument_list(self, function_call, prefix=''):
        ret = []
        for arg in function_call.get_args():
            ret.append(self.print_expression(arg, prefix=prefix))

        return tuple(ret)


class TypesPrinter(object):
    __doc__ = '\n    Returns a processable format of the handed over element.\n    '

    @classmethod
    def pretty_print(cls, element):
        assert element is not None, '(PyNestML.CodeGeneration.PrettyPrinter) No element provided (%s)!' % element
        if isinstance(element, bool) and element:
            return 'true'
        if isinstance(element, bool) and not element:
            return 'false'
        if isinstance(element, int) or isinstance(element, float):
            return str(element)