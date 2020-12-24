# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extensions/middle/ApplyPermutations.py
# Compiled at: 2020-05-01 08:37:20
# Size of source mod 2**32: 6330 bytes
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
import logging as log, numpy as np
from extensions.middle.InsertLayoutPropagationTransposes import is_input_data_in_correct_layout, is_output_data_in_correct_layout
import extensions.middle.ApplyNHWCtoNCHWpermutation as ApplyNHWCtoNCHWpermutation
from extensions.middle.pass_separator import PostMiddleStart
from mo.front.common.partial_infer.utils import int64_array
from mo.graph.graph import Graph, Node
from mo.middle.replacement import MiddleReplacementPattern
from mo.utils.error import Error

class ApplyPermutation(MiddleReplacementPattern):
    enabled = True
    force_clean_up = True
    graph_condition = [
     lambda graph: graph.graph['fw'] != 'kaldi']

    def run_after(self):
        return [
         ApplyNHWCtoNCHWpermutation, PostMiddleStart]

    def run_before(self):
        return []

    def find_and_replace_pattern(self, graph: Graph):
        self.merge_nodes_permutations(graph)
        self.permute_data_nodes_attrs(graph)
        self.permute_op_nodes_attrs(graph)
        self.permute_input_data(graph)

    @staticmethod
    def merge_nodes_permutations(graph: Graph):
        for node in graph.nodes():
            node = Node(graph, node)
            if node.kind != 'data':
                continue
            permutations = []
            for in_node in node.in_nodes():
                edge_attrs = node.graph.get_edge_data(in_node.id, node.id)[0]
                if 'permutation' in edge_attrs:
                    permutations.append(edge_attrs['permutation'])

            for out_node in node.out_nodes():
                edge_attrs = node.graph.get_edge_data(node.id, out_node.id)[0]
                if 'permutation' in edge_attrs:
                    permutations.append(edge_attrs['permutation'])

            final_permutations = []
            for p in permutations:
                if p is not None:
                    final_permutations.append(p.perm)
                else:
                    final_permutations.append(int64_array(np.arange(node.shape.size)))

            if len(final_permutations) == 0:
                continue
            if not all([np.array_equal(final_permutations[0], perm) for perm in final_permutations]):
                raise Error('Permutations requested for {} data node are not equal! List of permutations: {}'.format(node.name, [p.perm for p in permutations]))
            if node.has_valid('permutation'):
                assert np.array_equal(node.permutation, permutations[0])
            node['permutation'] = permutations[0]

    @staticmethod
    def permute_data_nodes_attrs(graph: Graph):
        for node in graph.get_data_nodes():
            if not node.has_valid('permutation'):
                continue
            if len(node.in_nodes()) != 0:
                edge_attrs = graph.get_edge_data(node.in_node(0).id, node.id)[0]
                if is_output_data_in_correct_layout(node.in_node(0), edge_attrs['out']):
                    log.debug('Do not permute data node attrs for node "{}" output port "{}"'.format(node.in_node(0).id, edge_attrs['out']))
                    continue
            if len(node.permutation.perm) == 0:
                continue
            node.shape = np.array(node.shape)[node.permutation.perm]
            if node.has_valid('value'):
                assert len(node.value.shape) == len(node.permutation.perm), 'Node {} has shape {} and permutation {} that does not match. Their lengths should be equal'.format(node.name, node.value.shape, node.permutation.perm)
                node.value = np.array(node.value.transpose(node.permutation.perm))

    @staticmethod
    def permute_op_nodes_attrs(graph: Graph):
        for node in graph.get_op_nodes():
            if node.has_valid('permute_attrs') and not node.has_and_set('nchw_layout'):
                try:
                    node.permute_attrs.permute_attrs(node)
                except Exception as e:
                    try:
                        raise Error("Can't permute attrs for node {}. Error message: {}".format(node.id, e))
                    finally:
                        e = None
                        del e

    @staticmethod
    def permute_input_data(graph: Graph):
        if graph.graph['layout'] != 'NHWC':
            return
        for node in graph.get_op_nodes():
            input_permutations = [(in_port, edge_attrs['input_permutation']) for in_port, edge_attrs in node.in_edges().items() if edge_attrs.get('input_permutation') is not None]
            for in_port, input_perm in input_permutations:
                permutation, port_info = input_perm
                direction, port = port_info.split(':')
                port = int(port)
                port_to_check = node.in_port(port) if direction == 'input' else node.out_port(port)
                if is_input_data_in_correct_layout(node, in_port) or len(port_to_check.data.get_shape()) >= 4:
                    permutation(node, port_info, in_port)

        graph.graph['layout'] = 'NCHW'