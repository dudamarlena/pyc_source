# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mo/middle/passes/eliminate.py
# Compiled at: 2020-05-01 08:37:22
# Size of source mod 2**32: 10749 bytes
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
import re, logging as log
from collections import deque
import networkx as nx, numpy as np
from mo.utils.error import Error
from mo.utils.utils import deprecated_api

def get_nodes_with_attributes(graph, **attrs: dict):
    node_attrs = graph.nodes(data=True)
    return [n for n, d in node_attrs if all((a in d.items() for a in attrs.items()))]


def reverse_dfs(graph, node_name: str, update_func: callable, visited: set=None):
    d = deque()
    if visited is None:
        visited = set()
    visited.add(node_name)
    d.appendleft(node_name)
    while len(d) != 0:
        cur_node = d.popleft()
        update_func(graph, cur_node)
        for in_node_name, _ in graph.in_edges(cur_node):
            if in_node_name not in visited:
                visited.add(in_node_name)
                d.append(in_node_name)


def mark_input_nodes(graph, node_name: str, key: str, value):
    for input, _ in graph.in_edges(node_name):
        graph.node[input][key] = value


def mark_output_nodes(graph, node_name: str, key: str, value):
    for output, _ in graph.out_edges(node_name):
        graph.node[output][key] = value


def mark_output_reachable_nodes(graph):
    """
    Mark nodes whether they are outputs reachable or not. The node is considered output reachable if it is connected to
    one of the nodes that has attribute op=Result.
    """
    nx.set_node_attributes(G=graph, name='is_output_reachable', values=False)
    outputs = graph.get_nodes_with_attributes(op='Result')
    log.debug('The following nodes are seeded as output reachable:\n{}'.format('\n'.join(sorted(map(str, outputs)))))
    nx.set_node_attributes(G=graph, name='is_output_reachable', values={n:True for n in outputs})
    visited = set()
    for output_name in outputs:
        reverse_dfs(graph, output_name, lambda graph, node_name: mark_input_nodes(graph, node_name, 'is_output_reachable', True), visited)


def mark_undead_nodes(graph, undead_types: list):
    """
    Mark output nodes and nodes of the specific type as undead, meaning that they should survive the dead nodes
    elimination phase. Then mark all children nodes of the undead nodes (except children of inputs) as undead.
    :param graph: graph to operate on.
    :param undead_types: list of node types that should be marked as undead.
    :return: updated graph where each has attribute 'is_undead'.
    """
    from mo.utils.graph import bfs_search
    nx.set_node_attributes(G=graph, name='is_undead', values=False)
    outputs = graph.get_nodes_with_attributes(op='Result')
    nx.set_node_attributes(G=graph, name='is_undead', values={n:True for n in outputs})
    for type in undead_types:
        node_of_specific_type = graph.get_nodes_with_attributes(type=type)
        nx.set_node_attributes(G=graph, name='is_undead', values={n:True for n in node_of_specific_type})

    undead_nodes = graph.get_nodes_with_attributes(is_undead=True)
    for node_name in bfs_search(graph, undead_nodes):
        if graph.node[node_name]['is_undead']:
            for _, dst_node_name in graph.out_edges(node_name):
                node_attrs = graph.node[dst_node_name]
                if 'kind' in node_attrs:
                    if node_attrs['kind'] == 'data':
                        if node_attrs['value'] is not None or node_attrs['kind'] == 'op':
                            graph.node[dst_node_name]['is_undead'] = True

    inputs = graph.get_nodes_with_attributes(is_input=True)
    nx.set_node_attributes(G=graph, name='is_undead', values={n:True for n in inputs})


def mark_const_producer_nodes(graph):
    """
    Mark nodes that produce constant values.
    :param graph: graph to operate on.
    :return: .
    """
    nx.set_node_attributes(G=graph, name='is_const_producer', values=True)
    for node in graph.pseudo_topological_sort():
        for input, output, attrs in graph.in_edges((node.id), data=True):
            if 'control_flow_edge' in attrs and attrs['control_flow_edge']:
                graph.node[input]['is_const_producer'] = False
                graph.node[output]['is_const_producer'] = False

        if not node.has('value') or node.value is None:
            for input, _ in graph.in_edges(node.id):
                graph.node[input]['is_const_producer'] = False


