# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/meta_model/ast_block_with_variables.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 5097 bytes
from pynestml.meta_model.ast_node import ASTNode

class ASTBlockWithVariables(ASTNode):
    __doc__ = "\n    This class is used to store a block of variable declarations.\n    ast_block_with_variables.py represent a block with variables, e.g.:\n        state:\n          y0, y1, y2, y3 mV [y1 > 0; y2 > 0]\n        end\n\n    attribute state true: if the varblock is a state.\n    attribute parameter: true if the varblock is a parameter.\n    attribute internal: true if the varblock is a state internal.\n    attribute AliasDecl: a list with variable declarations\n    Grammar:\n         blockWithVariables:\n            blockType=('state'|'parameters'|'internals'|'initial_values')\n            BLOCK_OPEN\n              (declaration | NEWLINE)*\n            BLOCK_CLOSE;\n    Attributes:\n        is_state = False\n        is_parameters = False\n        is_internals = False\n        is_initial_values = False\n        declarations = None\n    "

    def __init__(self, is_state=False, is_parameters=False, is_internals=False, is_initial_values=False, declarations=list(), source_position=None):
        """
        Standard constructor.
        :param is_state: is a state block.
        :type is_state: bool
        :param is_parameters: is a parameter block.
        :type is_parameters: bool 
        :param is_internals: is an internals block.
        :type is_internals: bool
        :param is_initial_values: is an initial values block.
        :type is_initial_values: bool
        :param declarations: a list of declarations.
        :type declarations: list(ASTDeclaration)
        :param source_position: the position of this element in the source file.
        :type source_position: ASTSourceLocation.
        """
        if not is_internals:
            if not is_parameters:
                if not is_state:
                    assert is_initial_values, '(PyNESTML.AST.BlockWithVariables) Type of variable block specified!'
                    assert is_internals + is_parameters + is_state + is_initial_values == 1, '(PyNestML.AST.BlockWithVariables) Type of block ambiguous!'
                    if not declarations is None:
                        assert isinstance(declarations, list), '(PyNESTML.AST.BlockWithVariables) Wrong type of declaration provided (%s)!' % type(declarations)
                        super(ASTBlockWithVariables, self).__init__(source_position)
                        self.declarations = declarations
                        self.is_internals = is_internals
                        self.is_parameters = is_parameters
                        self.is_initial_values = is_initial_values
                        self.is_state = is_state

    def get_declarations(self):
        """
        Returns the set of stored declarations.
        :return: set of declarations
        :rtype: set(ASTDeclaration)
        """
        return self.declarations

    def clear(self):
        """
        Clears the list of declarations in this block.
        """
        del self.declarations
        self.declarations = list()

    def get_parent(self, ast=None):
        """
        Indicates whether a this node contains the handed over node.
        :param ast: an arbitrary meta_model node.
        :type ast: AST_
        :return: AST if this or one of the child nodes contains the handed over element.
        :rtype: AST_ or None
        """
        for stmt in self.get_declarations():
            if stmt is ast:
                return self
            if stmt.get_parent(ast) is not None:
                return stmt.get_parent(ast)

    def equals(self, other=None):
        """
        The equals method.
        :param other: a different object.
        :type other: object
        :return: True if equal, otherwise False
        :rtype: bool
        """
        if not isinstance(other, ASTBlockWithVariables):
            return False
        if not (self.is_initial_values == other.is_initial_values and self.is_internals == other.is_internals and self.is_parameters == other.is_parameters and self.is_state == other.is_state):
            return False
        if len(self.get_declarations()) != len(other.get_declarations()):
            return False
        my_declarations = self.get_declarations()
        your_declarations = other.get_declarations()
        for i in range(0, len(my_declarations)):
            if not my_declarations[i].equals(your_declarations[i]):
                return False

        return True