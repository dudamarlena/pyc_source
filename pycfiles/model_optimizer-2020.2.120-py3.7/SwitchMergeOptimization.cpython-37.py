# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extensions/front/tf/SwitchMergeOptimization.py
# Compiled at: 2020-05-01 08:37:20
# Size of source mod 2**32: 5117 bytes
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
from extensions.ops.select import Select
from mo.graph.graph import Graph
from mo.front.common.replacement import FrontReplacementSubgraph

class SwitchMergeOptimization(FrontReplacementSubgraph):
    __doc__ = "\n    Optimization for case, when combination of Switches have one common condition and can be expressed as Select node.\n\n    This transformation matches too big number of instances for models with many BatchNorm layers with the same input\n    from the model input data node with training/inference flag. So the transformation is implemented as a simple graph\n    traversal instead of regular pattern-based approach.\n    \n    The following pattern is checked:\n        nodes=[('Merge', dict(kind='op', op='Merge')),\n               ('Switch_2_input', dict(kind='data')),\n               ('Switch_2', dict(kind='op', op='Switch')),\n               ('Switch_2_data', dict(kind='data')),\n               ('op', dict(kind='op')),\n               ('op_data', dict(kind='data')),\n               ('Switch', dict(kind='op', op='Switch')),\n               ('Switch_data', dict(kind='data')),\n               ('Switch_1', dict(kind='op', op='Switch')),\n               ('Switch_1_data', dict(kind='data')),\n               ('cond_data', dict(kind='data')),\n               ('identity', dict(kind='op', op='Identity')),\n               ('identity_data', dict(kind='data')),\n               ],\n        edges=[\n               ('Switch_2_input', 'Switch_2', {'in': 0}),\n               ('Switch_2', 'Switch_2_data', {'out': 1}),\n               ('Switch_2_data', 'Merge'),\n               ('cond_data', 'Switch_2', {'in': 1}),\n               ('cond_data', 'Switch_1', {'in': 1}),\n               ('cond_data', 'Switch', {'in': 1}),\n               ('Switch_1', 'Switch_1_data', {'out': 0}),\n               ('Switch', 'Switch_data', {'out': 0}),\n               ('Switch_1_data', 'op', {'in': 1}),\n               ('Switch_data', 'op', {'in': 0}),\n               ('op', 'op_data'),\n               ('op_data', 'identity'),\n               ('identity', 'identity_data'),\n               ('identity_data', 'Merge'),\n               ],\n    "
    enabled = True

    def find_and_replace_pattern(self, graph: Graph):
        for merge in graph.get_op_nodes(op='Merge'):
            for merge_switch_in_port in range(2):
                if merge.in_port(merge_switch_in_port).disconnected() or merge.in_port(merge_switch_in_port).get_source().node.op != 'Switch':
                    continue
                switch_2 = merge.in_port(merge_switch_in_port).get_source().node
                if merge.in_port(1 - merge_switch_in_port).disconnected() or merge.in_port(1 - merge_switch_in_port).get_source().node.op != 'Identity':
                    continue
                false_value_port = merge.in_port(1 - merge_switch_in_port).get_source()
                true_value_port = switch_2.in_port(0).get_source()
                op = false_value_port.node.in_port(0).get_source().node
                if op.in_port(0).disconnected() or op.in_port(0).get_source().node.op != 'Switch':
                    continue
                switch = op.in_port(0).get_source().node
                if op.in_port(1).disconnected() or op.in_port(1).get_source().node.op != 'Switch':
                    continue
                switch_1 = op.in_port(1).get_source().node
                if switch.in_port(1).get_source() == switch_1.in_port(1).get_source() and switch.in_port(1).get_source() == switch_2.in_port(1).get_source():
                    select = Select(graph, dict(name=(merge.soft_get('name') + '/Select/'), format='tf')).create_node()
                    select.in_port(0).connect(switch.in_port(1).get_source())
                    select.in_port(1).connect(true_value_port)
                    select.in_port(2).connect(false_value_port)
                    merge.out_port(0).get_connection().set_source(select.out_port(0))
                    if not (1 in op.in_ports() and 0 in op.in_ports()):
                        raise AssertionError
                    op.in_port(0).disconnect()
                    op.in_port(1).disconnect()
                    switch.in_port(0).get_connection().set_destination(op.in_port(0))
                    switch_1.in_port(0).get_connection().set_destination(op.in_port(1))
                    graph.remove_nodes_from(nodes=[switch_1.id, switch.id, switch_2.id, merge.id])
                    break