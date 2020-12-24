# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extensions/ops/space_to_depth.py
# Compiled at: 2020-05-01 08:37:21
# Size of source mod 2**32: 2245 bytes
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
from mo.front.common.partial_infer.utils import int64_array
from mo.graph.graph import Node, Graph
from mo.ops.op import Op

class SpaceToDepth(Op):
    op = 'SpaceToDepth'

    def __init__(self, graph, attrs):
        mandatory_props = {'op':self.op, 
         'type':self.op, 
         'mode':'blocks_first', 
         'infer':self.infer, 
         'in_ports_count':1, 
         'out_ports_count':1}
        super().__init__(graph, mandatory_props, attrs)

    def supported_attrs(self):
        if self.ir_version == 10:
            return [
             'mode', 'block_size']
        return []

    @staticmethod
    def infer(node: Node):
        in_shape = node.in_node().shape
        if in_shape.size != 4:
            log.error("TensorFlow SpaceToDepth operation is supported for 4D 'NHWC' input layout only. Current input shape is '{}'".format(in_shape))
            return
        N, H, W, C = in_shape
        block_size = node['block_size']
        if H % block_size or W % block_size:
            log.error("Spatial dimensions of input tensor of SpaceToDepth operation have to be divisible by SpaceToDepth 'block_size' parameter. Input tensor shape = {}. Spatial dimensions = {},{}. block_size = {}".format(in_shape, H, W, block_size))
            return
        out_shape = [
         N, int(H / block_size), int(W / block_size), int(C * block_size ** 2)]
        assert np.prod(in_shape) == np.prod(out_shape)
        node.out_node().shape = int64_array(out_shape)