# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mo/ops/expand_dims.py
# Compiled at: 2020-05-01 08:37:22
# Size of source mod 2**32: 2804 bytes
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
from mo.graph.graph import Node
from mo.ops.op import Op
from mo.utils.error import Error

class ExpandDims(Op):
    __doc__ = '\n    The ExpandDims layer adds dimensions with shape 1 to the specified positions. The positions is a layer attribute,\n    not a separate input.\n    '
    op = 'ExpandDims'
    enabled = False

    def __init__(self, graph, attrs):
        super().__init__(graph, {'type':None, 
         'op':__class__.op, 
         'reinterp_shape':True, 
         'infer':__class__.infer, 
         'expand_axis':None, 
         'in_ports_count':1, 
         'out_ports_count':1}, attrs)

    @staticmethod
    def infer(node: Node):
        input_node = node.in_nodes()[0]
        output_node = node.out_node()
        if input_node.shape is None:
            return
        if not len(node.in_nodes()) == 1:
            raise AssertionError('Wrong number of inputs to the layer {}'.format(node.soft_get('name')))
        else:
            if not node.has_valid('expand_axis'):
                raise Error('ExpandDims axis is not defined for node {}'.format(node.soft_get('name')))
            expand_axes = node.expand_axis
            if expand_axes is None:
                raise Error('The "expand_axis" attribute is None for node "{}"'.format(node.soft_get('name')))
            if isinstance(expand_axes, int):
                expand_axes = int64_array([expand_axes])
            else:
                if expand_axes.ndim == 0:
                    expand_axes = expand_axes.reshape([1])
        for expand_axis in expand_axes:
            if expand_axis < 0:
                expand_axis += len(input_node.shape) + 1

        expand_axes = sorted(expand_axes)
        for expand_axis in expand_axes:
            output_node.shape = np.insert(input_node.shape, expand_axis, [1])

        output_node.shape = output_node.shape.astype(np.int64)
        if input_node.value is not None:
            output_node.value = input_node.value.reshape(output_node.shape)