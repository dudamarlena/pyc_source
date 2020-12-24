# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extensions/middle/RNNSequenceNormalizeToIE.py
# Compiled at: 2020-05-01 08:37:21
# Size of source mod 2**32: 9817 bytes
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
from copy import deepcopy
import numpy as np
from mo.front.common.partial_infer.utils import int64_array
from mo.graph.graph import Graph
from mo.middle.replacement import MiddleReplacementPattern
from mo.ops.const import Const
from mo.ops.op import Op
from mo.ops.reshape import Reshape

class RNNSequenceNormalize(MiddleReplacementPattern):
    __doc__ = '\n    This class normalize RNNSequence layers to IE-compatible from of weights, inputs and outputs.\n\n    In this pass next will be done:\n        1. Weights repack (squeeze all useless shapes in all blobls and concatenate W and R together, also add\n                            bin param and all similar staff )\n        1. UNSqueeze num directions (in states and )\n        2. Initial states squeeze\n        4. Renumbering inputs\n        5. Ports checks\n\n    After this normalization this layer will have next format of inputs:\n            0: X input data,    shape [batch_size, seq_len, input_size]\n            1: WR weights blob,  shape [M * hidden_size, hidden_size + input_size]\n            2: B biases blob,   shape [M * hidden_size]\n            3: (optional) sequence_length, shape [batch_size]\n            4: initial hidden state, shape  [batch_size, hidden_size]\n            5: (only for LSTM) initial cell state, shape [batch_size, hidden_size]\n            6: (optional for LSTM) Peepholes weights, shape  [(M - 1) * hidden_size]\n\n    '

    def run_after(self):
        import extensions.middle.DecomposeBidirectionalRNNSequence as DecomposeBidirectionalRNNSequence
        return [DecomposeBidirectionalRNNSequence]

    def pattern(self):
        return dict(nodes=[
         (
          'rnn_layer', dict(kind='op', type='RNNSequence')),
         (
          'input', dict(kind='data')),
         (
          'W', dict(kind='data')),
         (
          'R', dict(kind='data')),
         (
          'B', dict(kind='data'))],
          edges=[
         (
          'input', 'rnn_layer', {'in': 0}),
         (
          'W', 'rnn_layer', {'in': 1}),
         (
          'R', 'rnn_layer', {'in': 2}),
         (
          'B', 'rnn_layer', {'in': 3})])

    def replace_pattern(self, graph: Graph, match: dict):
        self.repack_weights(graph, match)
        if match['rnn_layer'].has_num_directions:
            self.unsqueeze_num_directions(graph, match)
        self.squeeze_initial_states(graph, match)
        self.reordering_inputs(graph, match)

    def repack_weights(self, graph: Graph, match: dict):
        lstm = match['rnn_layer']
        W, R, B = match['W'].value.copy(), match['R'].value.copy(), match['B'].value.copy()
        graph.remove_edge(match['W'].id, lstm.id)
        graph.remove_edge(match['R'].id, lstm.id)
        graph.remove_edge(match['B'].id, lstm.id)
        if lstm.op == 'GRU' and lstm.linear_before_reset:
            B_shape = np.array(B.shape)
            B_shape[3] = 4
            B_shape[2] = 1
            B_tmp = np.zeros(shape=B_shape)
            B_tmp[:, :, :, 0, :] = B[:, :, 0, 0, :] + B[:, :, 1, 0, :]
            B_tmp[:, :, :, 1, :] = B[:, :, 0, 1, :] + B[:, :, 1, 1, :]
            B_tmp[:, :, :, 2, :] = B[:, :, 0, 2, :][:, :, np.newaxis, :]
            B_tmp[:, :, :, 3, :] = B[:, :, 1, 2, :][:, :, np.newaxis, :]
            B = B_tmp
        else:
            B = np.add.reduce(B, axis=2, keepdims=True)
        assert len(W.shape) == 5
        assert len(R.shape) == 5
        WR = np.concatenate([W, R], axis=4)
        assert WR.shape[0] == 1
        assert WR.shape[1] == 1
        assert B.shape[0] == 1
        assert B.shape[1] == 1
        WR = WR.squeeze(axis=(0, 1))
        B = B.squeeze(axis=(0, 1))
        final_shape_WR = [
         WR.shape[0] * WR.shape[1], -1]
        assert final_shape_WR[0] == lstm.hidden_size * lstm.multiplier
        WR = WR.reshape(final_shape_WR)
        final_shape_B = final_shape_WR
        if lstm.op == 'GRU':
            if lstm.linear_before_reset:
                final_shape_B[0] = lstm.hidden_size * 4
        B = B.reshape(final_shape_B)
        B = B.squeeze(axis=(-1))
        for blob, port, name in [(WR, 1, 'weights'), (B, 2, 'biases')]:
            Op.create_and_connect_input_data_node(graph, lstm, {'value':blob, 
             'shape':np.array(blob.shape, dtype=np.int64)}, {'in':port, 
             'bin':name,  'permutation':None})

    @staticmethod
    def unsqueeze_num_directions(graph: Graph, match: dict):
        """ Assuming considered LSTM/GRU/RNN node should has num_directions in output shape and add Reshape
            to match it.
        """
        rnn_layer = match['rnn_layer']
        direction_dim = [
         1, 0, 0]
        for i in rnn_layer.out_nodes():
            old_data_node = rnn_layer.out_node(i)
            old_shape = old_data_node.shape.copy()
            new_shape = np.delete(old_shape, direction_dim[i])
            data = Op._create_data_node(graph, name=(rnn_layer.name + '/Out/{}/'.format(i)), attrs={'shape': new_shape})
            graph.remove_edge(rnn_layer.id, old_data_node.id)
            graph.add_edge((rnn_layer.id), (data.id), key=0, out=i)
            reshape = Reshape(graph, dict(dim=old_shape))
            reshape_dim_data = Const(graph, {'name':rnn_layer.name + '/SqueezeNumDirections/{}/Dim'.format(i),  'value':old_shape}).create_node_with_data()
            reshape.create_node_with_data([data, reshape_dim_data], dict(name=(rnn_layer.name + '/SqueezeNumDirections/{}'.format(i))),
              data_nodes=[
             old_data_node])

    @staticmethod
    def squeeze_initial_states(graph: Graph, match: dict):
        """
        Squeeze input initial states of recurrent node to 2-D shape.
        """
        hidden_init_port = 5
        cell_init_port = 6
        rnn_layer = match['rnn_layer']
        rnn_layer.add_sequence_of_ports(type='in', rng=(range(7)))
        reshape = Reshape(graph, {})
        assert hidden_init_port in rnn_layer.in_nodes()
        init_h = rnn_layer.in_node(hidden_init_port)
        edge_attrs = deepcopy(graph.get_edge_data(init_h.id, rnn_layer.id)[0])
        edge_attrs['in'] = hidden_init_port
        graph.remove_edge(init_h.id, rnn_layer.id)
        new_dim = int64_array([rnn_layer.in_node(0).shape[rnn_layer.batch_dim], rnn_layer.hidden_size])
        reshape_dim_data = Const(graph, {'name':rnn_layer.name + '/HiddenStateResizeDim',  'value':new_dim}).create_node_with_data()
        new_init_h = reshape.create_node_with_data([init_h, reshape_dim_data], dict(name=(rnn_layer.name + '/HiddenStateResize')))
        (graph.add_edge)((new_init_h.id), (rnn_layer.id), **edge_attrs)
        if rnn_layer.op == 'LSTM':
            assert cell_init_port in rnn_layer.in_nodes()
            init_c = rnn_layer.in_node(cell_init_port)
            edge_attrs = deepcopy(graph.get_edge_data(init_c.id, rnn_layer.id)[0])
            edge_attrs['in'] = cell_init_port
            graph.remove_edge(init_c.id, rnn_layer.id)
            reshape_dim_data = Const(graph, {'name':rnn_layer.name + '/CellStateResizeDim',  'value':new_dim}).create_node_with_data()
            new_init_c = reshape.create_node_with_data([init_c, reshape_dim_data], dict(name=(rnn_layer.name + '/CellStateResize')))
            (graph.add_edge)((new_init_c.id), (rnn_layer.id), **edge_attrs)

    @staticmethod
    def reordering_inputs(graph: Graph, match: dict):
        """
        Reorder (renumbering) inputs to described format. We need to renumber initial states ports.
        """
        rnn_layer = match['rnn_layer']
        assert 5 in rnn_layer.in_nodes()
        hidden_state_edge = graph.get_edge_data(rnn_layer.in_node(5).id, rnn_layer.id)
        hidden_state_edge[0]['in'] = 4
        if rnn_layer.op == 'LSTM':
            assert 6 in rnn_layer.in_nodes()
            cell_state_edge = graph.get_edge_data(rnn_layer.in_node(6).id, rnn_layer.id)
            cell_state_edge[0]['in'] = 5

    @staticmethod
    def ports_checks(graph: Graph, match: dict):
        """
            Check that all mandatory ports is present.
        """
        rnn_layer = match['rnn_layer']
        mandatory_ports = [0, 1, 2, 4]
        if rnn_layer.op == 'LSTM':
            mandatory_ports.append(5)
        assert set(rnn_layer.in_nodes().keys()) >= set(mandatory_ports)