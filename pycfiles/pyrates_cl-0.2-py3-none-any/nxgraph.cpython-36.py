# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: e:\01_work\15_phd\11_python_neural_mass_models\pyrates\pyrates\frontend\nxgraph.py
# Compiled at: 2019-07-12 14:06:06
# Size of source mod 2**32: 11894 bytes
__doc__ = '\n'
from copy import deepcopy
import networkx as nx
from networkx import MultiDiGraph, DiGraph, find_cycle, NetworkXNoCycle
from pyrates import PyRatesException
from pyrates.ir.edge import EdgeIR
from pyrates.ir.circuit import CircuitIR
from pyrates.frontend.dict import to_node
from pyrates.frontend._registry import register_interface
__author__ = 'Daniel Rose'
__status__ = 'Development'

@register_interface
def to_circuit(graph: nx.MultiDiGraph, label='circuit', node_creator=to_node):
    """Create a CircuitIR instance out of a networkx.MultiDiGraph"""
    circuit = CircuitIR(label)
    for name, data in graph.nodes(data=True):
        circuit.add_node(name, node=(node_creator(data)))

    required_keys = ['source_var', 'target_var', 'weight', 'delay']
    for source, target, data in graph.edges(data=True):
        if all([key in data for key in required_keys]):
            if 'edge_ir' not in data:
                data['edge_ir'] = EdgeIR()
            source_var = data.pop('source_var')
            target_var = data.pop('target_var')
            (circuit.add_edge)(f"{source}/{source_var}", f"{target}/{target_var}", **data)
        else:
            raise KeyError(f"Missing a key out of {required_keys} in an edge with source `{source}` and target`{target}`")

    return circuit


def from_circuit(circuit, revert_node_names=False):
    """Old implementation that transforms all information in a circuit to a networkx.MultiDiGraph with a few additional
    transformations that the old backend needed."""
    return Circuit2NetDef.network_def(circuit, revert_node_names)


class Circuit2NetDef:

    @classmethod
    def network_def(cls, circuit: CircuitIR, revert_node_names=False):
        """A bit of a workaround to connect interfaces of frontend and backend.
        TODO: Remove BackendIRFormatter and adapt corresponding tests"""
        network_def = MultiDiGraph()
        edge_list = []
        node_dict = {}
        for node_key, data in circuit.graph.nodes(data=True):
            node = data['node']
            if revert_node_names:
                names = node_key.split('/')
                node_key = '.'.join(reversed(names))
            node_dict[node_key] = {}
            node_dict[node_key] = dict(cls._nd_reformat_operators(node.op_graph))
            op_order = cls._nd_get_operator_order(node.op_graph)
            node_dict[node_key]['operator_order'] = op_order

        for source, target, data in circuit.graph.edges(data=True):
            if revert_node_names:
                source = '.'.join(reversed(source.split('/')))
                target = '.'.join(reversed(target.split('/')))
            node_dict[target], edge = cls._move_edge_ops_to_node(target, node_dict[target], data)
            edge_list.append((source, target, dict(**edge)))

        for key, node in node_dict.items():
            (network_def.add_node)(key, **node)

        network_def.add_edges_from(edge_list)
        return network_def

    @staticmethod
    def _nd_reformat_operators(op_graph: DiGraph):
        operator_args = dict()
        operators = dict()
        for op_key, op_dict in op_graph.nodes(data=True):
            op_cp = deepcopy(op_dict)
            var_dict = op_cp.pop('variables')
            for var_key, var_props in var_dict.items():
                var_prop_cp = deepcopy(var_props)
                var_prop_cp['shape'] = ()
                var_prop_cp.pop('unit', None)
                var_prop_cp.pop('description', None)
                var_prop_cp.pop('name', None)
                operator_args[f"{op_key}/{var_key}"] = deepcopy(var_prop_cp)

            op_cp['equations'] = op_cp['operator'].equations
            op_cp['inputs'] = op_cp['operator'].inputs
            op_cp['output'] = op_cp['operator'].output
            op_cp.pop('operator', None)
            operators[op_key] = op_cp

        reformatted = dict(operator_args=operator_args, operators=operators,
          inputs={})
        return reformatted

    @staticmethod
    def _nd_get_operator_order(op_graph: DiGraph) -> list:
        """

        Parameters
        ----------
        op_graph

        Returns
        -------
        op_order
        """
        try:
            find_cycle(op_graph)
        except NetworkXNoCycle:
            pass
        else:
            raise PyRatesException('Found cyclic operator graph. Cycles are not allowed for operators within one node.')
        op_order = []
        graph = op_graph.copy()
        while graph.nodes:
            primary_nodes = [node for node, in_degree in graph.in_degree if in_degree == 0]
            op_order.extend(primary_nodes)
            graph.remove_nodes_from(primary_nodes)

        return op_order

    @classmethod
    def _move_edge_ops_to_node(cls, target, node_dict: dict, edge_dict: dict) -> (dict, dict):
        """

        Parameters
        ----------
        target
            Key identifying target node in backend graph
        node_dict
            Dictionary of target node (to move operators into)
        edge_dict
            Dictionary with edge properties (to move operators from)
        Returns
        -------
        node_dict
            Updated dictionary of target node
        edge_dict
             Dictionary of reformatted edge
        """
        edge = edge_dict['edge_ir']
        source_var = edge_dict['source_var']
        target_var = edge_dict['target_var']
        weight = edge_dict['weight']
        delay = edge_dict['delay']
        input_var = edge.input
        output_var = edge.output
        if len(edge.op_graph) > 0:
            op_data = cls._nd_reformat_operators(edge.op_graph)
            op_order = cls._nd_get_operator_order(edge.op_graph)
            operators = op_data['operators']
            operator_args = op_data['operator_args']
            added_ops = False
            for op_name in reversed(op_order):
                if op_name in node_dict['operators']:
                    pass
                else:
                    added_ops = True
                    node_dict['operators'][op_name] = operators[op_name]
                    node_dict['operator_order'].insert(0, op_name)
                    node_dict['operator_args'].update(operator_args)

            out_op = op_order[(-1)]
            out_var = operators[out_op]['output']
            if added_ops:
                target_op, target_vname = target_var.split('/')
                if output_var not in node_dict['operators'][target_op]['inputs'][target_vname]['sources']:
                    node_dict['operators'][target_op]['inputs'][target_vname]['sources'].append(out_op)
            target_var = input_var
        edge_dict = {'source_var':source_var, 
         'target_var':target_var, 
         'weight':weight, 
         'delay':delay}
        return (
         node_dict, edge_dict)