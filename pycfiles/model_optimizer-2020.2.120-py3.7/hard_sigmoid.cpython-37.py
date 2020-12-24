# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extensions/ops/hard_sigmoid.py
# Compiled at: 2020-05-01 08:37:21
# Size of source mod 2**32: 1518 bytes
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

class HardSigmoid(Op):
    op = 'HardSigmoid'
    enabled = False

    def __init__(self, graph, attrs):
        super().__init__(graph, {'op':self.op, 
         'type':self.op, 
         'infer':self.infer, 
         'in_ports_count':3, 
         'out_ports_count':1}, attrs)

    @staticmethod
    def infer(node: Node):
        input_node = node.in_node(0)
        data_value = node.in_port(0).data.get_value()
        alpha_value = node.in_port(1).data.get_value()
        beta_value = node.in_port(2).data.get_value()
        if data_value is not None:
            if alpha_value is not None:
                if beta_value is not None:
                    node.out_port(0).data.set_value(np.clip(data_value * alpha_value + beta_value, 0, 1))
                    return
        node.out_port(0).data.set_shape(input_node.shape.copy())