def eliminate_dead_nodes--- This code section failed: ---

 L. 130         0  LOAD_GLOBAL              set
                2  CALL_FUNCTION_0       0  '0 positional arguments'
                4  STORE_FAST               'nodes_to_remove'

 L. 131         6  SETUP_LOOP           78  'to 78'
                8  LOAD_FAST                'graph'
               10  LOAD_ATTR                nodes
               12  LOAD_CONST               True
               14  LOAD_CONST               ('data',)
               16  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               18  GET_ITER         
             20_0  COME_FROM            62  '62'
             20_1  COME_FROM            42  '42'
               20  FOR_ITER             76  'to 76'
               22  UNPACK_SEQUENCE_2     2 
               24  STORE_FAST               'node_name'
               26  STORE_FAST               'node_attrs'

 L. 132        28  LOAD_FAST                'node_attrs'
               30  LOAD_STR                 'is_output_reachable'
               32  BINARY_SUBSCR    
               34  POP_JUMP_IF_FALSE    64  'to 64'

 L. 133        36  LOAD_FAST                'node_attrs'
               38  LOAD_STR                 'is_const_producer'
               40  BINARY_SUBSCR    
               42  POP_JUMP_IF_FALSE    20  'to 20'
               44  LOAD_FAST                'node_attrs'
               46  LOAD_STR                 'is_undead'
               48  BINARY_SUBSCR    
               50  POP_JUMP_IF_FALSE    64  'to 64'

 L. 134        52  LOAD_FAST                'node_attrs'
               54  LOAD_METHOD              get
               56  LOAD_STR                 'force_dead_node'
               58  LOAD_CONST               False
               60  CALL_METHOD_2         2  '2 positional arguments'
               62  POP_JUMP_IF_FALSE    20  'to 20'
             64_0  COME_FROM            50  '50'
             64_1  COME_FROM            34  '34'

 L. 135        64  LOAD_FAST                'nodes_to_remove'
               66  LOAD_METHOD              add
               68  LOAD_FAST                'node_name'
               70  CALL_METHOD_1         1  '1 positional argument'
               72  POP_TOP          
               74  JUMP_BACK            20  'to 20'
               76  POP_BLOCK        
             78_0  COME_FROM_LOOP        6  '6'

 L. 136        78  LOAD_GLOBAL              log
               80  LOAD_METHOD              debug
               82  LOAD_STR                 'Removing the following dead nodes: {}'
               84  LOAD_METHOD              format
               86  LOAD_STR                 '\n'
               88  LOAD_METHOD              join
               90  LOAD_GLOBAL              sorted
               92  LOAD_GLOBAL              map
               94  LOAD_GLOBAL              str
               96  LOAD_FAST                'nodes_to_remove'
               98  CALL_FUNCTION_2       2  '2 positional arguments'
              100  CALL_FUNCTION_1       1  '1 positional argument'
              102  CALL_METHOD_1         1  '1 positional argument'
              104  CALL_METHOD_1         1  '1 positional argument'
              106  CALL_METHOD_1         1  '1 positional argument'
              108  POP_TOP          

 L. 137       110  LOAD_FAST                'graph'
              112  LOAD_METHOD              remove_nodes_from
              114  LOAD_FAST                'nodes_to_remove'
              116  CALL_METHOD_1         1  '1 positional argument'
              118  POP_TOP          

