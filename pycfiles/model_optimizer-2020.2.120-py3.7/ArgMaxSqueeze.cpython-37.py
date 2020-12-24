# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extensions/front/ArgMaxSqueeze.py
# Compiled at: 2020-05-01 08:37:19
# Size of source mod 2**32: 2066 bytes
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
from mo.front.common.replacement import FrontReplacementSubgraph
from mo.graph.graph import Graph
from mo.ops.const import Const
from mo.ops.squeeze import Squeeze

class ArgMaxSqueeze(FrontReplacementSubgraph):
    __doc__ = '\n        In some frameworks ArgMax operation has keepdims attribute that indicates whether to stay a dimension along\n        which maximum is computed or not. In case of keepdims=0 this dimension should be removed but ArgMax operation in\n        IR format is not designed to cover this case. So we should additionally add Squeeze operation right after ArgMax\n        for this case.\n    '
    op = 'ArgMax'
    enabled = True

    def pattern(self):
        return dict(nodes=[('argmax', dict(op='ArgMax', keepdims=0))], edges=[])

    def replace_sub_graph(self, graph: Graph, match: dict):
        node = match['argmax']
        connected_ports = [port for port in node.in_ports().values() if not port.disconnected()]
        squeeze_node = Squeeze(graph, dict()).create_node([], dict(name=(node.name + '/Squeeze')))
        if len(connected_ports) == 2:
            node.in_port(1).get_source().connect(squeeze_node.in_port(1))
        else:
            axis_node = Const(graph, {'value': node.axis}).create_node()
            squeeze_node.in_port(1).connect(axis_node.out_port(0))
        node.out_port(0).get_connection().set_source(squeeze_node.out_port(0))
        node.out_port(0).connect(squeeze_node.in_port(0))
        return []