# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/meta_model/ast_declaration.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 8087 bytes
from pynestml.meta_model.ast_data_type import ASTDataType
from pynestml.meta_model.ast_expression import ASTExpression
from pynestml.meta_model.ast_node import ASTNode

class ASTDeclaration(ASTNode):
    __doc__ = "\n    This class is used to store declarations.\n    ASTDeclaration A variable declaration. It can be a simple declaration defining one or multiple variables:\n    'a,b,c real = 0'. Or an function declaration 'function a = b + c'.\n    @attribute hide is true iff. declaration is not traceable.\n    @attribute function is true iff. declaration is an function.\n    @attribute vars          List with variables\n    @attribute Datatype      Obligatory data type, e.g. 'real' or 'mV/s'\n    @attribute sizeParameter An optional array parameter. E.g. 'tau_syn ms[n_receptors]'\n    @attribute expr An optional initial rhs, e.g. 'a real = 10+10'\n    @attribute invariants List with optional invariants.\n    Grammar:\n        declaration :\n            ('recordable')? ('function')?\n            variable (',' variable)*\n            datatype\n            ('[' sizeParameter=NAME ']')?\n            ( '=' rhs)?\n            ('[[' invariant=rhs ']]')?;\n    Attributes:\n        is_recordable = False\n        is_function = False\n        variables = None\n        data_type = None\n        size_parameter = None\n        expression = None\n        invariant = None\n    "

    def __init__(self, is_recordable=False, is_function=False, _variables=list(), data_type=None, size_parameter=None, expression=None, invariant=None, source_position=None):
        """
        Standard constructor.
        :param is_recordable: is a recordable declaration.
        :type is_recordable: bool
        :param is_function: is a function declaration.
        :type is_function: bool
        :param _variables: a list of variables.
        :type _variables: list(ASTVariable)
        :param data_type: the data type.
        :type data_type: ast_data_type
        :param size_parameter: an optional size parameter.
        :type size_parameter: str
        :param expression: an optional right-hand side rhs.
        :type expression: ASTExpression
        :param invariant: a optional invariant.
        :type invariant: ASTExpression.
        :param source_position: the position of this element in the source file.
        :type source_position: ASTSourceLocation.
        """
        super(ASTDeclaration, self).__init__(source_position)
        self.is_recordable = is_recordable
        self.is_function = is_function
        self.variables = _variables
        self.data_type = data_type
        self.size_parameter = size_parameter
        self.expression = expression
        self.invariant = invariant

    def get_variables(self):
        """
        Returns the set of left-hand side variables.
        :return: a list of variables.
        :rtype: list(ASTVariables)
        """
        return self.variables

    def get_data_type(self):
        """
        Returns the data type.
        :return: a data type object.
        :rtype: ASTDataType
        """
        return self.data_type

    def has_size_parameter(self):
        """
        Returns whether the declaration has a size parameter or not.
        :return: True if has size parameter, else False.
        :rtype: bool
        """
        return self.size_parameter is not None

    def get_size_parameter(self):
        """
        Returns the size parameter.
        :return: the size parameter.
        :rtype: str
        """
        return self.size_parameter

    def set_size_parameter(self, _parameter):
        """
        Updates the current size parameter to a new value.
        :param _parameter: the size parameter
        :type _parameter: str
        """
        assert _parameter is not None and isinstance(_parameter, str), '(PyNestML.AST.Declaration) No or wrong type of size parameter provided (%s)!' % type(_parameter)
        self.size_parameter = _parameter

    def has_expression(self):
        """
        Returns whether the declaration has a right-hand side rhs or not.
        :return: True if right-hand side rhs declared, else False.
        :rtype: bool
        """
        return self.expression is not None

    def get_expression(self):
        """
        Returns the right-hand side rhs.
        :return: the right-hand side rhs.
        :rtype: ASTExpression
        """
        return self.expression

    def set_expression(self, expr):
        self.expression = expr

    def has_invariant(self):
        """
        Returns whether the declaration has a invariant or not.
        :return: True if has invariant, otherwise False.
        :rtype: bool
        """
        return self.invariant is not None

    def get_invariant(self):
        """
        Returns the invariant.
        :return: the invariant
        :rtype: ASTExpression
        """
        return self.invariant

    def get_parent(self, ast):
        """
        Indicates whether a this node contains the handed over node.
        :param ast: an arbitrary meta_model node.
        :type ast: AST_
        :return: AST if this or one of the child nodes contains the handed over element.
        :rtype: AST_ or None
        """
        for var in self.get_variables():
            if var is ast:
                return self
            if var.get_parent(ast) is not None:
                return var.get_parent(ast)

        if self.get_data_type() is ast:
            return self
        if self.get_data_type().get_parent(ast) is not None:
            return self.get_data_type().get_parent(ast)
        if self.has_expression():
            if self.get_expression() is ast:
                return self
            if self.get_expression().get_parent(ast) is not None:
                pass
            return self.get_expression().get_parent(ast)
        if self.has_invariant():
            if self.get_invariant() is ast:
                return self
            if self.get_invariant().get_parent(ast) is not None:
                pass
            return self.get_invariant().get_parent(ast)

    def equals(self, other):
        """
        The equals method.
        :param other: a different object.
        :type other: object
        :return: True if equal, otherwise False.
        :rtype: bool
        """
        if not isinstance(other, ASTDeclaration):
            return False
        if not (self.is_function == other.is_function and self.is_recordable == other.is_recordable):
            return False
        if self.get_size_parameter() != other.get_size_parameter():
            return False
        if len(self.get_variables()) != len(other.get_variables()):
            return False
        my_vars = self.get_variables()
        your_vars = other.get_variables()
        for i in range(0, len(my_vars)):
            if not my_vars[i].equals(your_vars[i]):
                return False

        if self.has_invariant() + other.has_invariant() == 1:
            return False
        if self.has_invariant() and other.has_invariant() and not self.get_invariant().equals(other.get_invariant()):
            return False
        return self.get_data_type().equals(other.get_data_type()) and self.get_expression().equals(other.get_expression())