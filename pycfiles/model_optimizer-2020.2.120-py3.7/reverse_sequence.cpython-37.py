# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extensions/ops/reverse_sequence.py
# Compiled at: 2020-05-01 08:37:21
# Size of source mod 2**32: 1563 bytes
"""
 Copyright (C) 2017-2020 Intel Corporation

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
from mo.graph.graph import Graph
from mo.ops.op import Op

class ReverseSequence(Op):
    op = 'ReverseSequence'

    def __init__(self, graph, attrs):
        mandatory_props = {'type':__class__.op, 
         'seq_axis':None, 
         'batch_axis':0, 
         'op':__class__.op, 
         'in_ports_count':2, 
         'out_ports_count':1, 
         'infer':__class__.infer, 
         'in_ports_count':2, 
         'out_ports_count':1}
        super().__init__(graph, mandatory_props, attrs)

    def supported_attrs(self):
        return [
         'seq_axis', 'batch_axis']

    @staticmethod
    def infer(node):
        input_data_shape = node.in_node(0).shape
        assert input_data_shape is not None
        assert node.has_valid('seq_axis')
        assert node.has_valid('batch_axis')
        assert len(node.out_nodes()) == 1
        node.out_node().shape = input_data_shape.copy()