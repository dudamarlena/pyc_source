# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mo/ops/memoryoffset.py
# Compiled at: 2020-05-01 08:37:22
# Size of source mod 2**32: 3182 bytes
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
from mo.front.common.partial_infer.elemental import copy_shape_infer
from mo.graph.graph import Graph, Node
from mo.ops.op import Op
from mo.utils.error import Error

class MemoryOffset(Op):
    op = 'MemoryOffset'
    enabled = True

    def __init__(self, graph, attrs):
        super().__init__(graph, {'op':'MemoryOffset', 
         'pair_name':None, 
         'has_default':False, 
         'infer':__class__.infer, 
         'in_ports_count':1, 
         'out_ports_count':1}, attrs)

    def supported_attrs(self):
        return [
         't']

    @staticmethod
    def infer(node: Node):
        if not node.in_port(0).disconnected():
            copy_shape_infer(node)
            pair_node = Node(node.graph, node.pair_name)
            pair_node.out_port(0).data.set_shape(node.out_port(0).data.get_shape())
        else:
            pair_node = Node(node.graph, node.pair_name)
            if pair_node.in_port(0).data.get_shape() is not None:
                node.out_port(0).data.set_shape(pair_node.in_port(0).data.get_shape())
                copy_shape_infer(pair_node)
            else:
                if pair_node.has_valid('element_size'):
                    node.out_port(0).data.set_shape(np.array([1, pair_node['element_size']]))
                else:
                    if pair_node.in_port(0).get_source().node.has_valid('out-size'):
                        out_size = pair_node.in_port(0).get_source().node['out-size']
                        node.out_port(0).data.set_shape(np.array([1, out_size]))
                    else:
                        if pair_node.in_port(0).get_source().node.op == 'Add' and pair_node.in_port(0).get_source().node.in_port(0).get_source().node.has_valid('out-size'):
                            out_size = pair_node.in_port(0).get_source().node.in_port(0).get_source().node['out-size']
                            node.out_port(0).data.set_shape(np.array([1, out_size]))
                        else:
                            if pair_node.in_port(0).get_source().node.has_valid('in_dim'):
                                out_size = pair_node.in_port(0).get_source().node['in_dim']
                                node.out_port(0).data.set_shape(np.array([1, out_size]))
                            else:
                                raise Error("Can't calculate MemoryOffset shape for node {}. ".format(node.id) + 'Possibly you need to add shape for it through --input_shape')