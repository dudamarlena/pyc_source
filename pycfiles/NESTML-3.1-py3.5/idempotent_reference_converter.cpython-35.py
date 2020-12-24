# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/codegeneration/idempotent_reference_converter.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 3892 bytes
from pynestml.codegeneration.i_reference_converter import IReferenceConverter
from pynestml.meta_model.ast_function_call import ASTFunctionCall
from pynestml.meta_model.ast_variable import ASTVariable
from pynestml.utils.ast_utils import ASTUtils

class IdempotentReferenceConverter(IReferenceConverter):
    __doc__ = '\n    Returns the same input as output, i.e., an identity mapping of elements is preformed. This converter is used\n    whenever comments have to be printed, in order to preserve the initial PyNestML syntax.\n    '

    def convert_unary_op(self, ast_unary_operator):
        """
        Returns the same string.
        :param ast_unary_operator: a single unary operator string.
        :type ast_unary_operator: ast_unary_operator
        :return: the same string
        :rtype: str
        """
        return str(ast_unary_operator) + '%s'

    def convert_name_reference(self, ast_variable):
        """
        Returns the same string
        :param ast_variable: a single variable
        :type ast_variable: ASTVariable
        :return: the same string
        :rtype: str
        """
        return ast_variable.get_complete_name()

    def convert_function_call(self, function_call, prefix=''):
        """Return the function call in NESTML syntax.

        Parameters
        ----------
        function_call : ASTFunctionCall
            The function call node to convert.
        prefix : str
            The prefix argument is not relevant for rendering NESTML syntax and will be ignored.

        Returns
        -------
        s : str
            The function call string in NESTML syntax.
        """
        result = function_call.get_name()
        if ASTUtils.needs_arguments(function_call):
            n_args = len(function_call.get_args())
            result += '(' + ', '.join(['{!s}' for _ in range(n_args)]) + ')'
        else:
            result += '()'
        return result

    def convert_binary_op(self, ast_binary_operator):
        """
        Returns the same binary operator back.
        :param ast_binary_operator:  a single binary operator
        :type ast_binary_operator: str
        :return: the same binary operator
        :rtype: str
        """
        return '%s' + str(ast_binary_operator) + '%s'

    def convert_constant(self, constant_name):
        """
        Returns the same string back.
        :param constant_name: a constant name
        :type constant_name: str
        :return: the same string
        :rtype: str
        """
        return constant_name

    def convert_ternary_operator(self):
        """
        Converts the ternary operator to its initial shape.
        :return: a string representation
        :rtype: str
        """
        return '(%s)?(%s):(%s)'

    def convert_logical_operator(self, op):
        return str(op)

    def convert_arithmetic_operator(self, op):
        return str(op)

    def convert_encapsulated(self):
        return '(%s)'

    def convert_comparison_operator(self, op):
        return str(op)

    def convert_logical_not(self):
        return 'not'

    def convert_bit_operator(self, op):
        return str(op)