Parse error at or near `POP_BLOCK' instruction at offset 76


def add_constant_operations(graph):
    data_nodes = graph.get_data_nodes(has_value=True)
    for node in data_nodes:
        if len(node.in_nodes()) == 0 and len(node.out_nodes()) != 0:
            from mo.ops.const import Const
            name = node.soft_get'name'node.id
            new_name = re.sub('\\/Output_\\d+\\/Data_(.?)+', '', name)
            const_node = Const(graph, dict(value=(node.value), name=new_name, force_shape=(node.soft_get'force_shape'None),
              override_output_shape=(node.has_valid('force_shape')),
              force_type=(node.soft_get'force_type'None),
              correct_data_type=(node.soft_get'correct_data_type'False))).create_node()
            graph.add_edges_from([(const_node.id, node.id, {'out': 0})])


def remove_const_ops(graph):
    for node in graph.get_op_nodes(type='Const'):
        graph.remove_edgenode.idnode.out_node().id
        graph.remove_node(node.id)


def shape_inference(graph):
    for node in graph.pseudo_topological_sort():
        if node.has_and_set('need_shape_inference'):
            old_out_shapes = [port.data.get_shape() for port in node.out_ports().values() if not port.disconnected()]
            node.infer(node)
            new_out_shapes = [port.data.get_shape() for port in node.out_ports().values() if not port.disconnected()]
            if not node.has_and_set('override_output_shape'):
                for shape1, shape2 in zip(old_out_shapes, new_out_shapes):
                    if shape1 is not None and not np.array_equalshape1shape2:
                        raise Error('After partial shape inference were found shape collision for node {} (old shape: {}, new shape: {})'.format(node.name, shape1, shape2))

            else:
                del node['override_output_shape']
            node.need_shape_inference = False


@deprecated_api('Graph', 'clean_up')
def graph_clean_up(graph, undead_node_types: list=None):
    graph.clean_up(undead_node_types)


@deprecated_api('Graph', 'clean_up')
def graph_clean_up_tf(graph):
    graph.clean_up()


@deprecated_api('Graph', 'clean_up')
def graph_clean_up_onnx(graph):
    graph.clean_up()


def merge_data_nodes(graph, survived, removed):
    if survived.has_and_set('op'):
        if survived.op == 'Result':
            graph.node[removed.id].update({'op': 'Result'})
    for u, v, d in list(graph.in_edges((removed.id), data=True)):
        graph.add_edges_from([(u, survived.id, d)])
        graph.remove_edgeuv

    for u, v, d in list(graph.out_edges((removed.id), data=True)):
        graph.add_edges_from([(survived.id, v, d)])
        graph.remove_edgeuv

    for attr in graph.node[removed.id]:
        if attr not in ('name', ):
            if attr == 'fw_tensor_debug_info':
                if not survived.has_valid(attr):
                    survived[attr] = []
                for fw_tensor_debug_info in removed[attr]:
                    survived[attr].append(fw_tensor_debug_info)

            else:
                survived[attr] = removed[attr]


def remove_op_node_with_data_node(graph, node_to_remove):
    from mo.graph.graph import Node
    assert node_to_remove.kind == 'op'
    input_data_node = node_to_remove.in_node()
    output_node = [v for _, v in graph.out_edges(node_to_remove.id)]
    assert len(output_node) == 1, 'Cannot remove node producing two or more output tensors'
    output_node = Node(graph, output_node[0])
    assert output_node.kind == 'data', 'The function must be used after partial infer'
    graph.remove_edgeinput_data_node.idnode_to_remove.id
    graph.remove_edgenode_to_remove.idoutput_node.id
    merge_data_nodes(graph, output_node, input_data_node)
    log.debug('Removing op node: {}'.format(node_to_remove.id))
    graph.remove_nodes_from([node_to_remove.id, input_data_node.id])


def remove_op_nodes(graph, attrs: dict):
    for node in (graph.get_op_nodes)(**attrs):
        remove_op_node_with_data_node(graph, node)


def remove_edges_for_nodes(graph, node_attrs: dict, edge_attrs: dict):
    from mo.graph.graph import Node
    for node in graph.nodes():
        node = Node(graph, node)
        if all([node.has(attr) and node[attr] == node_attrs[attr] for attr in node_attrs]):
            nodes_edges = node.in_nodes_edges()
            for port in nodes_edges:
                src_node, edge = nodes_edges[port]
                if all([attr in edge and edge[attr] == edge_attrs[attr] for attr in edge_attrs]):
                    graph.remove_edgesrc_node.idnode.id