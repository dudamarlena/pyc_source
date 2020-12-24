# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extensions/back/DumpFakeQuantStat.py
# Compiled at: 2020-05-01 08:37:19
# Size of source mod 2**32: 2093 bytes
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
from mo.back.replacement import BackReplacementPattern
from mo.graph.graph import Graph
from mo.middle.passes.eliminate import remove_op_node_with_data_node

class DumpFakeQuantStat(BackReplacementPattern):
    enabled = True

    def find_and_replace_pattern(self, graph: Graph):
        intervals = {}
        for node in graph.get_op_nodes(type='FakeQuantize', keep_in_IR=False):
            prev_node = node.in_node().in_node()
            prev_node_id = prev_node.id
            prev_node_out_shape = prev_node.out_node()['shape']
            C = prev_node_out_shape[1]
            assert node.in_node(1).value.size == 1
            assert node.in_node(2).value.size == 1
            assert_msg = 'FakeQuantize cannot be removed because input and output intervals do not match'
            assert node.in_node(1).value == node.in_node(3).value, assert_msg
            assert node.in_node(2).value == node.in_node(4).value, assert_msg
            min = ', '.join([str(node.in_node(1).value.flatten()[0])] * C)
            max = ', '.join([str(node.in_node(2).value.flatten()[0])] * C)
            intervals[prev_node_id] = {'min':min,  'max':max}
            remove_op_node_with_data_node(graph, node)

        if intervals:
            if 'statistics' not in graph.graph:
                graph.graph['statistics'] = intervals
            else:
                graph.graph['statistics'].update(intervals)