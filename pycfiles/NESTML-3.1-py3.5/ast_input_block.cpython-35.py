# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/meta_model/ast_input_block.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 3698 bytes
from pynestml.meta_model.ast_input_port import ASTInputPort
from pynestml.meta_model.ast_node import ASTNode

class ASTInputBlock(ASTNode):
    __doc__ = "\n    This class is used to store blocks of input definitions.\n    ASTInputBlock represents the input block, e.g.:\n        input:\n          spikeBuffer pA <- excitatory spike\n          currentBuffer pA <- current\n        end\n\n    @attribute inputPort set of input ports.\n    Grammar:\n          inputBlock: 'input'\n            BLOCK_OPEN\n              (inputPort | NEWLINE)*\n            BLOCK_CLOSE;\n    Attributes:\n        input_definitions = None\n    "

    def __init__(self, input_definitions=None, source_position=None):
        """
        Standard constructor.
        :param input_definitions:
        :type input_definitions: list(ASTInputPort)
        :param source_position: the position of this element in the source file.
        :type source_position: ASTSourceLocation.
        """
        if input_definitions is None:
            input_definitions = []
        assert input_definitions is not None and isinstance(input_definitions, list), '(PyNestML.AST.Input) No or wrong type of input definitions provided (%s)!' % type(input_definitions)
        for definition in input_definitions:
            if not (definition is not None and isinstance(definition, ASTInputPort)):
                raise AssertionError('(PyNestML.AST.Input) No or wrong type of input definition provided (%s)!' % type(definition))

        super(ASTInputBlock, self).__init__(source_position)
        self.input_definitions = input_definitions

    def get_input_ports(self):
        """
        Returns the list of input ports.
        :return: a list of input ports
        :rtype: list(ASTInputPort)
        """
        return self.input_definitions

    def get_parent(self, ast):
        """
        Indicates whether a this node contains the handed over node.
        :param ast: an arbitrary meta_model node.
        :type ast: AST_
        :return: AST if this or one of the child nodes contains the handed over element.
        :rtype: AST_ or None
        """
        for port in self.get_input_ports():
            if port is ast:
                return self
            if port.get_parent(ast) is not None:
                return port.get_parent(ast)

    def equals(self, other):
        """
        The equals method.
        :param other: a different object.
        :type other:  object
        :return: True if equal, otherwise False.
        :rtype: bool
        """
        if not isinstance(other, ASTInputBlock):
            return False
        if len(self.get_input_ports()) != len(other.get_input_ports()):
            return False
        my_input_ports = self.get_input_ports()
        your_input_ports = other.get_input_ports()
        for i in range(0, len(my_input_ports)):
            if not my_input_ports[i].equals(your_input_ports[i]):
                return False

        return True