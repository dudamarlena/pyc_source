# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extensions/middle/TF_lstm_cell_to_generic.py
# Compiled at: 2020-05-01 08:37:21
# Size of source mod 2**32: 3795 bytes
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
from mo.graph.graph import Graph
from mo.middle.replacement import MiddleReplacementPattern

class TensorFlowLSTMtoGeneric(MiddleReplacementPattern):
    __doc__ = '\n    Resolves all differences in TensorFlow LSTMCell and Inference Engine LSTMCell:\n    - weights transposing\n    - shift_const value addition to biases\n    - extra inputs deletion\n    '
    enabled = True

    def run_after(self):
        from extensions.middle.pass_separator import MiddleStart
        return [
         MiddleStart]

    def run_before(self):
        from extensions.middle.permute_tensor_iterator import TransposeTensorIteratorLSTM
        return [
         TransposeTensorIteratorLSTM]

    def pattern(self):
        return dict(nodes=[
         (
          'lstm', dict(op='LSTMCell', tf=True))],
          edges=[])

    def replace_pattern(self, graph: Graph, match: dict):
        weights_node = match['lstm'].in_node(3)
        biases_node = match['lstm'].in_node(4)
        node = match['lstm']
        shift_const = node.shift_const
        assert len(weights_node.out_nodes()) == 1
        assert len(biases_node.out_nodes()) == 1
        input_size = node.in_node(0).shape[1]
        hidden_size = node.in_node(1).shape[1]
        weights = weights_node.value
        biases = biases_node.value
        assert weights.shape[0] == input_size + hidden_size, 'weights.shape={} input_size={} hidden_size={}'.format(weights.shape, input_size, hidden_size)
        assert weights.shape[1] == biases.shape[0] == 4 * hidden_size, 'weights.shape={} biases.shape={} hidden_size={}'.format(weights.shape, biases.shape, hidden_size)
        weights = weights.reshape([
         weights.shape[0],
         4,
         hidden_size])
        biases = biases.reshape([
         4,
         hidden_size])
        gate_reorder = [
         2, 0, 1, 3]
        weights = np.take(weights, gate_reorder, axis=1)
        biases = np.take(biases, gate_reorder, axis=0)
        biases[0] += shift_const
        weights = weights.reshape([weights.shape[0], -1])
        biases = biases.flatten()
        weights = weights.transpose()
        weights_node.value = weights
        weights_node.shape = np.array((weights.shape), dtype=(np.int64))
        biases_node.value = biases
        biases_node.shape = np.array((biases.shape), dtype=(np.int64))
        for i in range(len(node.inputs), len(node.inputs) + len(node.extra_inputs)):
            node.graph.remove_edge(node.in_node(i).id, node.id)