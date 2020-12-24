# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extensions/ops/TensorArrayWrite.py
# Compiled at: 2020-05-01 08:37:21
# Size of source mod 2**32: 1986 bytes
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
from mo.graph.graph import Node, Graph
from mo.ops.op import Op
from mo.utils.utils import match_shapes

class TensorArrayWriter(Op):
    op = 'TensorArrayWriteV3'

    def __init__(self, graph, attrs):
        mandatory_props = {'type':__class__.op, 
         'op':__class__.op, 
         'infer':TensorArrayWriter.array_infer}
        super().__init__(graph, mandatory_props, attrs)

    @staticmethod
    def array_infer(node: Node):
        assert len(node.in_nodes()) == 4
        handle = node.in_node(0)
        index = node.in_node(1)
        value = node.in_node(2)
        flow_in = node.in_node(3)
        value_shape = value.shape
        ta_node = Node(node.graph, str(handle.value))
        if ta_node.has_valid('element_shape'):
            if len(ta_node.element_shape) > 0:
                assert match_shapes(ta_node['element_shape'], value.shape), 'Shapes are not compatible: {} and {}'.format(ta_node['element_shape'], value.shape)
        ta_node['element_shape'] = value_shape
        output_shape = flow_in.shape
        output_value = flow_in.value
        for _, out_node in node.graph.out_edges(node.id):
            node.graph.node[out_node]['shape'] = np.array(output_shape)
            node.graph.node[out_node]['value'] = None if output_value is None else np.array(output_value)