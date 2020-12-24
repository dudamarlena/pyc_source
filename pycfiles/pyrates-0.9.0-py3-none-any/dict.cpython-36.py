# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: e:\01_work\15_phd\11_python_neural_mass_models\pyrates\pyrates\frontend\dict.py
# Compiled at: 2019-07-12 14:06:06
# Size of source mod 2**32: 3268 bytes
"""
"""
from copy import deepcopy
from pyrates.ir.circuit import CircuitIR
from pyrates.ir.node import NodeIR
from pyrates.ir.edge import EdgeIR
from pyrates.ir.operator import OperatorIR
from pyrates.frontend._registry import register_interface
__author__ = 'Daniel Rose'
__status__ = 'Development'

@register_interface
def to_node(node_dict: dict):
    operators = {}
    operator_args = node_dict['operator_args']
    for key, item in node_dict['operators'].items():
        operators[key] = {'operator':to_operator(item),  'variables':{}}

    for key, item in operator_args.items():
        op_name, var_name = key.split('/')
        operators[op_name]['variables'][var_name] = item

    return NodeIR(operators=operators)


@register_interface
def to_operator(op_dict: dict):
    return OperatorIR(equations=(op_dict['equations']), inputs=(op_dict['inputs']), output=(op_dict['output']))


@register_interface
def from_circuit(circuit: CircuitIR):
    """Reformat graph structure into a dictionary that can be saved as YAML template. The current implementation assumes
    that nodes and edges are given by as templates."""
    node_dict = {}
    for node_key, node_data in circuit.nodes(data=True):
        node = node_data['node']
        if node.template:
            node_dict[node_key] = node.template
            continue

    edge_list = []
    for source, target, edge_data in circuit.edges(data=True):
        edge_data = deepcopy(edge_data)
        edge = edge_data.pop('edge_ir')
        source = f"{source}/{edge_data['source_var']}"
        target = f"{target}/{edge_data['target_var']}"
        edge_list.append((source, target, edge.template,
         dict(weight=(edge_data['weight']), delay=(edge_data['delay']))))

    base = 'CircuitTemplate'
    return dict(nodes=node_dict, edges=edge_list, base=base)