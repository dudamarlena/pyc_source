# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/meta_model/ast_equations_block.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 5241 bytes
from pynestml.meta_model.ast_node import ASTNode
from pynestml.meta_model.ast_ode_equation import ASTOdeEquation
from pynestml.meta_model.ast_ode_function import ASTOdeFunction
from pynestml.meta_model.ast_ode_shape import ASTOdeShape

class ASTEquationsBlock(ASTNode):
    __doc__ = "\n    This class is used to store an equations block.\n    ASTEquationsBlock a special function definition:\n       equations:\n         G = (e/tau_syn) * t * exp(-1/tau_syn*t)\n         V' = -1/Tau * V + 1/C_m * (I_sum(G, spikes) + I_e + currents)\n       end\n     @attribute odeDeclaration Block with equations and differential equations.\n     Grammar:\n          equationsBlock:\n            'equations'\n            BLOCK_OPEN\n              (odeFunction|odeEquation|odeShape|NEWLINE)+\n            BLOCK_CLOSE;\n    Attributes:\n        declarations = None\n    "

    def __init__(self, declarations, source_position):
        """
        Standard constructor.
        :param declarations: a block of definitions.
        :type declarations: ast_block
        :param source_position: the position of this element in the source file.
        :type source_position: ASTSourceLocation.
        """
        assert declarations is not None and isinstance(declarations, list), '(PyNestML.AST.EquationsBlock) No or wrong type of declarations provided (%s)!' % type(declarations)
        for decl in declarations:
            if not (decl is not None and (isinstance(decl, ASTOdeShape) or isinstance(decl, ASTOdeEquation) or isinstance(decl, ASTOdeFunction))):
                raise AssertionError('(PyNestML.AST.EquationsBlock) No or wrong type of ode-element provided (%s)' % type(decl))

        super(ASTEquationsBlock, self).__init__(source_position)
        self.declarations = declarations

    def get_declarations(self):
        """
        Returns the block of definitions.
        :return: the block
        :rtype: list(ASTOdeFunction|ASTOdeEquation|ASTOdeShape)
        """
        return self.declarations

    def get_parent(self, ast):
        """
        Indicates whether a this node contains the handed over node.
        :param ast: an arbitrary meta_model node.
        :type ast: AST_
        :return: AST if this or one of the child nodes contains the handed over element.
        :rtype: AST_ or None
        """
        for decl in self.get_declarations():
            if decl is ast:
                return self
            if decl.get_parent(ast) is not None:
                return decl.get_parent(ast)

    def get_ode_equations(self):
        """
        Returns a list of all ode equations in this block.
        :return: a list of all ode equations.
        :rtype: list(ASTOdeEquations)
        """
        ret = list()
        for decl in self.get_declarations():
            if isinstance(decl, ASTOdeEquation):
                ret.append(decl)

        return ret

    def get_ode_shapes(self):
        """
        Returns a list of all ode shapes in this block.
        :return: a list of all ode shapes.
        :rtype: list(ASTOdeShape)
        """
        ret = list()
        for decl in self.get_declarations():
            if isinstance(decl, ASTOdeShape):
                ret.append(decl)

        return ret

    def get_ode_functions(self):
        """
        Returns a list of all ode functions in this block.
        :return: a list of all ode shapes.
        :rtype: list(ASTOdeShape)
        """
        ret = list()
        for decl in self.get_declarations():
            if isinstance(decl, ASTOdeFunction):
                ret.append(decl)

        return ret

    def clear(self):
        """
        Deletes all declarations as stored in this block.
        """
        del self.declarations
        self.declarations = list()

    def equals(self, other):
        """
        The equals method.
        :param other: a different object.
        :type other: object
        :return: True if equal, otherwise False.
        :rtype: bool
        """
        if not isinstance(other, ASTEquationsBlock):
            return False
        if len(self.get_declarations()) != len(other.get_declarations()):
            return False
        my_declarations = self.get_declarations()
        your_declarations = other.get_declarations()
        for i in range(0, len(my_declarations)):
            if not my_declarations[i].equals(your_declarations[i]):
                return False

        return True