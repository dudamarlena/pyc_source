# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extensions/ops/sparse_fill_empty_rows.py
# Compiled at: 2020-05-01 08:37:21
# Size of source mod 2**32: 3361 bytes
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

class SparseFillEmptyRows(Op):
    __doc__ = ' The operation fills empty rows in the input 2-D sparse tensor with a default value.\n        For more details see https://www.tensorflow.org/api_docs/cc/class/tensorflow/ops/sparse-fill-empty-rows\n\n        4 inputs:\n            - [0, required] input indices of the sparse tensor (2D),\n            - [1, required] input values of the sparse tensor (1D),\n            - [2, required] shape of the sparse tensor. Value of this input is required for the Model Optimizer (1D),\n            - [3, required] default value to insert at rows missing from the input sparse tensor (0D),\n        \n        3 outputs:\n            - [0, optional] indices of the filled sparse tensor (2D)\n            - [1, optional] values of the filled sparse tensor (1D)\n            - [2, optional] indicator of whether the dense row was missing in the input sparse tensor (1D)\n    '
    op = 'SparseFillEmptyRows'

    def __init__(self, graph, attrs):
        mandatory_props = {'type':__class__.op, 
         'op':__class__.op, 
         'infer':__class__.infer, 
         'in_ports_count':4, 
         'out_ports_count':3}
        super().__init__(graph, mandatory_props, attrs)

    def supported_attrs(self):
        return []

    @staticmethod
    def infer(node: Node):
        if not len(node.in_nodes()) == 4:
            raise AssertionError
        else:
            shape = node.in_node(2)
            if not (shape.value is not None and shape.value.size == 2):
                raise AssertionError('SparseFillEmptyRows is supported only with constant shape value')
            shape_value = np.array((shape.value), dtype=(np.int64))
            default_value = node.in_node(3)
            raise default_value.shape is not None and len(default_value.shape) == 0 or AssertionError('Default value for SparseFillEmptyRows must be scalar')
        for out_node_ind in node.out_nodes():
            if out_node_ind == 0:
                node.out_node(0).shape = np.array([np.prod(shape_value), 2], dtype=(np.int64))
                continue
            elif out_node_ind == 1:
                node.out_node(1).shape = np.array([np.prod(shape_value)], dtype=(np.int64))
                continue
            elif out_node_ind == 2:
                node.out_node(2).shape = np.array([shape_value[0]], dtype=(np.int64))
                continue
            else:
                log.error('SparseFillEmptyRows has only three outputs')
                return