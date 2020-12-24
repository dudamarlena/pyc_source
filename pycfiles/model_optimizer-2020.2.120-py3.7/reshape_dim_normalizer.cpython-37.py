# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extensions/front/reshape_dim_normalizer.py
# Compiled at: 2020-05-01 08:37:20
# Size of source mod 2**32: 2244 bytes
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
from extensions.front.pass_separator import FrontStart
from mo.front.common.replacement import FrontReplacementSubgraph
from mo.front.subgraph_matcher import SubgraphMatch
from mo.graph.graph import Graph
from mo.ops.const import Const
from mo.utils.error import Error

class ReshapeDimNormalizer(FrontReplacementSubgraph):
    __doc__ = '\n    Reshape operation requires information about output dimensions, that is represented in original frameworks\n    differently:\n        - by layer parameter\n        - by 1-port input value\n\n    This transformation reforms Reshape operations to store dim info in 1-port input.\n    '
    enabled = True
    force_shape_inference = True

    def run_before(self):
        return [
         FrontStart]

    def run_after(self):
        from extensions.front.freeze_placeholder_value import FreezePlaceholderValue
        return [
         FreezePlaceholderValue]

    def pattern(self):
        return dict(nodes=[
         (
          'reshape', dict(kind='op', op='Reshape'))],
          edges=[])

    def replace_sub_graph(self, graph: Graph, match: [dict, SubgraphMatch]):
        node = match['reshape']
        connected_in_ports = [port for port in node.in_ports().values() if not port.disconnected()]
        if len(connected_in_ports) == 1:
            if node.has('dim'):
                const = Const(graph, {'value': node.dim}).create_node()
                node.add_input_port(1, skip_if_exist=True)
                const.out_port(0).connect(node.in_port(1))
                del node['dim']
            else:
                raise Error('The `dim` attribute for node {} is not set'.format(node.op))