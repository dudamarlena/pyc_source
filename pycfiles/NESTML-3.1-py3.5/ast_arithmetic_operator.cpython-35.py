# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/meta_model/ast_arithmetic_operator.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 2803 bytes
from pynestml.meta_model.ast_node import ASTNode

class ASTArithmeticOperator(ASTNode):
    __doc__ = '\n    This class is used to store a single arithmetic operator, e.g. +.\n    No grammar. This part is defined outside the grammar to make processing and storing of models easier and \n    comprehensible.\n    Attributes:\n        is_times_op = False  # type: bool\n        is_div_op = False  # type:bool\n        is_modulo_op = False  # type:bool\n        is_plus_op = False  # type:bool\n        is_minus_op = False  # type: bool\n        is_pow_op = False  # type:bool\n    '

    def __init__(self, is_times_op, is_div_op, is_modulo_op, is_plus_op, is_minus_op, is_pow_op, source_position):
        assert is_times_op + is_div_op + is_modulo_op + is_plus_op + is_minus_op + is_pow_op == 1, '(PyNESTML.AST.ArithmeticOperator) Type of arithmetic operator not specified!'
        super(ASTArithmeticOperator, self).__init__(source_position)
        self.is_times_op = is_times_op
        self.is_div_op = is_div_op
        self.is_modulo_op = is_modulo_op
        self.is_plus_op = is_plus_op
        self.is_minus_op = is_minus_op
        self.is_pow_op = is_pow_op

    def get_parent(self, ast):
        """
        Indicates whether a this node contains the handed over node.
        :param ast: an arbitrary meta_model node.
        :type ast: AST_
        :return: AST if this or one of the child nodes contains the handed over element.
        :rtype: AST_ or None
        """
        pass

    def equals(self, other):
        """
        The equality method.
        """
        if not isinstance(other, ASTArithmeticOperator):
            return False
        return self.is_times_op == other.is_times_op and self.is_div_op == other.is_div_op and self.is_modulo_op == other.is_modulo_op and self.is_plus_op == other.is_plus_op and self.is_minus_op == other.is_minus_op and self.is_pow_op == other.is_pow_op