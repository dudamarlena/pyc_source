# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extensions/middle/TensorIteratorMerge.py
# Compiled at: 2020-05-01 08:37:21
# Size of source mod 2**32: 17433 bytes
"""
 Copyright (C) 2018-2020 Intel Corporation

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
"""
from collections import deque
import numpy as np
from copy import deepcopy
from extensions.ops.tensor_iterator import TensorIterator
from mo.graph.graph import Node, Graph, add_opoutput
from mo.middle.replacement import MiddleReplacementPattern
from mo.ops.const import Const
from mo.ops.op import Op
from mo.ops.squeeze import Squeeze
from mo.ops.unsqueeze import Unsqueeze
from mo.utils.graph import sub_graph_between_nodes, invert_sub_graph_between_nodes
stop_nodes = [
 'TensorIteratorInput', 'TensorIteratorOutput', 'TensorIteratorBackEdge', 'TensorIteratorCondition']

def op_type(graph, node_name: str):
    node = Node(graph, node_name)
    if node.has_valid('kind'):
        if node['kind'] == 'op':
            return node['op']
    return


def update_inputs(graph, inputs: list, node_name: str):
    node = Node(graph, node_name)
    if node.has_valid('kind'):
        if node['kind'] == 'op':
            if node['op'] == 'TensorIteratorInput':
                if node_name not in inputs:
                    inputs.append(node_name)


def reverse_dfs(graph: Graph, node_name: str, stop_nodes: list, inputs: list, visited: set=None):
    d = deque()
    if visited is None:
        visited = set()
    visited.add(node_name)
    d.appendleft(node_name)
    while len(d) != 0:
        cur_node = d.popleft()
        for in_node_name, _ in graph.in_edges(cur_node):
            if in_node_name not in visited:
                if op_type(graph, in_node_name) not in stop_nodes:
                    visited.add(in_node_name)
                    d.append(in_node_name)
                else:
                    update_inputs(graph, inputs, in_node_name)


def dfs(graph: Graph, node_name: str, stop_nodes: list, visited: set=None):
    d = deque()
    visited.add(node_name)
    d.appendleft(node_name)
    while len(d) != 0:
        cur_node = d.popleft()
        for _, out_node_name in graph.out_edges(cur_node):
            if out_node_name not in visited and op_type(graph, out_node_name) not in stop_nodes:
                visited.add(out_node_name)
                d.append(out_node_name)


def get_body(graph, inputs, outputs):
    if len(inputs) == 0:
        nodes, extra_inputs = invert_sub_graph_between_nodes(graph, outputs, inputs, lambda node: node.soft_get('op') == 'TensorIteratorInput')
    else:
        nodes, extra_inputs = sub_graph_between_nodes(graph, inputs, outputs, lambda node: node.soft_get('op') == 'TensorIteratorInput')
    nodes = list(set(nodes) - set(inputs) - set(outputs) - set(extra_inputs))
    return (nodes, extra_inputs)


