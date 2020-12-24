# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extensions/middle/ConvertLayoutDependentOperations.py
# Compiled at: 2020-05-01 08:37:21
# Size of source mod 2**32: 4855 bytes
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
from extensions.ops.transpose import Transpose
from mo.front.common.layout import indices_mapping
from mo.graph.graph import Node, Graph
from mo.middle.replacement import MiddleReplacementPattern
from mo.ops.const import Const
from mo.ops.op import Op, PermuteAttrs

class ConvertLayoutDependentOperations(MiddleReplacementPattern):
    __doc__ = '\n         This pass finds all convolutions and in case if layout of convolution differs from graph layout\n         we insert permutes before and after convolution and convert convolution attributes\n    '
    enabled = True

    def run_after(self):
        from extensions.middle.pass_separator import MiddleStart
        return [
         MiddleStart]

    def find_and_replace_pattern(self, graph: Graph):
        for node in list(graph.nodes()):
            node = Node(graph, node)
            if node.kind == 'op' and node.has_valid('layout'):
                if node.layout != indices_mapping[len(node.layout)][graph.graph['layout']]:
                    input = node.in_node()
                    output = node.out_node()
                    if graph.graph['layout'] == 'NCHW':
                        permutation = PermuteAttrs.get_nhwc_to_nchw_permutation(len(node.layout))
                    else:
                        permutation = PermuteAttrs.get_nchw_to_nhwc_permutation(len(node.layout))
                edge_attrs = graph.get_edge_data(input.id, node.id)[0]
                graph.remove_edge(input.id, node.id)
                input_order_const = Const(graph, {'value': permutation.perm}).create_node_with_data()
                input_permute_op = Transpose(graph, dict(name=(node.name + '/Transpose_')))
                input_permute_data_node = input_permute_op.create_node_with_data([input, input_order_const])
                (graph.add_edge)((input_permute_data_node.id), (node.id), **edge_attrs)
                edge_attrs = graph.get_edge_data(node.id, output.id)[0]
                graph.remove_edge(node.id, output.id)
                input_data_node = Op.create_data_node(graph, node, {'shape': output.shape[permutation.perm]}, edge_attrs)
                output_order_const = Const(graph, {'value': permutation.inv}).create_node_with_data()
                output_permute_op = Transpose(graph, dict(name=(node.name + '/Transpose_'))).create_node_with_data([
                 input_data_node, output_order_const],
                  data_nodes=output)
                node.in_node()['permutation'] = permutation
                node.out_node()['permutation'] = permutation
                node.permute_attrs.permute_attrs(node)
                node.in_node()['permutation'] = None
                node.out_node()['permutation'] = None