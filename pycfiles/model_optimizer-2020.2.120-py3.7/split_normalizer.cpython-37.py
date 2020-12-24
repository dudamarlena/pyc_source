# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extensions/front/split_normalizer.py
# Compiled at: 2020-05-01 08:37:20
# Size of source mod 2**32: 5493 bytes
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
import numpy as np
from extensions.ops.split import Split, VariadicSplit
from mo.front.common.replacement import FrontReplacementOp
from mo.front.common.replacement import FrontReplacementSubgraph
from mo.front.tf.graph_utils import create_op_with_const_inputs
from mo.graph.graph import Graph
from mo.ops.squeeze import Squeeze

class SqueezeAxis(FrontReplacementOp):
    __doc__ = '\n    Split-like operations from original frameworks split tensor by a certain `axis` dimension, removing\n    dimension over which splitting is performed. The "Split" layer of IE doesn\'t do that.\n    This replacer inserts Squeeze operation for each output of the Split nodes to remove the dimension.\n\n    It is applicable to Unpack from TF operation and MxNet SliceChannel\n    '
    enabled = True

    def run_before(self):
        return [
         AttributedSplitToSplit, AttributedVariadicSplitToVariadicSplit]

    def find_and_replace_pattern(self, graph: Graph):
        for node in graph.get_op_nodes(squeeze_axis=True):
            name = node.soft_get('name', node.id)
            assert node.has_valid('axis'), 'Unknown axis to squeeze for node {}'.format(name)
            for out_port in node.out_ports().values():
                squeeze_node = create_op_with_const_inputs(graph, Squeeze, {1: np.array(node.axis)}, {'name': name + '/Squeeze_'})
                out_port.get_connection().insert_node(squeeze_node)


class SplitInputsReconnect(FrontReplacementSubgraph):
    __doc__ = '\n    Reconnect input ports to fit IR specification\n\n    The Split operation in original frameworks (e.g. TF) may have different semantics than IR specification states:\n        IE: 0 - input data to Split, 1 - axis of splitting\n        TF: 0 - axis of splitting, 1 - input data to Split\n    '
    enabled = True

    def find_and_replace_pattern(self, graph: Graph):
        for node in graph.get_op_nodes(op='Split', input_port=1):
            axis_src = node.in_port(0).get_source()
            node.in_port(0).disconnect()
            node.in_port(1).get_connection().set_destination(node.in_port(0))
            node.in_port(1).connect(axis_src)
            del node['input_port']


class AttributedSplitToSplit(FrontReplacementSubgraph):
    enabled = True

    def find_and_replace_pattern(self, graph: Graph):
        for node in graph.get_op_nodes(op='AttributedSplit'):
            name = node.soft_get('name', node.id)
            axis = node.soft_get('axis', None)
            assert axis is not None, 'AttributedSplit should have `axis` parameter set, but it`s not for node {}'.format(name)
            num_splits = node.soft_get('num_splits', None)
            assert num_splits is not None, 'AttributedSplit should have `num_splits` parameter set, but it`s not for node {}'.format(name)
            split = create_op_with_const_inputs(graph, Split, {1: np.int64(axis)}, {'name':name + '/Split', 
             'num_splits':num_splits})
            for idx, port in node.out_ports().items():
                port.get_connection().set_source(split.out_port(idx))

            node.in_port(0).get_connection().set_destination(split.in_port(0))
            graph.remove_node(node.id)


class AttributedVariadicSplitToVariadicSplit(FrontReplacementSubgraph):
    enabled = True

    def find_and_replace_pattern(self, graph: Graph):
        for node in graph.get_op_nodes(op='AttributedVariadicSplit'):
            name = node.soft_get('name', node.id)
            axis = node.soft_get('axis', None)
            assert axis is not None, 'AttributedVariadicSplit should have `axis` parameter set, but it`s not for node {}'.format(name)
            size_splits = node.soft_get('size_splits', None)
            assert size_splits is not None, 'AttributedVariadicSplit should have `size_splits` parameter set, but it`s not for node {}'.format(name)
            split = create_op_with_const_inputs(graph, VariadicSplit, {1:np.int64(axis),  2:size_splits}, {'name':name + '/VariadicSplit', 
             'out_ports_count':len(size_splits)})
            for idx, port in node.out_ports().items():
                port.get_connection().set_source(split.out_port(idx))

            node.in_port(0).get_connection().set_destination(split.in_port(0))
            graph.remove_node(node.id)


class VariadicSplitInputsSwap(FrontReplacementSubgraph):
    enabled = True

    def find_and_replace_pattern(self, graph: Graph):
        for node in graph.get_op_nodes(op='VariadicSplit', swap_axis_and_split_size_inputs=True):
            axis_src = node.in_port(2).get_source()
            node.in_port(2).disconnect()
            node.in_port(1).get_connection().set_destination(node.in_port(2))
            node.in_port(1).connect(axis_src)