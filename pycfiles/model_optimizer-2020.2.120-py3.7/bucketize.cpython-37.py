# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extensions/ops/bucketize.py
# Compiled at: 2020-05-01 08:37:21
# Size of source mod 2**32: 2053 bytes
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
from mo.graph.graph import Node, Graph
from mo.ops.op import Op

class Bucketize(Op):
    op = 'Bucketize'

    def __init__(self, graph, attrs):
        mandatory_props = {'kind':'op', 
         'type':__class__.op, 
         'op':__class__.op, 
         'type_infer':self.type_infer, 
         'infer':self.infer, 
         'in_ports_count':2, 
         'out_ports_count':1}
        super().__init__(graph, mandatory_props, attrs)

    def supported_attrs(self):
        return [
         'with_right_bound']

    @staticmethod
    def type_infer(node):
        node.out_port(0).set_data_type(np.int32)

    @staticmethod
    def infer(node: Node):
        if not node.with_right_bound is not None:
            raise AssertionError('Attribute "with_right_bound" is not defined')
        else:
            assert len(node.in_nodes()) == 2, 'Incorrect number of inputs for {} node'.format(node.id)
            output_shape = node.in_port(0).data.get_shape()
            node.out_port(0).data.set_shape(output_shape)
            input_value = node.in_port(0).data.get_value()
            buckets_value = node.in_port(1).data.get_value()
            if input_value is not None and buckets_value is not None:
                node.out_port(0).data.set_value(np.digitize(input_value, buckets_value, right=(node.with_right_bound)))