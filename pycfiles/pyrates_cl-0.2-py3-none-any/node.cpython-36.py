# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: E:\01_Work\15_PhD\11_Python_neural_mass_models\PyRates\pyrates\ir\node.py
# Compiled at: 2020-02-14 03:08:20
# Size of source mod 2**32: 5662 bytes
__doc__ = '\n'
from copy import copy, deepcopy
from typing import Iterator
import numpy as np
from pyrates.ir.abc import AbstractBaseIR
from pyrates.ir.operator_graph import OperatorGraph, VectorizedOperatorGraph
__author__ = 'Daniel Rose'
__status__ = 'Development'

class NodeIR(AbstractBaseIR):
    __slots__ = [
     '_op_graph', 'values']

    def __init__(self, operators=None, values=None, template=None):
        super().__init__(template)
        self._op_graph, changed_labels = OperatorGraph(operators)
        try:
            for old_name, new_name in changed_labels.items():
                values[new_name] = values.pop(old_name)

        except AttributeError:
            pass

        self.values = values

    @property
    def op_graph(self):
        return self._op_graph

    def getitem_from_iterator(self, key: str, key_iter: Iterator[str]):
        """Alias for self.op_graph.getitem_from_iterator"""
        return self.op_graph.getitem_from_iterator(key, key_iter)

    def __iter__(self):
        """Return an iterator containing all operator labels in the operator graph."""
        return iter(self.op_graph)

    @property
    def operators(self):
        return self.op_graph.operators

    def __hash__(self):
        raise NotImplementedError


class VectorizedNodeIR(AbstractBaseIR):
    """VectorizedNodeIR"""
    __slots__ = [
     'op_graph', '_length']

    def __init__(self, node_ir):
        super().__init__(node_ir.template)
        self.op_graph = VectorizedOperatorGraph(node_ir.op_graph, node_ir.values)
        values = {}
        self._length = 1

    def getitem_from_iterator(self, key: str, key_iter: Iterator[str]):
        """Alias for self.op_graph.getitem_from_iterator"""
        return self.op_graph.getitem_from_iterator(key, key_iter)

    def __iter__(self):
        """Return an iterator containing all operator labels in the operator graph."""
        return iter(self.op_graph)

    @property
    def operators(self):
        return self.op_graph.operators

    def __hash__(self):
        raise NotImplementedError

    def extend(self, node: NodeIR):
        """ Extend variables vectors by values from one additional node.

        Parameters
        ----------
        node
            A node whose values are used to extend the vector dimension of this vectorized node.

        Returns
        -------
        """
        self.op_graph.append_values(node.values)
        self._length += 1

    def __len__(self):
        """Returns size of this vector node as recorded in self._length.

        Returns
        -------
        self._length
        """
        return self._length

    def add_op(self, op_key: str, inputs: dict, output: str, equations: list, variables: dict):
        """Wrapper for internal `op_graph.add_operator` that adds any values to node-level values dictionary for quick
        access

        Parameters
        ----------
        op_key
            Name of operator to be added
        inputs
            dictionary definining input variables of the operator
        output
            string defining name of single output variable
        equations
            list of equations (strings)
        variables
            dictionary describing variables

        Returns
        -------

        """
        self.op_graph.add_operator(op_key, inputs=inputs, output=output, equations=equations, variables=variables)

    def add_op_edge(self, source_op_key: str, target_op_key: str, **attr):
        """ Alias to `self.op_graph.add_edge`

        Parameters
        ----------
        source_op_key
        target_op_key
        attr

        Returns
        -------

        """
        (self.op_graph.add_edge)(source_op_key, target_op_key, **attr)