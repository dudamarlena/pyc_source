# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extensions/ops/GRUCell.py
# Compiled at: 2020-05-01 08:37:21
# Size of source mod 2**32: 2715 bytes
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
from mo.front.common.partial_infer.utils import mark_input_bins
from mo.graph.graph import Node, Graph
from mo.ops.op import Op
from mo.utils.error import Error

class GRUCell(Op):
    __doc__ = ' A single GRU cell (without a loop).\n\n        2 inputs:\n            - [0, required] input data (2D),\n            - [1, required] initial hidden state (2D),\n\n        2 blobs:\n            - [2, required] cell FC weights\n            - [3, required] cell FC biases\n\n        1 outputs:\n            - [required] output data / resulting hidden state (2D)\n    '
    op = 'GRUCell'

    def __init__(self, graph, attrs):
        mandatory_props = {'type':__class__.op, 
         'op':__class__.op, 
         'infer':__class__.infer, 
         'in_ports_count':4, 
         'out_ports_count':1}
        super().__init__(graph, mandatory_props, attrs)

    def supported_attrs(self):
        return [
         'hidden_size',
         'activations',
         'activation_alpha',
         'activation_beta',
         'clip',
         'linear_before_reset']

    def backend_attrs(self):
        return [
         'hidden_size',
         (
          'activations',
          lambda node:           if node.activations is not None:
','.join(node.activations) # Avoid dead code: None),
         'activation_alpha',
         'activation_beta',
         'clip',
         'linear_before_reset']

    @staticmethod
    def infer(node: Node):
        if not len(node.out_nodes()) in (1, 2):
            raise AssertionError
        else:
            hidden_shape = node.in_node(1).shape.copy()
            mark_input_bins(node, start_port=2)
            node.out_node(0).shape = hidden_shape
            hidden_size = hidden_shape[1]
            if node.has_valid('hidden_size'):
                if node.hidden_size != hidden_size:
                    raise Error("Input shape {} for hidden size doesn't match pre-defined hidden_size in node {}".format(node.in_node(1).shape, node.soft_get('name')))
            else:
                node['hidden_size'] = hidden_size