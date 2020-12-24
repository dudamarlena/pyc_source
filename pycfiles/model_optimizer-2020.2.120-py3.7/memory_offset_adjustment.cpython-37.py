# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extensions/front/kaldi/memory_offset_adjustment.py
# Compiled at: 2020-05-01 08:37:19
# Size of source mod 2**32: 6491 bytes
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
import networkx as nx
from mo.front.common.replacement import FrontReplacementSubgraph
from mo.graph.graph import Graph, Node
from mo.ops.memoryoffset import MemoryOffset

def find_max_frame_time(node: Node):
    in_frame_time_max = 0
    should_align = False
    for inp in node.in_ports():
        if node.in_port(inp).disconnected():
            continue
        in_node = node.in_port(inp).get_source().node
        if in_node.frame_time > in_frame_time_max:
            in_frame_time_max = in_node.frame_time

    if in_frame_time_max == 0:
        return (
         in_frame_time_max, False)
    for inp in node.in_ports():
        if node.in_port(inp).disconnected():
            continue
        if in_frame_time_max != node.in_port(inp).get_source().node.frame_time:
            should_align = True
            break

    return (
     in_frame_time_max, should_align)


def align_frame_time(graph: Graph, node: Node, frame_time_max):
    for inp in node.in_ports():
        if node.in_port(inp).disconnected():
            continue
        in_node = node.in_port(inp).get_source().node
        in_node_out_port = node.in_port(inp).get_source()
        in_port = node.in_port(inp)
        if in_node.frame_time < frame_time_max:
            if in_node.op != 'Const':
                if in_node.op == 'MemoryOffset':
                    in_node.t = in_node.frame_time - frame_time_max
                    in_node.frame_time = in_node.t
                else:
                    mem_name = graph.unique_id('align_' + node.id)
                    memory_align = MemoryOffset(graph, attrs={'id':mem_name,  'name':mem_name, 
                     'pair_name':mem_name + '_pair', 
                     't':in_node.frame_time - frame_time_max, 
                     'splitted':False}).create_node()
                    if in_node.op == 'Parameter':
                        memory_align['element_size'] = in_node.shape[1]
                    in_port.get_connection().set_source(memory_align.out_port(0))
                    memory_align.in_port(0).connect(in_node_out_port)
                    memory_align['frame_time'] = memory_align.t
        if in_node.frame_time == frame_time_max and in_node.op == 'MemoryOffset':
            in_node_out_port.get_connection().set_source(in_node.in_port(0).get_source())
            graph.remove_node(in_node.id)


class MemoryOffsetAdjustment(FrontReplacementSubgraph):
    __doc__ = '\n    Pass used to fix wrong results in the following situation:\n                              input\n                              |                               ...   ...\n                             |                           MemoryOffset(k)                                |        |\n                             ...      |\n                              \\      |\n                               \\     |\n                               Concat\n    In Left branch we have MemoryOffset with k > 0 so we wait until kth frame will be calcualted. In right branch\n    we have no such offsets. As result we Concat (or use in any calculations with more than 1 input) kth frame from\n    left branch and 0th from right branch. So we need to add synchronization before Concat node. it can be done with\n    MemoryOffset(k) inserted before Concat.\n\n    Main idea of this change that when we found memoryOffset with t>0 we should re-calculate all delays relative to this\n    t.\n    '
    enabled = True
    graph_condition = [lambda graph: graph.graph['fw'] == 'kaldi']

    def run_before(self):
        from extensions.front.kaldi.split_memoryoffsets import SplitMemoryOffsets
        return [
         SplitMemoryOffsets]

    def find_and_replace_pattern(self, graph: Graph):
        should_continue = False
        for n in graph:
            if Node(graph, n).op == 'MemoryOffset' and Node(graph, n).t > 0:
                should_continue = True
                break

        if not should_continue:
            return
        try:
            nodes = list(nx.topological_sort(graph))
        except:
            return
        else:
            nx.set_node_attributes(G=graph, name='frame_time', values=(-1))
            for n in nodes:
                node = Node(graph, n)
                if node.frame_time < 0:
                    if node.op == 'MemoryOffset':
                        node.frame_time = node.in_port(0).get_source().node.frame_time + node.t
                    elif len(node.in_edges()) > 1:
                        in_frame_time_max, should_align = find_max_frame_time(node)
                        if should_align:
                            align_frame_time(graph, node, in_frame_time_max)
                        node.frame_time = in_frame_time_max
                    elif len(node.in_edges()) == 1:
                        node.frame_time = node.in_port(0).get_source().node.frame_time
                    else:
                        node.frame_time = 0

            for n in graph:
                node = Node(graph, n)
                if 'frame_time' in node:
                    del node['frame_time']