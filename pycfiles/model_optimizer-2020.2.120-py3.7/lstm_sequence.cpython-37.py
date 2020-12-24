# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extensions/ops/lstm_sequence.py
# Compiled at: 2020-05-01 08:37:21
# Size of source mod 2**32: 6392 bytes
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
import numpy as np
from mo.front.common.partial_infer.utils import mark_input_bins
from mo.graph.graph import Node, add_opoutput, Graph
from mo.ops.op import Op

class LSTMSequence(Op):
    __doc__ = " Implements a layer that incorporates LSTM cell in a loop like it is specified in ONNX\n\n        It is assumed that there is no equivalent of this op in IE,\n        so it is considered as intermediate operation that will be translated differently.\n        We define type for this operation to enable debuggin at IE side.\n\n        There are several flavors of this op depending on how it was created and in which framework.\n        There are several attributes that specifies the LSTM flavor:\n            - ONNX/LSTM gives this op in non-normalized form and will require normalization\n                as a separate transformation (see LSTMSequenceNormalize middle transformation);\n                in this case blobs_wrb=True. Normalized weights/biases for MatMul is used when\n                blobs_wrb=True.\n            - ONNX/LSTM defines output shape as 4D: [seq_length, num_directions, batch_size,\n                hidden_size], where num_directions = 1 is supported only. In this case\n                has_num_directions=True. Otherwise, output is 3D and doesn't contain num_directions.\n            - Depending on the original framework, `format` attrtibutes is specified accordingly.\n                Its value controls which normalize transformations are called.\n    "
    op = 'LSTMSequence'

    def __init__(self, graph, attrs):
        mandatory_props = {'type':'__LSTMSequence', 
         'op':__class__.op, 
         'blobs_wrb':False, 
         'has_num_directions':False, 
         'direction':'forward', 
         'num_layers':1, 
         'infer':__class__.infer, 
         'blob_bidirectional_split':lambda node: (
          LSTMSequence.split_helper(node, 0, 'forward'),
          LSTMSequence.split_helper(node, 1, 'reverse'))}
        super().__init__(graph, mandatory_props, attrs)

    def supported_attrs(self):
        return [
         'hidden_size',
         'direction',
         'batch_dim',
         'sequence_dim',
         'blobs_wrb',
         'has_num_directions',
         'format']

    def backend_attrs(self):
        return [
         'hidden_size']

    @staticmethod
    def split_helper(node, index: int, direction: str):
        return Op._create_data_node((node.graph),
          name=(node.name + '/SplittedBiLSTM/{}/'.format(direction)),
          attrs={'value':node.value[index], 
         'shape':np.array(node.value[index].shape, dtype=np.int64)})

    @staticmethod
    def infer(node: Node):
        if not len(node.in_nodes()) >= 3:
            raise AssertionError
        else:
            if not len(node.in_nodes()) <= 7:
                raise AssertionError
            else:
                assert len(node.out_nodes()) <= 3
                assert node.batch_dim <= 1
                assert node.sequence_dim <= 1
                assert node.batch_dim != node.sequence_dim
                assert node.direction in ('forward', 'reverse', 'bidirectional')
                if node.blobs_wrb:
                    mark_input_bins(node, ['W', 'R', 'B'])
                else:
                    mark_input_bins(node)
            input_shape = node.in_node(0).shape
            assert len(input_shape) == 3
            for port in (2, 3):
                if port in node.in_nodes() and len(node.in_node(port).in_nodes()) > 0 and 'zero_shapes' in node.in_node(port).in_node():
                    for i in node.in_node(port).in_node().zero_shapes:
                        if node.in_node(port).shape[i] != input_shape[i]:
                            node.in_node(port).value = np.repeat((node.in_node(port).value), (input_shape[i]), axis=i)
                            node.in_node(port).shape[i] = input_shape[i]

            out_shape = np.array([input_shape[node.sequence_dim], input_shape[node.batch_dim], node.hidden_size], dtype=(np.int64))
            if node.has_num_directions and not node.sequence_dim == 0:
                raise AssertionError('If has_num_directions == True, then node.sequence_dim should be equal 0, but it is {}'.format(node.sequence_dim))
        num_directions = 2 if node.direction in ('bidirectional', ) else 1
        num_layers = node.num_layers
        if node.has_num_directions:
            out_shape = np.insert(out_shape, 1, np.int64(num_directions))
        node.out_node(0).shape = out_shape
        state_size = np.array([input_shape[1], node.hidden_size], dtype=(np.int64))
        if node.has_num_directions:
            state_size = np.insert(state_size, 0, num_directions * num_layers)
        for i in (1, 2):
            if i not in node.out_nodes():
                data_node = Op._create_data_node((node.graph),
                  name=(node.node + '/ExtraOutput/' + str(i)),
                  attrs={'executable': True})
                node.graph.add_edge((node.id), (data_node.id), key=0, out=i)
                add_opoutput(node.graph, data_node.id, 0, False)
            else:
                data_node = node.out_node(i)
            data_node.shape = state_size.copy()