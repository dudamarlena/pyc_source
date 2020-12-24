# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extensions/ops/unique.py
# Compiled at: 2020-05-01 08:37:21
# Size of source mod 2**32: 7241 bytes
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
import logging as log, networkx as nx, numpy as np
from mo.graph.graph import Node, Graph
from mo.ops.op import Op

class Unique(Op):
    __doc__ = ' The operation finds unique elements in 1-D tensor.\n        For more details see https://www.tensorflow.org/api_docs/python/tf/unique\n\n        attributes:\n            - sorted, indicates whether to sort the unique elements in ascending order or\n                      to return in the same order as they occur in the input\n            - return_inverse, indicates whether to output indices\n            - return_counts, indicates whether to output the counts of each unique element\n\n        1 input:\n            - [0, required] input tensor (1D)\n        \n        2 outputs:\n            - [0, required] tensor containing all of the unique elements of the input\n                            and sorted in the same order as in the input (1D)\n            - [1, optional] tensor of indices for each value of the input\n                            in the tensor of unique elements (1D)\n            - [2, optional] tensor with a number of occurences for each unique element\n                            in the input (1D)\n    '
    op = 'Unique'

    def __init__(self, graph, attrs):
        mandatory_props = {'type':__class__.op, 
         'op':__class__.op, 
         'infer':__class__.infer, 
         'in_ports_count':1, 
         'out_ports_count':3}
        super().__init__(graph, mandatory_props, attrs)

    def supported_attrs(self):
        return [
         'sorted',
         'return_inverse',
         'return_counts']

    @staticmethod
    def infer(node: Node):
        if node.has('sorted'):
            if not node.sorted in ('true', 'false'):
                raise AssertionError('Unique does not have valid sorted attribute')
            if node.has('return_inverse'):
                raise node.return_inverse in ('true', 'false') or AssertionError('Unique does not have valid return_inverse attribute')
            else:
                raise node.has('return_counts') and node.return_counts in ('true',
                                                                           'false') or AssertionError('Unique does not have valid return_counts attribute')
            assert len(node.in_nodes()) == 1, 'Unique must have one input'
            assert len(node.out_nodes()) <= 3, 'Unique must have less or equal to 3 outputs'
            max_num_outputs = 1
            if node.return_inverse == 'true':
                max_num_outputs += 1
            if node.return_counts == 'true':
                max_num_outputs += 1
            assert len(node.out_nodes()) <= max_num_outputs, 'The number of outputs in IR Unique layer must be less or equal to framework graph one'
            assert 0 in node.out_nodes(), 'The output with unique elements must remain in a graph'
            if len(node.out_nodes()) == 1:
                node.return_inverse = 'false'
                node.return_counts = 'false'
            if len(node.out_nodes()) == 2 and 1 in node.out_nodes() and node.return_inverse == 'true':
                if node.return_counts == 'true':
                    node.return_counts = 'false'
        else:
            if len(node.out_nodes()) == 2:
                if 2 in node.out_nodes():
                    if node.return_inverse == 'true':
                        if node.return_counts == 'true':
                            node.return_inverse = 'false'
            input_shape = node.in_node(0).shape
            raise input_shape is not None and input_shape.size == 1 or AssertionError('Unique accepts only 1-D input')
        for out_node_ind in node.out_nodes():
            assert out_node_ind < max_num_outputs, 'Unique has three outputs at most'
            node.out_node(out_node_ind).shape = input_shape

        input_value = node.in_node(0).value
        if input_value is None:
            return
        assert len(input_value.shape) == 1, 'Unique accepts only 1-D input'
        is_sorted = node.sorted == 'true'
        return_inverse = node.return_inverse == 'true'
        return_counts = node.return_counts == 'true'
        if is_sorted:
            unique_output = np.unique(input_value, return_inverse=return_inverse, return_counts=return_counts,
              return_index=False)
            unique_output = return_inverse or return_counts or [
             unique_output]
        else:
            sorted_uniques, sorted_index, sorted_inverse, sorted_counts = np.unique(input_value, return_index=True, return_inverse=True,
              return_counts=True)
            uniques = []
            inverse = []
            counts = []
            old_ind_by_elem = dict(zip(sorted_uniques, range(len(sorted_index))))
            new_ind_by_elem = dict()
            new_ind = 0
            for ind in np.sort(sorted_index):
                uniques.append(input_value[ind])
                old_ind = old_ind_by_elem[input_value[ind]]
                counts.append(sorted_counts[old_ind])
                new_ind_by_elem[input_value[ind]] = new_ind
                new_ind += 1

            inverse = [new_ind_by_elem[input_value[ind]] for ind in range(len(input_value))]
            unique_output = []
            unique_output.append(uniques)
            if return_inverse:
                unique_output.append(inverse)
            if return_counts:
                unique_output.append(counts)
            j = 0
            for out_node_ind in node.out_nodes():
                node.out_node(out_node_ind).value = np.array((unique_output[j]), dtype=(np.float))
                node.out_node(out_node_ind).shape = np.array((node.out_node(out_node_ind).value.shape), dtype=(np.int64))
                j += 1