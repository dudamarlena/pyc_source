# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mo/front/tf/custom_subgraph_call.py
# Compiled at: 2020-05-01 08:37:22
# Size of source mod 2**32: 8760 bytes
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
import logging as log
from re import findall
from mo.front.extractor import update_ie_fields
from mo.graph.graph import Node, merge_edge_props, Graph
from mo.utils.graph import is_connected_component

def internal_output_name_for_node(node_name: str, output_port: int):
    return node_name + ':' + str(output_port)


def add_node_pb_if_not_yet_added(node: Node, mega_node: Node):
    if node.has_valid('pb'):
        if node.pb.name not in mega_node.pbs.keys():
            mega_node.pbs[node.pb.name] = node.pb


def find_input_port(node: Node, input_desc: list, search_node_name: str, search_node_port: int):
    if input_desc is None:
        return len(node.in_nodes())
    for in_port, tensor_desc in enumerate(input_desc):
        for node_pattern, node_port in tensor_desc:
            if findall(node_pattern, search_node_name) and node_port == search_node_port:
                return in_port

    raise Exception('Did not find input port of the node "{}" with port "{}"'.format(search_node_name, search_node_port))


def find_output_port(node: Node, output_desc: list, search_node_name: str, search_node_port: int):
    if output_desc is None:
        return len(node.out_nodes())
    for out_port, (node_pattern, node_port) in enumerate(output_desc):
        if findall(node_pattern, search_node_name) and node_port == search_node_port:
            return out_port

    raise Exception('Did not find output port of the node "{}" with port "{}"'.format(search_node_name, search_node_port))


def merge_nodes(graph: Graph, nodes_to_merge_names: list, inputs_desc: list=None, outputs_desc: list=None):
    """
    Merges nodes specified in the set 'nodes_to_merge_names' into one mega-node, creating new edges between mega-node
    and inputs/outputs nodes of the mega-node. The added edges contain name of input/output nodes which will be used for
    generation of placeholders and will be saved to the IR xml so IE plug-in know how to map input/output data for the
    layer. Also the function adds protobufs of the nodes of the sub-graph and 'Const' ops consumed by nodes in the
    sub-graph to the node's attribute 'pbs'.
    :param graph: the graph object to operate on.
    :param nodes_to_merge_names: list of nodes names that should be merged into a single node.
    :param inputs_desc: optional list describing input nodes order.
    :param outputs_desc: optional list describing output nodes order.
    """
    if not is_connected_component(graph, nodes_to_merge_names):
        log.warning('The following nodes do not form connected sub-graph: {}'.format(nodes_to_merge_names))
    new_node_name = graph.unique_id('TFSubgraphCall_')
    log.info("Create new node with name '{}' for nodes '{}'".format(new_node_name, ', '.join(nodes_to_merge_names)))
    graph.add_node(new_node_name)
    new_node_attrs = graph.node[new_node_name]
    new_node_attrs['name'] = new_node_name
    set_tf_custom_call_node_attrs(new_node_attrs)
    new_node = Node(graph, new_node_name)
    added_input_tensors_names = set()
    added_new_node_output_tensors = dict()
    for node_name in nodes_to_merge_names:
        node = Node(graph, node_name)
        add_node_pb_if_not_yet_added(node, new_node)
        for in_node_name, edge_attrs in Node(graph, node_name).get_inputs():
            in_node = Node(graph, in_node_name)
            if in_node_name in nodes_to_merge_names:
                add_node_pb_if_not_yet_added(in_node, new_node)
                continue
            if in_node_name not in nodes_to_merge_names:
                input_tensor_name = node.pb.input[edge_attrs['in']]
            if input_tensor_name not in added_input_tensors_names:
                if not new_node.has_port('in', edge_attrs['in']):
                    new_node.add_input_port(edge_attrs['in'])
                (graph.add_edge)(in_node_name, new_node_name, **merge_edge_props({'in':find_input_port(new_node, inputs_desc, node_name, edge_attrs['in']), 
                  'out':edge_attrs['out'], 
                  'internal_input_node_name':input_tensor_name, 
                  'original_dst_node_name':node_name, 
                  'original_dst_port':edge_attrs['in'], 
                  'in_attrs':[
                   'in', 'internal_input_node_name', 'original_dst_node_name',
                   'original_dst_port', 'placeholder_name'], 
                  'out_attrs':[
                   'out']}, edge_attrs))
                log.debug('Creating edge from outside of sub-graph to inside sub-graph: {} -> {}'.format(in_node_name, new_node_name))
                added_input_tensors_names.add(input_tensor_name)

        for out_node_name, edge_attrs in Node(graph, node_name).get_outputs():
            if out_node_name not in nodes_to_merge_names:
                log.debug('Creating edge from inside of sub-graph to outside sub-graph: {} -> {}'.format(new_node_name, out_node_name))
                out_name = internal_output_name_for_node(node_name, edge_attrs['out'])
                if out_name not in added_new_node_output_tensors.keys():
                    added_new_node_output_tensors[out_name] = find_output_port(new_node, outputs_desc, node_name, edge_attrs['out'])
                if not new_node.has_port('out', added_new_node_output_tensors[out_name]):
                    new_node.add_output_port(added_new_node_output_tensors[out_name])
                (graph.add_edge)(new_node_name, out_node_name, **merge_edge_props({'in':edge_attrs['in'], 
                  'out':added_new_node_output_tensors[out_name], 
                  'internal_output_node_name':out_name, 
                  'in_attrs':[
                   'in', 'internal_input_node_name'], 
                  'out_attrs':[
                   'out', 'internal_output_node_name']}, edge_attrs))

        new_node['output_tensors_names'] = [val for val in {v:k for k, v in added_new_node_output_tensors.items()}.values()]

    new_node['nodes_order'] = [node for node in graph.graph['initial_nodes_order'] if node in new_node['pbs'].keys()]
    for n in nodes_to_merge_names:
        if graph.has_node(n):
            graph.remove_node(n)

    return Node(graph, new_node_name)


def set_tf_custom_call_node_attrs(node_attrs: dict):
    from mo.front.tf.partial_infer.tf import tf_subgraph_infer
    update_ie_fields(node_attrs)
    node_attrs['input_nodes_names'] = list()
    node_attrs['output_tensors_names'] = list()
    node_attrs['real_input_dims'] = list()
    node_attrs['pbs'] = dict()
    node_attrs['type'] = 'TFCustomSubgraphCall'
    node_attrs['op'] = 'TFCustomSubgraphCall'
    node_attrs['infer'] = tf_subgraph_infer
    node_attrs['kind'] = 'op'