# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extensions/ops/LSTM.py
# Compiled at: 2020-05-01 08:37:21
# Size of source mod 2**32: 2922 bytes
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
from extensions.ops.RNN import rnn_infer
from mo.graph.graph import Node, Graph
from mo.ops.op import Op

class LSTM(Op):
    op = 'LSTM'

    def __init__(self, graph, attrs):
        mandatory_props = {'type':'RNNSequence', 
         'op':__class__.op, 
         'blobs_wrb':False, 
         'has_num_directions':False, 
         'direction':'forward', 
         'infer':__class__.infer, 
         'multiplier':4, 
         'gate_order':None, 
         'normalized':False, 
         'multilayers':False, 
         'format':None, 
         'activation_alpha':None, 
         'activation_beta':None, 
         'activations':None, 
         'clip':None, 
         'input_forget':None, 
         'in_ports_count':7, 
         'out_ports_count':3}
        super().__init__(graph, mandatory_props, attrs)

    @staticmethod
    def supported_attrs():
        return [
         'hidden_size',
         'direction',
         'axis',
         'activation_alpha',
         'activation_beta',
         'activations',
         'clip']

    def backend_attrs(self):
        return [
         'hidden_size',
         'direction',
         'axis',
         'activation_alpha',
         'activation_beta',
         (
          'activations',
          lambda node:           if node.activations is not None:
','.join(node.activations) # Avoid dead code: None),
         'clip']

    @staticmethod
    def infer(node: Node):
        assert len(node.in_nodes()) >= 3
        assert len(node.in_nodes()) <= 7
        assert len(node.out_nodes()) <= 3
        rnn_infer(node, [1, 2])