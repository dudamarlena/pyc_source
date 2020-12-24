# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extensions/front/binary_quantize_normalization.py
# Compiled at: 2020-05-01 08:37:19
# Size of source mod 2**32: 2181 bytes
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
from mo.front.common.replacement import FrontReplacementPattern
from mo.graph.graph import Graph
from mo.ops.const import Const
from extensions.ops.elementwise import Add, Mul

class BinaryFakeQuantizeNormalization(FrontReplacementPattern):
    __doc__ = '\n    FakeQuantize in binary form has exceptional meaning of 1 and 2 input nodes.\n    This nodes values should be equal and express threshold to quantize tensors to two levels..\n    '
    enabled = True

    @staticmethod
    def pattern():
        return dict(nodes=[
         (
          'min_in', dict()),
         (
          'max_in', dict()),
         (
          'quantize', dict(op='FakeQuantize', levels=2))],
          edges=[
         (
          'min_in', 'quantize', {'in': 1}),
         (
          'max_in', 'quantize', {'in': 2})])

    def replace_pattern(self, graph: Graph, match: dict):
        quantize = match['quantize']
        sum_node = Add(graph, dict()).create_node()
        const = Const(graph, {'value': np.array(0.5)}).create_node()
        mul_node = Mul(graph, dict()).create_node()
        mul_node.in_port(0).connect(sum_node.out_port(0))
        mul_node.in_port(1).connect(const.out_port(0))
        quantize.in_port(1).get_connection().get_source().connect(sum_node.in_port(0))
        quantize.in_port(2).get_connection().get_source().connect(sum_node.in_port(1))
        quantize.in_port(1).disconnect()
        quantize.in_port(2).disconnect()
        mul_node.out_port(0).connect(quantize.in_port(1))
        mul_node.out_port(0).connect(quantize.in_port(2))