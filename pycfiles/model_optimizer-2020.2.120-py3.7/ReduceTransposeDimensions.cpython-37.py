# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extensions/back/ReduceTransposeDimensions.py
# Compiled at: 2020-05-01 08:37:19
# Size of source mod 2**32: 6057 bytes
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
import logging as log, numpy as np
from mo.back.replacement import BackReplacementPattern
from extensions.back.OptimizeTransposeReshapeSequence import set_reshape_new_output_shape
from mo.front.common.partial_infer.utils import int64_array
from mo.graph.graph import Graph

def sequential_dims(order: np.array):
    """
    Returns first instance (counting from left) of the sequential dimensions in the 'order'
    :param order: order to look for sequential dims
    :return: list of indices of the sequential dimensions. If sequential dimensions are not found then return None.
    """
    start_ind = cur_ind = 0
    while cur_ind + 1 < len(order):
        if order[cur_ind] + 1 == order[(cur_ind + 1)]:
            cur_ind += 1
        else:
            if start_ind < cur_ind:
                return list(range(start_ind, cur_ind + 1))
            cur_ind += 1
            start_ind = cur_ind

    if start_ind < cur_ind:
        return list(range(start_ind, cur_ind + 1))


def merge_permute_order_dimensions(dims: list, permute_order: np.array):
    """
    Creates updated permutation for a given permutation order and the *input* dimension indices to be merged into one.
    :param dims: the input tensor dimensions indices to merge
    :param permute_order: the permutation order
    :return: the new permutation order after merging of the specified dimensions into one
    """
    assert len(dims) >= 2
    new_permute_order = list()
    for permute_index in permute_order:
        if permute_index < permute_order[dims[0]]:
            new_permute_order.append(permute_index)
        else:
            if permute_index > permute_order[dims[(-1)]]:
                new_permute_order.append(permute_index - len(dims) + 1)

    return int64_array(new_permute_order)


def merge_dims(dims_to_merge: np.array, shape: np.array):
    """
    Merge several sequential specified dims into one.

    The function does not support magic number "0" in the 'shape'.
    :param dims_to_merge: the dimensions indices to merge
    :param shape: shape to merge
    :return: new shape with merged specified dims
    """
    for ind in range(len(dims_to_merge) - 1):
        assert dims_to_merge[ind] + 1 == dims_to_merge[(ind + 1)], 'The dims to merge must be sequential'

    if not 0 not in shape:
        raise AssertionError('The value 0 is not supported during merging of the shape')
    else:
        result = list()
        if dims_to_merge[0] != 0:
            result.extend(shape[:dims_to_merge[0]])
        if -1 in shape[dims_to_merge]:
            result.append(-1)
        else:
            result.append(np.prod(shape[dims_to_merge]))
    if dims_to_merge[(-1)] + 1 != len(shape):
        result.extend(shape[dims_to_merge[(-1)] + 1:])
    return int64_array(result)


class ReduceTransposeDimensions(BackReplacementPattern):
    __doc__ = '\n    Transformation looks for the Transpose layers with sequential dimensions in the permutation order and merges them into\n    one thus reducing the number of dimensions. The transformation is applied to 5D+ permutations only.\n    '
    enabled = False

    def run_after(self):
        import extensions.back.OptimizeTransposeReshapeSequence as OptimizeTransposeReshapeSequence
        return [
         OptimizeTransposeReshapeSequence]

    def run_before(self):
        import extensions.back.ReshapeMutation as ReshapeMutation
        import extensions.back.TransposeToPermute as TransposeToPermute
        return [
         ReshapeMutation, TransposeToPermute]

    @staticmethod
    def pattern():
        return dict(nodes=[
         (
          'reshape_1', dict(kind='op', type='Reshape')),
         (
          'reshape_1_data', dict(kind='data')),
         (
          'permute', dict(kind='op', type='Transpose')),
         (
          'permute_data', dict(kind='data')),
         (
          'reshape_2', dict(kind='op', type='Reshape'))],
          edges=[
         ('reshape_1', 'reshape_1_data'),
         ('reshape_1_data', 'permute'),
         ('permute', 'permute_data'),
         ('permute_data', 'reshape_2')])

    @staticmethod
    def replace_pattern(graph: Graph, match: dict):
        permute_node = match['permute']
        reshape_1_node = match['reshape_1']
        order = permute_node.in_port(1).data.get_value().copy()
        if len(order) >= 5:
            log.debug('Trying to merge dimensions of the Transpose layer "{}"'.format(permute_node.soft_get('name')))
            seq_dims = sequential_dims(order)
            while seq_dims is not None:
                permute_input_shape = permute_node.in_port(0).data.get_shape().copy()
                new_reshape_dims = merge_dims(order[seq_dims], permute_input_shape)
                new_permute_order = merge_permute_order_dimensions(seq_dims, order)
                assert reshape_1_node.has('dim')
                set_reshape_new_output_shape(reshape_1_node, new_reshape_dims)
                permute_node.in_port(1).data.set_value(new_permute_order)
                permute_node.infer(permute_node)
                order = permute_node.in_port(1).data.get_value().copy()
                seq_dims = sequential_dims(order)