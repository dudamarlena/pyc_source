# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/meta_model/ast_nestml_compilation_unit.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 4277 bytes
from pynestml.meta_model.ast_neuron import ASTNeuron
from pynestml.meta_model.ast_node import ASTNode

class ASTNestMLCompilationUnit(ASTNode):
    __doc__ = '\n    The ASTNestMLCompilationUnit class as used to store a collection of processed ASTNeurons.\n    Grammar:\n        nestMLCompilationUnit: (neuron | NEWLINE )* EOF;\n    Attributes:\n        neuron_list = None # a list of all processed neurons\n        artifact_name = None\n    '

    def __init__(self, source_position=None, artifact_name=None):
        """
        Standard constructor of ASTNestMLCompilationUnit.
        :param source_position: the position of this element in the source file.
        :type source_position: ASTSourceLocation.
        :param artifact_name: the name of the file where ths model is contained in
        :type artifact_name: str
        """
        assert artifact_name is not None and isinstance(artifact_name, str), '(PyNestML.AST.NestMLCompilationUnit) No or wrong type of artifact name provided (%s)!' % type(artifact_name)
        super(ASTNestMLCompilationUnit, self).__init__(source_position)
        self.neuron_list = list()
        self.artifact_name = artifact_name

    def add_neuron(self, neuron):
        """
        Expects an instance of neuron element which is added to the collection.
        :param neuron: an instance of a neuron 
        :type neuron: ASTNeuron
        :return: no returned value
        :rtype: void
        """
        assert neuron is not None and isinstance(neuron, ASTNeuron), '(PyNestML.AST.CompilationUnit) No or wrong type of neuron provided (%s)!' % type(neuron)
        self.neuron_list.append(neuron)

    def delete_neuron(self, neuron):
        """
        Expects an instance of neuron element which is deleted from the collection.
        :param neuron: an instance of a ASTNeuron
        :type neuron:ASTNeuron
        :return: True if element deleted from list, False else.
        :rtype: bool
        """
        if self.neuron_list.__contains__(neuron):
            self.neuron_list.remove(neuron)
            return True
        else:
            return False

    def get_neuron_list(self):
        """
        :return: a list of neuron elements as stored in the unit
        :rtype: list(ASTNeuron)
        """
        return self.neuron_list

    def get_parent(self, ast):
        """
        Indicates whether a this node contains the handed over node.
        :param ast: an arbitrary meta_model node.
        :type ast: AST_
        :return: AST if this or one of the child nodes contains the handed over element.
        :rtype: AST_ or None
        """
        for neuron in self.get_neuron_list():
            if neuron is ast:
                return self
            if neuron.get_parent(ast) is not None:
                return neuron.get_parent(ast)

    def equals(self, other):
        """
        The equals method.
        :param other: a different object
        :type other: object
        :return: True if equal, otherwise False.
        :rtype: bool
        """
        if not isinstance(other, ASTNestMLCompilationUnit):
            return False
        if len(self.get_neuron_list()) != len(other.get_neuron_list()):
            return False
        my_neurons = self.get_neuron_list()
        your_neurons = other.get_neuron_list()
        for i in range(0, len(my_neurons)):
            if not my_neurons[i].equals(your_neurons[i]):
                return False

        return True