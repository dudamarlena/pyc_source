# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extensions/middle/BlockLSTMtoLSTMSequence.py
# Compiled at: 2020-05-01 08:37:20
# Size of source mod 2**32: 13276 bytes
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
import extensions.ops.LSTM as LSTM
from mo.graph.graph import Graph
from mo.middle.replacement import MiddleReplacementPattern
from mo.utils.error import Error

class BlockLSTMtoLSTMSequence(MiddleReplacementPattern):
    __doc__ = '\n    MO virtual operation RNNSequence that converts to IE TensorIterator with LSTMCell inside supports 3 outputs:\n    0: concatenated hidden states over the whole time sequence,\n    1: last hidden state,\n    2: last cell state.\n\n    Replacer do several tasks:\n    1. Checks if current BlockLSTM can be translated to IR (IE does not support concatenated cell state output\n    which can be produced by BlockLSTM)\n    2. Searches for sub-graph, that takes last cell state out of unsupported concatenated cell state output.\n    We cut this sub-graph off in case if there are no other consumers of concatenated cell state output and we connect\n    BlockLSTM to consumers of this sub-graph by port producing last cell state output\n    3. Renumber input ports of BlockLSTM to match RNNSequence specification.\n    4. (Optional. Resolves by multiple checks) We cut the same sug-graph (as in 2) for concatenated cell states check\n    for better performance\n    '
    enabled = True

    def run_before(self):
        from extensions.middle.LSTMRNNSequenceToTensorIterator import LSTMToTensorIterator
        return [
         LSTMToTensorIterator]

    def run_after(self):
        from extensions.middle.pass_separator import MiddleStart
        from extensions.middle.RNNSequenceNormalizeToIE import RNNSequenceNormalize
        return [
         MiddleStart, RNNSequenceNormalize]

    def pattern(self):
        return dict(nodes=[
         (
          'BlockLSTM', dict(op='BlockLSTM')),
         (
          'concatenated_hidden_states', dict(kind='data')),
         (
          'mul', dict(op='Mul')),
         (
          'mul_data', dict(kind='data')),
         (
          'after_mul_op_to_the_rest_of_model', dict(kind='op')),
         (
          'concat_0', dict(op='ConcatV2')),
         (
          'concat_0_data', dict(kind='data')),
         (
          'reshape_0', dict(op='Reshape')),
         (
          'reshape_0_data', dict(kind='data')),
         (
          'gather_0', dict(op='Gather')),
         (
          'gather_0_data', dict(kind='data')),
         (
          'concatenated_cell_states_data', dict(kind='data')),
         (
          'concat_1', dict(op='ConcatV2')),
         (
          'concat_1_data', dict(kind='data')),
         (
          'reshape_1', dict(op='Reshape')),
         (
          'reshape_1_data', dict(kind='data')),
         (
          'gather_1', dict(op='Gather')),
         (
          'gather_1_data', dict(kind='data'))],
          edges=[
         (
          'BlockLSTM', 'concatenated_hidden_states', {'out': 0}),
         ('concatenated_hidden_states', 'mul'),
         ('mul', 'mul_data'),
         ('mul_data', 'after_mul_op_to_the_rest_of_model'),
         ('mul_data', 'concat_0'),
         ('concat_0', 'concat_0_data'),
         ('concat_0_data', 'reshape_0'),
         ('reshape_0', 'reshape_0_data'),
         ('reshape_0_data', 'gather_0'),
         ('gather_0', 'gather_0_data'),
         (
          'BlockLSTM', 'concatenated_cell_states_data', {'out': 1}),
         (
          'concatenated_cell_states_data', 'concat_1', {'in': 1}),
         ('concat_1', 'concat_1_data'),
         ('concat_1_data', 'reshape_1'),
         ('reshape_1', 'reshape_1_data'),
         ('reshape_1_data', 'gather_1'),
         ('gather_1', 'gather_1_data')])

    @staticmethod
    def replace_pattern(graph: Graph, match: dict):
        time_len = match['concatenated_hidden_states'].shape[0]
        valid_output_names = [
         'concat_1', 'concat_1_data', 'reshape_1', 'reshape_1_data', 'gather_1', 'gather_1_data']
        valid_output_node_ids = [match[name].id for name in valid_output_names]
        node_names_to_check_outputs = ['concatenated_cell_states_data', 'concat_1_data', 'reshape_1_data']
        for name in node_names_to_check_outputs:
            for node in match[name].out_nodes():
                if node.id not in valid_output_node_ids:
                    raise Error('BlockLSTM node {} has output which contains concatenated cell states over the whole time sequence. It is not replaceable by another output and is not supported originally'.format(match['BlockLSTM'].id))

        gather_indexes = match['gather_1'].in_node(1).value
        if len(gather_indexes) == 1:
            gather_index = gather_indexes[0]
        else:
            raise Error('BlockLSTM node {} has output which contains concatenated cell states over the whole time sequence. It is not replaceable by another output and is not supported originally'.format(match['BlockLSTM'].id))
        if gather_index != time_len:
            raise Error('BlockLSTM node {} has output which contains concatenated cell states over the whole time sequence. It is not replaceable by another output and is not supported originally'.format(match['BlockLSTM'].id))
        else:
            node = match['BlockLSTM']
            weights_node = node.in_node(1)
            biases_node = node.in_node(2)
            shift_const = node.forget_bias
            input_size = node.in_node(0).shape[(-1)]
            hidden_size = node.in_node(3).shape[(-1)]
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
            attrs = dict(graph.get_edge_data(match['gather_1'].id, match['gather_1_data'].id)[0])
            attrs.update({'out': 2})
            graph.remove_edge(match['BlockLSTM'].id, match['concatenated_cell_states_data'].id)
            graph.remove_edge(match['gather_1'].id, match['gather_1_data'].id)
            match['BlockLSTM'].add_output_port(attrs['out'])
            (graph.add_edge)((match['BlockLSTM'].id), (match['gather_1_data'].id), **attrs)
            h_init_port = 4
            c_init_port = 5
            if 4 in node.in_nodes():
                assert c_init_port not in node.in_nodes()
                cell_state_edge = graph.get_edge_data(node.in_node(4).id, node.id)
                cell_state_edge[0]['in'] = c_init_port
            if 3 in node.in_nodes():
                assert h_init_port not in node.in_nodes()
                hidden_state_edge = graph.get_edge_data(node.in_node(3).id, node.id)
                hidden_state_edge[0]['in'] = h_init_port
            new_attrs = {'sequence_dim':0,  'batch_dim':1, 
             'direction':'forward', 
             'hidden_size':match['concatenated_hidden_states'].shape[-1], 
             'format':'tf'}
            LSTM.update_node_stat(match['BlockLSTM'], new_attrs)
            data_to_mul = [n for n in match['mul'].in_nodes().values() if n.id != match['concatenated_hidden_states'].id]
            if len(data_to_mul) != 1:
                return
            data_to_mul = data_to_mul[0]
            if not data_to_mul.has_valid('value'):
                return
            data_to_mul_value = data_to_mul.value
            return np.all(data_to_mul_value == 1) or None
        attrs = dict(graph.get_edge_data(match['BlockLSTM'].id, match['concatenated_hidden_states'].id)[0])
        graph.remove_edge(match['BlockLSTM'].id, match['concatenated_hidden_states'].id)
        graph.remove_edge(match['mul'].id, match['mul_data'].id)
        (graph.add_edge)((match['BlockLSTM'].id), (match['mul_data'].id), **attrs)
        valid_output_names = [
         'mul_data', 'concat_0', 'concat_0_data', 'reshape_0', 'reshape_0_data', 'gather_0',
         'gather_0_data']
        valid_output_node_ids = [match[name].id for name in valid_output_names]
        node_names_to_check_outputs = ['mul_data', 'concat_0_data', 'reshape_0_data']
        list_of_concatenated_hidden_states_children_node_ids = []
        for name in node_names_to_check_outputs:
            for node in match[name].out_nodes():
                if node.id not in valid_output_node_ids:
                    list_of_concatenated_hidden_states_children_node_ids.append(node.id)

        if len(list_of_concatenated_hidden_states_children_node_ids) != 1:
            return
        conacenated_child_node_id = list_of_concatenated_hidden_states_children_node_ids[0]
        if conacenated_child_node_id != match['after_mul_op_to_the_rest_of_model'].id:
            return
        gather_indexes = match['gather_0'].in_node(1).value
        if len(gather_indexes) == 1:
            gather_index = gather_indexes[0]
        else:
            return
            if gather_index != time_len:
                return
            attrs = dict(graph.get_edge_data(match['gather_0'].id, match['gather_0_data'].id)[0])
            attrs.update({'out': 1})
            graph.remove_edge(match['mul_data'].id, match['concat_0'].id)
            graph.remove_edge(match['gather_0'].id, match['gather_0_data'].id)
            (graph.add_edge)((match['BlockLSTM'].id), (match['gather_0_data'].id), **attrs)