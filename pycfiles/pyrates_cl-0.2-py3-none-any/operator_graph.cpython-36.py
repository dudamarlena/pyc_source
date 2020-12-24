# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: E:\01_Work\15_PhD\11_Python_neural_mass_models\PyRates\pyrates\ir\operator_graph.py
# Compiled at: 2020-02-14 03:08:20
# Size of source mod 2**32: 12362 bytes
__doc__ = '\n'
from copy import deepcopy, copy
from typing import Iterator, Dict, List
import numpy as _np
from networkx import DiGraph, find_cycle, NetworkXNoCycle
from pyrates import PyRatesException
from pyrates.ir.operator import OperatorIR
__author__ = 'Daniel Rose'
__status__ = 'Development'
op_graph_cache = {}

def _cache_op_graph(cls):
    """Cache unique instances of operator graphs and return the instance. If hash of Operator graph is not known yet,
    a new instance will be created. Otherwise, an instance from cash will be returned."""

    def cache_func(operators=None, template=''):
        if operators is None:
            operators = {}
        h = hash(tuple(operators.values()))
        changed_labels = False
        try:
            op_graph = op_graph_cache[h]
        except KeyError:
            op_graph = cls(operators, template)
            assert h == hash(op_graph)
            op_graph_cache[h] = op_graph
        else:
            changed_labels = {}
            for name, op in operators.items():
                op_hash = hash(op)
                for cached_name, cached_op in op_graph:
                    if op_hash == hash(cached_op['operator']):
                        changed_labels[name] = cached_name
                        break

        return (
         op_graph, changed_labels)

    return cache_func


@_cache_op_graph
class OperatorGraph(DiGraph):
    """OperatorGraph"""

    def __init__(self, operators=None, template=''):
        super().__init__()
        if operators is None:
            operators = {}
        self._h = hash(tuple(operators.values()))
        all_outputs = {}
        for key, operator in operators.items():
            inputs = {var:dict(sources=(set()), reduce_dim=True) for var in operator.inputs}
            self.add_node(key, operator=operator, inputs=inputs, label=key)
            out_var = operator.output
            if out_var not in all_outputs:
                all_outputs[out_var] = []
            all_outputs[out_var].append(key)

        for label, data in self.nodes(data=True):
            op = data['operator']
            for in_var in op.inputs:
                if in_var in all_outputs:
                    for predecessor in all_outputs[in_var]:
                        data['inputs'][in_var]['sources'].add(predecessor)
                        self.add_edge(predecessor, label)

                    continue

        try:
            find_cycle(self)
        except NetworkXNoCycle:
            pass
        else:
            raise PyRatesException('Found cyclic operator graph. Cycles are not allowed for operators within one node or edge.')

    def __hash__(self):
        return self._h

    def getitem_from_iterator(self, key: str, key_iter: Iterator[str]):
        """
        Helper function for Python magic __getitem__. Accepts an iterator that yields string keys. If `key_iter`
        contains one key, an operator will be (looked for and) returned. If it instead contains two keys, properties of
        a variable that belong to an operator is returned.

        Parameters
        ----------
        key
        key_iter

        Returns
        -------
        item
            operator or variable properties
        """
        try:
            var = next(key_iter)
        except StopIteration:
            item = self.nodes[key]['operator']
        else:
            item = self.nodes[key]['operator'].variables[var]
        return item

    def __iter__(self):
        """Return an iterator containing all operator labels in the operator graph."""
        return iter(self.nodes(data=True))

    def operators(self, get_ops=False, get_vals=False):
        """Alias for self.nodes"""
        if get_ops:
            if get_vals:
                return ((data['label'], op, data['values']) for op, data in self.nodes(data=True))
        if get_ops:
            return ((data['label'], op) for op, data in self.nodes(data=True))
        else:
            if get_vals:
                return ((data['label'], data['values']) for op, data in self.nodes(data=True))
            return self.nodes


class VectorizedOperatorGraph(DiGraph):
    """VectorizedOperatorGraph"""

    def __init__(self, op_graph=None, values=None):
        super().__init__()
        if op_graph is None:
            pass
        else:
            for op_key, data in op_graph:
                try:
                    op = data['operator']
                except KeyError:
                    (self.add_operator)(op_key, **deepcopy(data))
                else:
                    self.add_operator(op_key, inputs=(deepcopy(data['inputs'])),
                      equations=(list(op.equations)),
                      variables=(deepcopy(op.variables.to_dict())),
                      output=(op.output))
                op_values = deepcopy(values[op_key])
                op_vars = self.operators[op_key]['variables']
                for var_key, value in op_values.items():
                    op_vars[var_key]['value'] = [
                     value]

            self.add_edges_from(op_graph.edges)

    def add_operator(self, *args, **kwargs):
        """Alias for `self.add_node`"""
        (self.add_node)(*args, **kwargs)

    def getitem_from_iterator(self, key: str, key_iter: Iterator[str]):
        """
        Helper function for Python magic __getitem__. Accepts an iterator that yields string keys. If `key_iter`
        contains one key, an operator will be (looked for and) returned. If it instead contains two keys, properties of
        a variable that belong to an operator is returned.

        Parameters
        ----------
        key
        key_iter

        Returns
        -------
        item
            operator or variable properties
        """
        try:
            var = next(key_iter)
        except StopIteration:
            item = self.nodes[key]
        else:
            item = self.nodes[key]['variables'][var]
        return item

    @property
    def operators(self):
        """Alias for self.nodes"""
        return self.nodes

    def append_values(self, value_dict: dict):
        """Append value along vector dimension of operators.

        Parameters
        ----------
        value_dict

        Returns
        -------

        """
        for op_key, variables_updates in value_dict.items():
            original_variables = self.nodes[op_key]['variables']
            for var_key, value in variables_updates.items():
                var = original_variables[var_key]
                shape = _np.shape(value)
                shape_sum = _np.sum(shape)
                if shape_sum > 1:
                    if _np.all(shape == _np.shape(var['value'])[1:]):
                        raise ValueError(f"Inconsistent dimensions of variable {var}. Dimension of value to add: {shape} Internal dimension of vectorized value array: {_np.shape(var['value'])[1:]}")
                    var['value'].append(value)
                else:
                    if shape_sum == 0:
                        var['value'].append(value)
                    else:
                        var['value'].extend(value)
                var['shape'] = _np.shape(var['value'])