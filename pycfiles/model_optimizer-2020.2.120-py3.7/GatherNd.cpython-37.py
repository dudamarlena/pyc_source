# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extensions/ops/GatherNd.py
# Compiled at: 2020-05-01 08:37:21
# Size of source mod 2**32: 1410 bytes
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

class GatherNd(Op):
    op = 'GatherNd'

    def __init__(self, graph, attrs):
        mandatory_props = {'op':__class__.op, 
         'infer':__class__.infer, 
         'in_ports_count':2, 
         'out_ports_count':1}
        super().__init__(graph, mandatory_props, attrs)

    def supported_attrs(self):
        return []

    @staticmethod
    def infer(node: Node):
        input_node = node.in_node(0)
        indices = node.in_node(1).value
        assert indices is not None
        output_shape = list(indices.shape[:-1]) + list(input_node.shape[indices.shape[(-1)]:])
        node.out_node().shape = np.array(output_shape, dtype=(np.int64))