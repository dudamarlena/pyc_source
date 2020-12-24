# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extensions/ops/lstm_cell.py
# Compiled at: 2020-05-01 08:37:21
# Size of source mod 2**32: 3315 bytes
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
import networkx as nx
from mo.front.common.partial_infer.utils import mark_input_bins
from mo.graph.graph import Node, Graph
from mo.ops.op import Op
from mo.utils.error import Error

class LSTMCell(Op):
    __doc__ = ' A single LSTM cell (without a loop).\n\n        3 inputs:\n            - [0, required] input data (2D),\n            - [1, required] initial hidden state (2D),\n            - [2, required] initial cell state (2D),\n        \n        2 blobs:\n            - [3, required] LSTM FC weights\n            - [4, required] LSTM FC biases\n        \n        2 outputs:\n            - [required] output data / resulting hidden state (2D)\n            - [required] resulting cell state (2D)\n    '
    op = 'LSTMCell'

    def __init__(self, graph, attrs):
        mandatory_props = {'type':__class__.op, 
         'op':__class__.op, 
         'infer':__class__.infer, 
         'in_ports_count':5, 
         'out_ports_count':2}
        super().__init__(graph, mandatory_props, attrs)

    def supported_attrs(self):
        return [
         'hidden_size',
         'activations',
         'activation_alpha',
         'activation_beta',
         'clip']

    def backend_attrs(self):
        return [
         'hidden_size',
         (
          'activations',
          lambda node:           if node.activations is not None:
','.join(node.activations) # Avoid dead code: None),
         'activation_alpha',
         'activation_beta',
         'clip']

    @staticmethod
    def infer(node: Node):
        if node.has_and_set('extra_inputs') and not len(node.in_nodes()) == 8:
            raise AssertionError
        else:
            if not len(node.in_nodes()) == 5:
                raise AssertionError
            elif not len(node.out_nodes()) in (1, 2):
                raise AssertionError
            else:
                hidden_shape = node.in_node(1).shape.copy()
                cell_shape = node.in_node(2).shape.copy()
                mark_input_bins(node, start_port=3)
                node.out_node(0).shape = hidden_shape
                if len(node.out_nodes()) == 2:
                    node.out_node(1).shape = cell_shape
                hidden_size = hidden_shape[1]
                if node.has_valid('hidden_size'):
                    if node.hidden_size != hidden_size:
                        raise Error("Input shape {} for hidden size doesn't match pre-defined hidden_size in node {}".format(node.in_node(1).shape, node.soft_get('name')))
                else:
                    node['hidden_size'] = hidden_size
            assert cell_shape[1] == hidden_size
            input_shape = node.in_node(0).shape
            assert input_shape is not None
            assert hidden_shape[0] == cell_shape[0] == input_shape[0], 'States are not broadcastable by batch'