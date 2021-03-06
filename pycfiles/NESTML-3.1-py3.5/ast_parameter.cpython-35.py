# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/meta_model/ast_parameter.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 3407 bytes
from pynestml.meta_model.ast_data_type import ASTDataType
from pynestml.meta_model.ast_node import ASTNode

class ASTParameter(ASTNode):
    __doc__ = '\n    This class is used to store a single function parameter definition.\n    ASTParameter represents singe:\n      output: spike\n    @attribute compartments Lists with compartments.\n    Grammar:\n        parameter : NAME datatype;\n    Attributes:\n        name (str): The name of the parameter.\n        data_type (ASTDataType): The data type of the parameter.\n    '

    def __init__(self, name=None, data_type=None, source_position=None):
        """
        Standard constructor.
        :param name: the name of the parameter.
        :type name: str
        :param data_type: the type of the parameter.
        :type data_type: ASTDataType
        :param source_position: the position of this element in the source file.
        :type source_position: ASTSourceLocation.
        """
        assert name is not None and isinstance(name, str), '(PyNestML.AST.Parameter) No or wrong type of name provided (%s)!' % type(name)
        assert data_type is not None and isinstance(data_type, ASTDataType), '(PyNestML.AST.Parameter) No or wrong type of datatype provided (%s)!' % type(data_type)
        super(ASTParameter, self).__init__(source_position)
        self.data_type = data_type
        self.name = name

    def get_name(self):
        """
        Returns the name of the parameter.
        :return: the name of the parameter.
        :rtype: str
        """
        return self.name

    def get_data_type(self):
        """
        Returns the data type of the parameter.
        :return: the data type of the parameter.
        :rtype: ASTDataType
        """
        return self.data_type

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

    def equals(self, other):
        """
        The equals method.
        :param other: a different object.
        :type other: object
        :return: True if equal, otherwise False.
        :rtype: bool
        """
        if not isinstance(other, ASTParameter):
            return False
        return self.get_name() == other.get_name() and self.get_data_type().equals(other.get_data_type())