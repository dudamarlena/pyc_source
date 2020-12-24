# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/meta_model/ast_simple_expression.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 10478 bytes
from pynestml.meta_model.ast_expression_node import ASTExpressionNode
from pynestml.meta_model.ast_function_call import ASTFunctionCall
from pynestml.meta_model.ast_variable import ASTVariable

class ASTSimpleExpression(ASTExpressionNode):
    __doc__ = "\n    This class is used to store a simple rhs, e.g. +42mV.\n    ASTSimpleExpression, consisting of a single element without combining operator, e.g.,10mV, inf, V_m.\n    Grammar:\n    simpleExpression : functionCall\n                   | BOOLEAN_LITERAL // true & false ;\n                   | (UNSIGNED_INTEGER | FLOAT) (variable)?\n                   | isInf='inf'\n                   | STRING_LITERAL\n                   | variable;\n    Attributes:\n        function_call: A function call reference.\n        numeric_literal: A numeric literal.\n        variable: A variable reference.\n        is_boolean_true (bool): True if this is a boolean true literal.\n        is_boolean_false (bool): True if this is a boolean false literal.\n        is_inf_literal (bool): True if this is a infinity literal.\n        string (str): A string literal.\n\n    "

    def __init__(self, function_call=None, boolean_literal=None, numeric_literal=None, is_inf=False, variable=None, string=None, source_position=None):
        """
        Standard constructor.
        :param function_call: a function call.
        :type function_call: ASTFunctionCall
        :param boolean_literal: a boolean value.
        :type boolean_literal: bool
        :param numeric_literal: a numeric value.
        :type numeric_literal: float/int
        :param is_inf: is inf symbol.
        :type is_inf: bool
        :param variable: a variable object.
        :type variable: ASTVariable
        :param string: a single string literal
        :type string: str
        :param source_position: the position of this element in the source file.
        :type source_position: ASTSourceLocation.
        """
        if not function_call is None:
            assert isinstance(function_call, ASTFunctionCall), '(PyNestML.AST.SimpleExpression) Not a function call provided (%s)!' % type(function_call)
            if not boolean_literal is None:
                assert isinstance(boolean_literal, bool), '(PyNestML.AST.SimpleExpression) Not a bool provided (%s)!' % type(boolean_literal)
                if not is_inf is None:
                    assert isinstance(is_inf, bool), '(PyNestML.AST.SimpleExpression) Not a bool provided (%s)!' % type(is_inf)
                    if not variable is None:
                        assert isinstance(variable, ASTVariable), '(PyNestML.AST.SimpleExpression) Not a variable provided (%s)!' % type(variable)
                        if not numeric_literal is None:
                            if not isinstance(numeric_literal, int):
                                assert isinstance(numeric_literal, float), '(PyNestML.AST.SimpleExpression) Not a number provided (%s)!' % type(numeric_literal)
                                if not string is None:
                                    assert isinstance(string, str), '(PyNestML.AST.SimpleExpression) Not a string provided (%s)!' % type(string)
                                    super(ASTSimpleExpression, self).__init__(source_position)
                                    self.function_call = function_call
                                    self.is_boolean_true = False
                                    self.is_boolean_false = False
                                    if boolean_literal is not None:
                                        if boolean_literal:
                                            self.is_boolean_true = True
                                        else:
                                            self.is_boolean_false = True
                                        self.numeric_literal = numeric_literal
                                        self.is_inf_literal = is_inf
                                        self.variable = variable
                                        self.string = string

    def is_function_call(self):
        """
        Returns whether it is a function call or not.
        :return: True if function call, otherwise False.
        :rtype: bool
        """
        return self.function_call is not None

    def get_function_call(self):
        """
        Returns the function call object.
        :return: the function call object.
        :rtype: ASTFunctionCall
        """
        return self.function_call

    def get_function_calls(self):
        """
        This function is used for better interactions with the general rhs meta_model class.
        :return: returns a single list with this function call if such an exists, otherwise an empty list
        :rtype: list(ASTFunctionCall)
        """
        ret = list()
        if self.is_function_call():
            ret.append(self.get_function_call())
        return ret

    def is_numeric_literal(self):
        """
        Returns whether it is a numeric literal or not.
        :return: True if numeric literal, otherwise False.
        :rtype: bool
        """
        return self.numeric_literal is not None

    def get_numeric_literal(self):
        """
        Returns the value of the numeric literal.
        :return: the value of the numeric literal.
        :rtype: int/float
        """
        return self.numeric_literal

    def is_variable(self):
        """
        Returns whether it is a variable or not.
        :return: True if has a variable, otherwise False.
        :rtype: bool
        """
        return self.variable is not None and self.numeric_literal is None

    def get_variables(self):
        """
        This function is used for better interactions with the general rhs meta_model class.
        :return: returns a single list with this variable if such an exists, otherwise an empty list
        :rtype: list(ASTVariable)
        """
        ret = list()
        if self.is_variable():
            ret.append(self.get_variable())
        return ret

    def has_unit(self):
        """
        Returns whether this is a numeric literal with a defined unit.
        :return: True if numeric literal with unit, otherwise False. 
        :rtype: bool
        """
        return self.variable is not None and self.numeric_literal is not None

    def get_units(self):
        """
        This function is used for better interactions with the general rhs meta_model class.
        :return: returns a single list with unit if such an exists, otherwise an empty list
        :rtype: list(ASTVariable)
        """
        ret = list()
        if self.has_unit():
            ret.append(self.get_variable())
        return ret

    def get_variable(self):
        """
        Returns the variable.
        :return: the variable object.
        :rtype: ASTVariable
        """
        return self.variable

    def is_string(self):
        """
        Returns whether this simple rhs is a string.
        :return: True if string, False otherwise.
        :rtype: bool
        """
        return self.string is not None and isinstance(self.string, str)

    def get_string(self):
        """
        Returns the string as stored in this simple rhs.
        :return: a string as stored in this rhs.
        :rtype: str
        """
        return self.string

    def get_parent(self, ast):
        """
        Indicates whether a this node contains the handed over node.
        :param ast: an arbitrary meta_model node.
        :type ast: AST_
        :return: AST if this or one of the child nodes contains the handed over element.
        :rtype: AST_ or None
        """
        if self.is_function_call():
            if self.get_function_call() is ast:
                return self
            if self.get_function_call().get_parent(ast) is not None:
                pass
            return self.get_function_call().get_parent(ast)
        if self.variable is not None:
            if self.variable is ast:
                return self
            if self.variable.get_parent(ast) is not None:
                pass
            return self.variable.get_parent(ast)

    def set_variable(self, variable):
        """
        Updates the variable of this node.
        :param variable: a single variable
        :type variable: ASTVariable
        """
        if not variable is None:
            assert isinstance(variable, ASTVariable), '(PyNestML.AST.SimpleExpression) No or wrong type of variable provided (%s)!' % type(variable)
            self.variable = variable

    def set_function_call(self, function_call):
        """
        Updates the function call of this node.
        :param function_call: a single function call
        :type function_call: Union(ASTFunctionCall,None)
        """
        if not function_call is None:
            assert isinstance(function_call, ASTVariable), '(PyNestML.AST.SimpleExpression) No or wrong type of function call provided (%s)!' % type(function_call)
            self.function_call = function_call

    def equals(self, other):
        """
        The equals method.
        :param other: a different object.
        :type other: object
        :return:True if equal, otherwise False.
        :rtype: bool
        """
        if not isinstance(other, ASTSimpleExpression):
            return False
        if self.is_function_call() + other.is_function_call() == 1:
            return False
        if self.is_function_call() and other.is_function_call() and not self.get_function_call().equals(other.get_function_call()):
            return False
        if self.get_numeric_literal() != other.get_numeric_literal():
            return False
        if self.is_boolean_false != other.is_boolean_false or self.is_boolean_true != other.is_boolean_true:
            return False
        if self.is_variable() + other.is_variable() == 1:
            return False
        if self.is_variable() and other.is_variable() and not self.get_variable().equals(other.get_variable()):
            return False
        if self.is_inf_literal != other.is_inf_literal:
            return False
        if self.is_string() + other.is_string() == 1:
            return False
        if self.get_string() != other.get_string():
            return False
        return True