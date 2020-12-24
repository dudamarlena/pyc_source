# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mo/ops/unsqueeze.py
# Compiled at: 2020-05-01 08:37:22
# Size of source mod 2**32: 2945 bytes
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
from mo.front.common.partial_infer.utils import int64_array
from mo.graph.perm_inputs import PermuteInputs
from mo.ops.op import Op
from mo.utils.error import Error

class Unsqueeze(Op):
    __doc__ = '\n    The operation that inserts dimensions of size one into specific positions of the input layer. The dimensions are\n    specified in the second input.\n    '
    op = 'Unsqueeze'
    enabled = False

    def __init__(self, graph, attrs):
        super().__init__(graph, {'kind':'op', 
         'op':__class__.op, 
         'type':__class__.op, 
         'unsqueeze_dims':None, 
         'reinterp_shape':True, 
         'in_ports_count':2, 
         'out_ports_count':1, 
         'infer':__class__.infer}, attrs)

    @staticmethod
    def infer(node):
        if len(node.in_nodes()) <= 1:
            raise Error('There is no input with unsqueeze dims for the node {}'.format(node.soft_get('name')))
        else:
            unsqueeze_dims = node.in_port(1).data.get_value()
            if unsqueeze_dims is None:
                raise Error('The dimensions to unsqueeze are not defined for the node {}'.format(node.soft_get('name')))
            unsqueeze_dims = int64_array(unsqueeze_dims)
            input_value = node.in_port(0).data.get_value()
            input_shape = node.in_port(0).data.get_shape()
            if unsqueeze_dims.ndim == 0:
                unsqueeze_dims = int64_array([unsqueeze_dims.item()])
            unsqueeze_dims = int64_array([dim + len(node.in_port(0).data.get_shape()) + 1 if dim < 0 else dim for dim in unsqueeze_dims])
            if node.in_port(1).get_source().node.op == 'Const':
                node.in_port(1).data.set_value(unsqueeze_dims)
            output_shape = int64_array(input_shape.copy())
            for dim in unsqueeze_dims:
                output_shape = np.insert(output_shape, dim, 1)

            if input_value is not None:
                node.out_port(0).data.set_value(input_value.reshape(output_shape))
            else:
                node.out_port(0).data.set_shape(int64_array(output_shape))
        PermuteInputs().set_input_permutation(node.in_node(1), node, 'input:0', 'axis')