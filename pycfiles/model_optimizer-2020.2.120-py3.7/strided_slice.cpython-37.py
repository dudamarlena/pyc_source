# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mo/ops/strided_slice.py
# Compiled at: 2020-05-01 08:37:22
# Size of source mod 2**32: 6164 bytes
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
from mo.front.common.partial_infer.slice import tf_strided_slice_infer
from mo.front.common.partial_infer.utils import int64_array
from mo.graph.graph import Node, Graph
from mo.ops.op import Op, PermuteAttrs
from mo.utils.utils import array_to_str

def extend_mask_according_ellipsis(ellipsis_mask, shrink_axis_mask, length_output_shape, attr_mask_extended, ins_value):
    if np.any(ellipsis_mask):
        idx = np.nonzero(ellipsis_mask)
        assert len(idx[0]) == 1
        insert_ind = idx[0][0]
    else:
        insert_ind = len(attr_mask_extended) - 1
    ellipse_ext = length_output_shape + np.count_nonzero(shrink_axis_mask) - len(attr_mask_extended)
    for i in range(0, ellipse_ext):
        attr_mask_extended.insert(insert_ind + i + 1, ins_value)

    return attr_mask_extended


def permute_array_with_ellipsis(node: Node, array: np.array, ins_value: int):
    """
    This function permutes masks according to permutation parameter. Several cases should be processed:
    * Some dimensions can be omitted in mask according to ellipsis mask
    * Mask length can be less than length of output dimensions plus shrinked dimensions
    * Mask have the same or more length than output
    """
    attr_mask_extended = list(array)
    if len(node.in_port(0).data.get_shape()) < 4:
        if len(node.out_port(0).data.get_shape()) < 4:
            return attr_mask_extended
    if len(attr_mask_extended) < len(node.out_port(0).data.get_shape()) + np.count_nonzero(node.shrink_axis_mask):
        attr_mask_extended = extend_mask_according_ellipsis(node.ellipsis_mask, node.shrink_axis_mask, len(node.out_port(0).data.get_shape()), attr_mask_extended, ins_value)
        perm = PermuteAttrs.get_nhwc_to_nchw_permutation(len(attr_mask_extended))
        attr_mask_extended = int64_array(attr_mask_extended)[perm.perm]
        return attr_mask_extended
    perm_len = len(node.out_port(0).data.get_shape()) + np.count_nonzero(node.shrink_axis_mask)
    perm = PermuteAttrs.get_nhwc_to_nchw_permutation(perm_len)
    perm_list = list(perm.perm)
    for i in range(perm_len, len(attr_mask_extended)):
        perm_list.append(i)

    return int64_array(attr_mask_extended)[int64_array(perm_list)]


def permute_masks(node: Node, permutation: PermuteAttrs.Permutation, attr: str):
    if not node.has_valid(attr):
        return
    node[attr] = permute_array_with_ellipsis(node, node[attr], attr in ('begin_mask',
                                                                        'end_mask'))
    return node[attr]


class StridedSlice(Op):
    op = 'StridedSlice'
    enabled = True

    def __init__(self, graph, attrs):
        super().__init__(graph, {'type':__class__.op, 
         'op':'StridedSlice', 
         'in_ports_count':4, 
         'out_ports_count':1, 
         'infer':__class__.infer}, attrs)

    def backend_attrs(self):
        al = list()

        def convert(attr):
            return lambda node: array_to_str(node, attr)

        for a in list(['new_axis_mask', 'shrink_axis_mask', 'ellipsis_mask', 'begin_mask', 'end_mask']):
            al.append((a, convert(a)))

        return al

    @staticmethod
    def infer(node: Node):
        tf_strided_slice_infer(node)
        if node.graph.graph['layout'] == 'NHWC':
            if node.out_port(0).data.get_value() is None:
                PermuteAttrs.create_permute_attrs(node, attrs=[('shrink_axis_mask', 'input:0', permute_masks),
                 (
                  'new_axis_mask', 'input:0', permute_masks),
                 (
                  'ellipsis_mask', 'input:0', permute_masks),
                 (
                  'begin_mask', 'input:0', permute_masks),
                 (
                  'end_mask', 'input:0', permute_masks)])
                for i in range(1, len(node.in_nodes())):
                    if node.in_node(i).value is not None and len(node.in_node(0).shape) > 3:
                        node.in_node(i).value = permute_array_with_ellipsis(node, node.in_node(i).value, 0)

                if np.any(node.ellipsis_mask):
                    for attr in ('new_axis_mask', 'shrink_axis_mask', 'begin_mask',
                                 'end_mask'):
                        node[attr] = int64_array(extend_mask_according_ellipsis(node.ellipsis_mask, node.shrink_axis_mask, len(node.out_port(0).data.get_shape()), list(node[attr]), attr in ('begin_mask',
                                                                                                                                                                                              'end_mask')))

                idx = np.nonzero(node.ellipsis_mask)
                node.ellipsis_mask[idx] = 0