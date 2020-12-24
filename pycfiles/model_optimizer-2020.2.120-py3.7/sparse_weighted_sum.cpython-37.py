# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extensions/ops/sparse_weighted_sum.py
# Compiled at: 2020-05-01 08:37:21
# Size of source mod 2**32: 2038 bytes
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
from mo.graph.graph import Node, Graph
from mo.ops.op import Op

class ExperimentalSparseWeightedSum(Op):
    op = 'ExperimentalSparseWeightedSum'
    enabled = True

    def __init__(self, graph, attrs):
        super().__init__(graph, {'kind':'op', 
         'type':__class__.op, 
         'op':__class__.op, 
         'reduce_op':None, 
         'type_infer':self.type_infer, 
         'infer':self.infer, 
         'in_ports_count':6, 
         'out_ports_count':1, 
         'version':'experimental'}, attrs)

    def supported_attrs(self):
        return []

    @staticmethod
    def type_infer(node):
        params_table_type = node.in_port(3).get_data_type()
        node.out_port(0).set_data_type(params_table_type)

    @staticmethod
    def infer(node: Node):
        if not len(node.in_nodes()) == 5:
            assert len(node.in_nodes()) == 6, 'Incorrect number of inputs for {} node'.format(node.id)
        batch_size = node.in_port(2).data.get_value()[0]
        num_features = node.in_port(3).data.get_shape()[1:]
        output_shape = int64_array([batch_size] + num_features.tolist())
        node.out_port(0).data.set_shape(output_shape)