# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mo/ops/broadcast.py
# Compiled at: 2020-05-01 08:37:22
# Size of source mod 2**32: 2182 bytes
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
from mo.graph.perm_inputs import PermuteInputs
from mo.ops.op import Op

class Broadcast(Op):
    __doc__ = ' Broadcast tensor to a given shape with optional axis parameter\n\n        Inputs:\n            [0] - tensor to be broadcasted\n            [1] - shape to be broadcast to\n            [2] - optional axis paramater that which axis are allowed to be broadcasted\n    '
    op = 'Broadcast'
    enabled = True

    def __init__(self, graph, attrs):
        super().__init__(graph, {'kind':'op', 
         'type':__class__.op, 
         'op':__class__.op, 
         'in_ports_count':3, 
         'out_ports_count':1, 
         'force_precision_in_ports':{1:'int64' if graph.graph['cmd_params'].generate_experimental_IR_V10 else 'int32', 
          2:'int64' if graph.graph['cmd_params'].generate_experimental_IR_V10 else 'int32'}, 
         'infer':__class__.infer}, attrs)

    @staticmethod
    def infer(node: Node):
        b_value = node.in_port(0).data.get_value()
        b_shape = node.in_port(1).data.get_value()
        assert b_shape is not None
        node.out_port(0).data.set_shape(b_shape)
        PermuteInputs().set_input_permutation(node.in_node(1), node, 'output:0', 'shape')
        if b_value is not None:
            if not node.has_and_set('stop_value_propagation'):
                new_value = np.broadcast_to(b_value, b_shape)
                node.out_port(0).data.set_value(new_value)