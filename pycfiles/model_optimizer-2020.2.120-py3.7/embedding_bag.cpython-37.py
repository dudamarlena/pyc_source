# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extensions/ops/embedding_bag.py
# Compiled at: 2020-05-01 08:37:21
# Size of source mod 2**32: 2570 bytes
"""
 Copyright (c) 2020 Intel Corporation

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
from mo.front.common.partial_infer.utils import int64_array
from mo.graph.graph import Node, Graph
from mo.ops.op import Op

class EmbeddingBag(Op):
    __doc__ = '\n     This is nn.EmbeddingBag from Pytorch. It is a simple lookup table that stores embeddings of a fixed dictionary and\n     size and computes sums or means of "bags" of embeddings, without instantiating the intermediate embeddings.\n     Inputs:\n      0: Weights (num_embeddings, embedding_dim) - the lookup table\n      1: Indices (N,) - indices to get from lookup table\n      2: Offsets (B,) - index in indices tensor on which each bag starts\n     Output:\n      0: Embeddings (B, embedding_dim)\n    '
    op = 'EmbeddingBag'
    enabled = False

    def __init__(self, graph, attrs):
        super().__init__(graph, {'op':self.op, 
         'type':None, 
         'infer':self.infer, 
         'in_ports_count':3, 
         'out_ports_count':1}, attrs)

    def supported_attrs(self):
        return [
         'mode', 'scale_grad_by_freq']

    @staticmethod
    def infer(node: Node):
        name = node.soft_get('name', node.id)
        connected_in_ports = {idx:port for idx, port in node.in_ports().items() if not port.disconnected() if not port.disconnected()}
        if not (len(connected_in_ports) == 3 and 0 in connected_in_ports and 1 in connected_in_ports and 2 in connected_in_ports):
            raise AssertionError("EmbeddingBag should have 3 connected input port, but it doesn't for node: `{}`. Ports: {}".format(name, connected_in_ports))
        weights = node.in_port(0).data.get_value()
        if not (weights is not None and len(weights.shape) == 2):
            raise AssertionError
        input_shape = node.in_port(1).data.get_shape()
        assert input_shape is not None
        offsets_shape = node.in_port(2).data.get_shape()
        if not (offsets_shape is not None and len(offsets_shape) == 1):
            raise AssertionError
        node.out_port(0).data.set_shape(int64_array([offsets_shape[0], weights.shape[1]]))