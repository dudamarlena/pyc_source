# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/meta_model/ast_ode_function.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 4100 bytes
from pynestml.meta_model.ast_expression_node import ASTExpressionNode
from pynestml.meta_model.ast_node import ASTNode

class ASTOdeFunction(ASTNode):
    __doc__ = "\n    Stores a single declaration of a ode function, e.g.,\n        function v_init mV = V_m - 50 mV\n    Grammar:\n        odeFunction : (recordable='recordable')? 'function' variableName=NAME datatype '=' rhs;\n    Attributes:\n        is_recordable = False\n        variable_name = None\n        data_type = None\n        expression = None\n    "

    def __init__(self, is_recordable=False, variable_name=None, data_type=None, expression=None, source_position=None):
        """
        Standard constructor.
        :param is_recordable: (optional) is this function recordable or not.
        :type is_recordable: bool
        :param variable_name: the name of the variable.
        :type variable_name: str
        :param data_type: the datatype of the function.
        :type data_type: ast_data_type
        :param expression: the computation rhs.
        :type expression: ast_expression
        :param source_position: the position of this element in the source file.
        :type source_position: ASTSourceLocation.
        """
        super(ASTOdeFunction, self).__init__(source_position)
        self.is_recordable = is_recordable
        self.variable_name = variable_name
        self.data_type = data_type
        self.expression = expression

    def get_variable_name(self):
        """
        Returns the variable name.
        :return: the name of the variable.
        :rtype: str
        """
        return self.variable_name

    def get_data_type(self):
        """
        Returns the data type as an object of ASTDatatype.
        :return: the type as an object of ASTDatatype.
        :rtype: ast_data_type
        """
        return self.data_type

    def get_expression(self):
        """
        Returns the rhs as an object of ASTExpression.
        :return: the rhs as an object of ASTExpression.
        :rtype: ast_expression
        """
        return self.expression

    def get_parent(self, ast):
        """
        Indicates whether a this node contains the handed over node.
        :param ast: an arbitrary meta_model node.
        :type ast: AST_
        :return: AST if this or one of the child nodes contains the handed over element.
        :rtype: AST_ or None
        """
        if self.get_data_type() is ast:
            return self
        if self.get_data_type().get_parent(ast) is not None:
            return self.get_data_type().get_parent(ast)
        if self.get_expression() is ast:
            return self
        if self.get_expression().get_parent(ast) is not None:
            return self.get_expression().get_parent(ast)

    def equals(self, other):
        """
        The equals method.
        :param other: a different object.
        :type other: object
        :return: True if equal, otherwise False.
        :rtype: bool
        """
        if not isinstance(other, ASTOdeFunction):
            return False
        if self.is_recordable != other.is_recordable:
            return False
        if self.get_variable_name() != other.get_variable_name():
            return False
        if not self.get_data_type().equals(other.get_data_type()):
            return False
        return self.get_expression().equals(other.get_expression())