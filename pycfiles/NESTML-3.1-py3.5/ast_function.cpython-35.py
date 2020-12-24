# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/meta_model/ast_function.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 6123 bytes
from copy import copy
from pynestml.meta_model.ast_node import ASTNode

class ASTFunction(ASTNode):
    __doc__ = "\n    This class is used to store a user-defined function.\n    ASTFunction a function definition:\n      function set_V_m(v mV):\n        y3 = v - E_L\n      end\n    @attribute name Functionname.\n    @attribute parameter A single parameter.\n    @attribute returnType Complex return type, e.g. String\n    @attribute primitiveType Primitive return type, e.g. int\n    @attribute block Implementation of the function.\n    Grammar:\n    function: 'function' NAME '(' (parameter (',' parameter)*)? ')' (returnType=datatype)?\n           BLOCK_OPEN\n             block\n           BLOCK_CLOSE;\n    Attributes:\n        name = None\n        parameters = None\n        return_type = None\n        block = None\n        # the corresponding type symbol\n        type_symbol = None\n    "

    def __init__(self, name, parameters, return_type, block, source_position):
        """
        Standard constructor.
        :param name: the name of the defined function.
        :type name: str
        :param parameters: (Optional) Set of parameters.
        :type parameters: list(ASTParameter)
        :param return_type: (Optional) Return type.
        :type return_type: ast_data_type
        :param block: a block of declarations.
        :type block: ast_block
        :param source_position: the position of this element in the source file.
        :type source_position: ASTSourceLocation.
        """
        super(ASTFunction, self).__init__(source_position)
        self.block = block
        self.return_type = return_type
        self.parameters = parameters
        self.name = name

    def get_name(self):
        """
        Returns the name of the function.
        :return: the name of the function.
        :rtype: str
        """
        return self.name

    def has_parameters(self):
        """
        Returns whether parameters have been defined.
        :return: True if parameters defined, otherwise False.
        :rtype: bool
        """
        return self.parameters is not None and len(self.parameters) > 0

    def get_parameters(self):
        """
        Returns the list of parameters.
        :return: a parameters object containing the list.
        :rtype: list(ASTParameter)
        """
        return self.parameters

    def has_return_type(self):
        """
        Returns whether return a type has been defined.
        :return: True if return type defined, otherwise False.
        :rtype: bool
        """
        return self.return_type is not None

    def get_return_type(self):
        """
        Returns the return type of function.
        :return: the return type 
        :rtype: ast_data_type
        """
        return self.return_type

    def get_block(self):
        """
        Returns the block containing the definitions.
        :return: the block of the definitions.
        :rtype: ast_block
        """
        return self.block

    def get_type_symbol(self):
        """
        Returns the type symbol of this rhs.
        :return: a single type symbol.
        :rtype: type_symbol
        """
        return copy(self.type_symbol)

    def set_type_symbol(self, type_symbol):
        """
        Updates the current type symbol to the handed over one.
        :param type_symbol: a single type symbol object.
        :type type_symbol: type_symbol
        """
        self.type_symbol = type_symbol

    def get_parent(self, ast):
        """
        Indicates whether a this node contains the handed over node.
        :param ast: an arbitrary meta_model node.
        :type ast: AST_
        :return: AST if this or one of the child nodes contains the handed over element.
        :rtype: AST_ or None
        """
        for param in self.get_parameters():
            if param is ast:
                return self
            if param.get_parent(ast) is not None:
                return param.get_parent(ast)

        if self.has_return_type():
            if self.get_return_type() is ast:
                return self
            if self.get_return_type().get_parent(ast) is not None:
                pass
            return self.get_return_type().get_parent(ast)
        if self.get_block() is ast:
            return self
        if self.get_block().get_parent(ast) is not None:
            return self.get_block().get_parent(ast)

    def equals(self, other):
        """
        The equals method.
        :param other: a different object.
        :type other: object
        :return: True if equal, otherwise False.
        :rtype: bool
        """
        if not isinstance(other, ASTFunction):
            return False
        if self.get_name() != other.get_name():
            return False
        if len(self.get_parameters()) != len(other.get_parameters()):
            return False
        my_parameters = self.get_parameters()
        your_parameters = other.get_parameters()
        for i in range(0, len(my_parameters)):
            if not my_parameters[i].equals(your_parameters[i]):
                return False

        if self.has_return_type() + other.has_return_type() == 1:
            return False
        if self.has_return_type() and other.has_return_type() and not self.get_return_type().equals(other.get_return_type()):
            return False
        return self.get_block().equals(other.get_block())