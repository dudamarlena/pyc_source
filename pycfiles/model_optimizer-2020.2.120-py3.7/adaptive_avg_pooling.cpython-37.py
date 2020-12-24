# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extensions/ops/adaptive_avg_pooling.py
# Compiled at: 2020-05-01 08:37:21
# Size of source mod 2**32: 2306 bytes
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
from mo.graph.graph import Graph, Node
from mo.ops.op import Op
from mo.ops.pooling import Pooling
from mo.front.common.partial_infer.utils import int64_array

class AdaptiveAvgPooling(Op):
    __doc__ = '\n    Non-reshape-able op.\n    '
    enabled = False
    op = 'AdaptiveAvgPooling'

    def __init__(self, graph, attrs):
        super().__init__(graph, {'type':None, 
         'op':self.op, 
         'infer':__class__.infer, 
         'in_ports_count':1, 
         'out_ports_count':1}, attrs)

    @classmethod
    def infer(cls, node: Node):
        input_shape = node.in_node(0).shape
        input_h = input_shape[2]
        input_w = input_shape[3]
        output_h = node.output_size[0]
        output_w = node.output_size[1]
        stride_h = input_h // output_h
        stride_w = input_w // output_w
        kernel_h = input_h - (output_h - 1) * stride_h
        kernel_w = input_w - (output_w - 1) * stride_w
        data = {'window':int64_array([1, 1, kernel_h, kernel_w]), 
         'stride':int64_array([1, 1, stride_h, stride_w]), 
         'pad':int64_array([[0, 0], [0, 0], [0, 0], [0, 0]]), 
         'pad_spatial_shape':int64_array([[0, 0], [0, 0]]), 
         'pool_method':'avg', 
         'exclude_pad':'false', 
         'output_spatial_shape':None, 
         'spatial_dims':None, 
         'channel_dims':int64_array([1]), 
         'batch_dims':int64_array([0]), 
         'layout':'NCHW', 
         'rounding_type':'floor', 
         'pooling_convention':'valid'}
        Pooling.update_node_stat(node, data)
        Pooling.infer(node)