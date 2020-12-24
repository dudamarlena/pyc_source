# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extensions/front/reduce_axis_normalizer.py
# Compiled at: 2020-05-01 08:37:20
# Size of source mod 2**32: 3175 bytes
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
from extensions.ops.ReduceOps import reduce_map
from extensions.ops.range import Range
from extensions.ops.rank import Rank
from mo.front.common.replacement import FrontReplacementSubgraph
from mo.front.subgraph_matcher import SubgraphMatch
from mo.graph.graph import Graph
from mo.ops.const import Const

class ReduceAxisNormalizer(FrontReplacementSubgraph):
    __doc__ = '\n    Reduce operation requires information about axis, that is represented in original frameworks differently:\n        - by layer parameter\n        - by 1-port input value\n\n    ReduceAxisNormalizer reforms Reduce operations to store axis info in 1-port input.\n    '
    enabled = True
    force_shape_inference = True

    def pattern(self):
        return dict(nodes=[
         (
          'reduce', dict(kind='op', op=(lambda op: op in reduce_map)))],
          edges=[])

    def replace_sub_graph(self, graph: Graph, match: [dict, SubgraphMatch]):
        node = match['reduce']
        connected_in_ports = [port for port in node.in_ports().values() if not port.disconnected()]
        if len(connected_in_ports) == 1:
            if node.has('axis'):
                const = Const(graph, {'value': node.axis}).create_node()
                node.add_input_port(1, skip_if_exist=True)
                const.out_port(0).connect(node.in_port(1))
                del graph.node[node.id]['axis']
            else:
                node_name = node.name
                begin_of_range = Const(graph, dict(name=(node_name + '/range_begin_'), value=0)).create_node()
                step = Const(graph, dict(name=(node_name + '/range_step_'), value=1)).create_node()
                end_of_range = Rank(graph, dict(name=(node_name + '/range_end_'))).create_node()
                axes = Range(graph, dict(name=(node_name + '/axes_'))).create_node()
                begin_of_range.out_port(0).connect(axes.in_port(0))
                end_of_range.out_port(0).connect(axes.in_port(1))
                step.out_port(0).connect(axes.in_port(2))
                node.add_input_port(1, skip_if_exist=True)
                axes.out_port(0).connect(node.in_port(1))
                node.in_port(0).get_connection().get_source().connect(end_of_range.in_port(0))