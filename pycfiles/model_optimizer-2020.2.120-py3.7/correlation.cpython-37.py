# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extensions/ops/correlation.py
# Compiled at: 2020-05-01 08:37:21
# Size of source mod 2**32: 2439 bytes
"""
 Copyright (C) 2017-2020 Intel Corporation

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
from math import ceil
import numpy as np
from mo.graph.graph import Node, Graph
from mo.ops.op import Op

class CorrelationOp(Op):
    op = 'Correlation'

    def __init__(self, graph, attrs):
        mandatory_props = {'type':__class__.op, 
         'op':__class__.op, 
         'in_ports_count':1, 
         'out_ports_count':1, 
         'infer':CorrelationOp.corr_infer}
        super().__init__(graph, mandatory_props, attrs)

    def supported_attrs(self):
        return [
         'pad',
         'kernel_size',
         'max_displacement',
         'stride_1',
         'stride_2',
         'single_direction',
         'do_abs',
         'correlation_type']

    @staticmethod
    def corr_infer(node: Node):
        outn = node.out_node(0)
        inn = node.in_node(0)
        outn.shape = np.zeros(4, dtype=int)
        outn.shape[0] = inn.shape[0]
        bottomchannels = inn.shape[1]
        paddedbottomheight = inn.shape[2]
        paddedbottomwidth = inn.shape[3] + 2 * node.pad
        kernel_radius_ = (node.kernel_size - 1) / 2
        border_size_ = node.max_displacement + kernel_radius_
        outn.shape[3] = ceil(float(paddedbottomwidth - border_size_ * 2) / node.stride_1)
        outn.shape[2] = ceil(float(paddedbottomheight - kernel_radius_ * 2) / node.stride_1)
        neighborhood_grid_radius_ = node.max_displacement / node.stride_2
        if node.single_direction != 0:
            neighborhood_grid_width_ = neighborhood_grid_radius_ + 1
        else:
            neighborhood_grid_width_ = neighborhood_grid_radius_ * 2 + 1
        outn.shape[1] = neighborhood_grid_width_ * neighborhood_grid_width_