class TensorIteratorMerge(MiddleReplacementPattern):
    enabled = True
    graph_condition = [lambda graph: graph.graph['is_cyclic']]

    def run_after(self):
        return []

    def run_before(self):
        return []

    @staticmethod
    def pattern():
        return dict(nodes=[
         (
          'condition', dict(kind='op', op='TensorIteratorCondition'))],
          edges=[])

    @staticmethod
    def replace_pattern(graph, match: dict):
        cond_data = match['condition'].out_node(0)
        time_data = match['condition'].out_node(1) if len(match['condition'].out_nodes()) > 1 else None
        name = match['condition'].name
        back_edges = []
        inputs = []
        outputs = []
        for node in cond_data.out_nodes():
            if node['kind'] == 'op':
                if node['op'] == 'TensorIteratorBackEdge':
                    back_edges.append(node.id)
            if node['kind'] == 'op':
                if node['op'] == 'TensorIteratorInput':
                    inputs.append(node.id)
            if node['kind'] == 'op' and node['op'] == 'TensorIteratorOutput':
                outputs.append(node.id)

        if time_data is not None:
            for node in time_data.out_nodes():
                if node['kind'] == 'op':
                    if node['op'] == 'TensorIteratorInput':
                        inputs.append(node.id)
                if node['kind'] == 'op':
                    if node['op'] == 'TensorIteratorOutput':
                        outputs.append(node.id)
                assert False

        condition = match['condition']
        tensor_sequence_length = condition.in_node(0)
        graph.remove_nodes_from([condition.id, cond_data.id, tensor_sequence_length.id])
        if time_data is not None:
            graph.remove_nodes_from([time_data.id])
        body_nodes, extra_inputs = get_body(graph, inputs, outputs)
        body_nodes = list(set(body_nodes) - set([cond_data]))
        inputs += extra_inputs
        assert all([node in graph.nodes() for node in body_nodes])
        inputs = [Node(graph, node) for node in inputs]
        outputs = [Node(graph, node) for node in outputs]
        back_edges = [Node(graph, node) for node in back_edges]
        external_inputs = [{'external_data_id':node.in_node(1 if node.has_valid('axis') else 0),  'internal_data_id':node.out_node(0),  'axis':node.axis,  'start':node.start,  'end':node.end,  'stride':node.stride,  'part_size':node.part_size} for node in inputs]
        external_outputs = [{'external_data_id':node.out_node(0),  'internal_data_id':node.in_node(1 if node.has_valid('axis') else 0),  'axis':node.axis,  'start':node.start,  'end':node.end,  'stride':node.stride,  'part_size':node.part_size} for node in outputs]
        back_edges_data = [{'from_data_id':node.in_node(1),  'to_data_id':node.out_node(0),  'init_data_id':node.in_node(0)} for node in back_edges]
        body = Graph(name='body')
        body.graph = graph.graph
        body.add_nodes_from([(node, graph.node[node]) for node in body_nodes])
        body.add_edges_from([(u, v, k, d) for u, v, k, d in graph.edges(data=True, keys=True) if u in body_nodes if v in body_nodes])
        graph.remove_nodes_from(body_nodes + [match['condition'].id] + [inp.id for inp in inputs] + [out.id for out in outputs])
        internal_id_count = 0
        real_back_edges = []
        for edge in back_edges_data:
            if not edge['from_data_id'].id in body.nodes():
                raise AssertionError
            else:
                assert edge['to_data_id'].id in body.nodes()
                assert edge['init_data_id'].id in body.nodes()
                edge['from_data_id'] = Node(body, edge['from_data_id'].id)
                edge['to_data_id'] = Node(body, edge['to_data_id'].id)
                edge['init_data_id'] = Node(body, edge['init_data_id'].id)
                add_opoutput(body, edge['from_data_id'].id, 0, False)
                assert len(edge['from_data_id'].in_nodes()) == 1
                edge['from_data_id'].in_node()['internal_layer_id'] = edge['from_data_id'].in_node().has_valid('internal_layer_id') or internal_id_count
                internal_id_count += 1
            edge['from_layer'] = edge['from_data_id'].in_node()['internal_layer_id']
            if 'internal_port_id' not in edge['from_data_id'].in_edge():
                edge['from_data_id'].in_edge()['internal_port_id'] = internal_id_count
                internal_id_count += 1
            edge['from_port'] = edge['from_data_id'].in_edge()['internal_port_id']
            current_real_back_edges = []
            for _, consumer, key, edge_attrs in body.out_edges((edge['to_data_id'].id), data=True, keys=True):
                real_edge = {}
                real_edge.update(edge)
                consumer = Node(body, consumer)
                if real_edge['to_data_id'].in_node().has_valid('internal_layer_id'):
                    assert False
                    real_edge['to_data_id'].out_node()['internal_layer_id'] = real_edge['to_data_id'].in_node().internal_layer_id
                else:
                    if not consumer.has_valid('internal_layer_id'):
                        consumer['internal_layer_id'] = internal_id_count
                        internal_id_count += 1
                    real_edge['to_layer'] = consumer['internal_layer_id']
                    assert 'internal_port_id' not in edge_attrs
                    assert len(real_edge['init_data_id'].out_edges()) == 1
                    assert 'internal_port_id' not in real_edge['init_data_id'].out_edge()
                    edge_attrs['internal_port_id'] = internal_id_count
                    internal_id_count += 1
                    real_edge['to_port'] = edge_attrs['internal_port_id']
                    real_edge['consumer'] = consumer
                    real_edge['consumer_key'] = key
                    real_edge['attrs'] = deepcopy(edge_attrs)
                    current_real_back_edges.append(real_edge)

            body.add_edges_from([(real_edge['init_data_id'].id, real_edge['consumer'].id, real_edge['consumer_key'], real_edge['attrs']) for real_edge in current_real_back_edges])
            body.remove_nodes_from([edge['to_data_id'].id, edge['to_data_id'].in_node().id])
            real_back_edges += current_real_back_edges

        real_external_inputs = []
        for ext_inp in external_inputs:
            assert ext_inp['external_data_id'].id not in body.nodes()
            assert ext_inp['internal_data_id'].id in body.nodes()
            ext_inp['internal_data_id'] = Node(body, ext_inp['internal_data_id'].id)
            if ext_inp['axis'] is not None:
                shape = ext_inp['internal_data_id'].shape.copy()
                assert not ext_inp['internal_data_id'].has_valid('value')
                new_input_data = Op._create_data_node(body, ext_inp['internal_data_id'].name + '/UnsqueezedInput', dict(shape=(np.insert(shape, ext_inp['axis'], 1))))
                dim = shape.copy()
                dim[0] = -1
                reshape_op = Squeeze(body, dict(name=(ext_inp['internal_data_id'].name + '/InputSqueeze')))
                reshape_dim_data = Const(body, {'name':ext_inp['internal_data_id'].name + '/ReshapeDim',  'value':ext_inp['axis']}).create_node_with_data()
                reshape_op.create_node_with_data([new_input_data, reshape_dim_data], data_nodes=[
                 ext_inp['internal_data_id']])
                ext_inp['internal_data_id'] = new_input_data
            ext_inp['internal_data_id']['is_input'] = True
            assert len(ext_inp['internal_data_id'].in_nodes()) == 0
            ext_inp['external_port_id'] = internal_id_count
            internal_id_count += 1
            for _, consumer, edge_attrs in body.out_edges((ext_inp['internal_data_id'].id), data=True):
                real_ext_inp = {}
                real_ext_inp.update(ext_inp)
                consumer = Node(body, consumer)
                if not consumer.has_valid('internal_layer_id'):
                    consumer['internal_layer_id'] = internal_id_count
                    internal_id_count += 1
                if 'internal_port_id' not in edge_attrs:
                    edge_attrs['internal_port_id'] = internal_id_count
                    internal_id_count += 1
                real_ext_inp['internal_layer_id'] = consumer['internal_layer_id']
                real_ext_inp['internal_port_id'] = edge_attrs['internal_port_id']
                real_external_inputs.append(real_ext_inp)

        for ext_out in external_outputs:
            if not ext_out['external_data_id'].id not in body.nodes():
                raise AssertionError
            else:
                assert ext_out['internal_data_id'].id in body.nodes()
                ext_out['internal_data_id'] = Node(body, ext_out['internal_data_id'].id)
                if ext_out['axis'] is not None:
                    dim = ext_out['internal_data_id'].shape.copy()
                    dim[0] = -1
                    assert not ext_out['internal_data_id'].has_valid('value')
                    reshape_op = Unsqueeze(body, dict(name=(ext_out['internal_data_id'].name + '/OutputUnsqueeze')))
                    reshape_dim_data = Const(body, {'name':ext_out['internal_data_id'].name + '/ReshapeDim',  'value':ext_out['axis']}).create_node_with_data()
                    ext_out['internal_data_id'] = reshape_op.create_node_with_data([ext_out['internal_data_id'],
                     reshape_dim_data])
                any([out_node.soft_get('op', None) == 'Result' for out_node in ext_out['internal_data_id'].out_nodes()]) or add_opoutput(body, ext_out['internal_data_id'].id, 0, False)
            assert len(ext_out['internal_data_id'].in_nodes()) == 1
            if 'internal_layer_id' not in ext_out['internal_data_id'].in_node():
                ext_out['internal_data_id'].in_node()['internal_layer_id'] = internal_id_count
                internal_id_count += 1
            if 'internal_port_id' not in ext_out['internal_data_id'].in_edge():
                ext_out['internal_data_id'].in_edge()['internal_port_id'] = internal_id_count
                internal_id_count += 1
            ext_out['internal_layer_id'] = ext_out['internal_data_id'].in_node()['internal_layer_id']
            ext_out['internal_port_id'] = ext_out['internal_data_id'].in_edge()['internal_port_id']
            ext_out['external_port_id'] = internal_id_count
            internal_id_count += 1

        ti_op = TensorIterator(graph, {'name':name + '/TensorIterator', 
         'body':body, 
         'in_ports_count':len(external_inputs), 
         'out_ports_count':len(external_outputs), 
         'input_port_map':[{field:external_input[field] for field in ('external_port_id', 'internal_layer_id',
                                            'internal_port_id', 'axis', 'stride',
                                            'part_size', 'start', 'end')} for external_input in real_external_inputs], 
         'output_port_map':[{field:external_output[field] for field in ('external_port_id', 'internal_layer_id',
                                             'internal_port_id', 'axis', 'stride',
                                             'part_size', 'start', 'end')} for external_output in external_outputs], 
         'back_edges':[{field:edge[field] for field in ('from_layer', 'from_port', 'to_layer', 'to_port')} for edge in real_back_edges]})
        ti_outs = ti_op.create_node_with_data(inputs=[inp['external_data_id'] for inp in external_inputs],
          edge_attrs=[{'external_port_id': inp['external_port_id']} for inp in external_inputs],
          data_nodes=[out['external_data_id'] for out in external_outputs])
        if not isinstance(ti_outs, list):
            ti_outs = [
             ti_outs]
        for i, out in enumerate(ti_outs):
            out.in_edge()['external_port_id'] = external_outputs[i]['external_port_id']

        ti = ti_outs[0].in_node()
        TensorIterator.cover_body_input_data_nodes_with_parameter_ops(ti)
        TensorIterator.cover_body_constant_data_nodes_with_const_ops(ti)
        TensorIterator.normalize_internal_ids(ti)