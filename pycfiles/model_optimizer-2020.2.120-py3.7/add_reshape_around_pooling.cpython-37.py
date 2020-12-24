# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extensions/front/kaldi/add_reshape_around_pooling.py
# Compiled at: 2020-05-01 08:37:19
# Size of source mod 2**32: 4011 bytes
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
from extensions.ops.elementwise import Mul, Pow
from extensions.ops.split import VariadicSplit
from mo.front.common.partial_infer.utils import int64_array
from mo.front.common.replacement import FrontReplacementPattern
from mo.front.tf.graph_utils import create_op_node_with_second_input, create_op_with_const_inputs
from mo.graph.graph import Graph
from mo.ops.concat import Concat
from mo.ops.const import Const
from mo.ops.reshape import Reshape
from mo.ops.shape import Shape

class ReplacePoolingReshape(FrontReplacementPattern):
    __doc__ = "\n        This pass adds Reshapes around a Pooling layer for reshaping from NH to NCHW\n        For example:\n            Let's suppose we have next graph:\n\n            Prev_Layer [N, H] -> Pooling [N, C, H, W] -> Next_Layer [N, H]\n\n            In this case Pooling takes only [N, H] from input tensor in 3rd dim\n            So this pass will convert this graph to the next one:\n\n            Prev_Layer [N, H] -> Reshape -> Pooling [N, C=1, H, W=1] -> Reshape -> Next_Layer [N, H]\n    "

    def run_before(self):
        from extensions.front.kaldi.add_permute_after_convolution import ReplaceConvolutionTranspose
        return [ReplaceConvolutionTranspose]

    def pattern(self):
        return dict(nodes=[('pool', dict(op='Pooling'))], edges=[])

    @staticmethod
    def replace_pattern(graph: Graph, match: dict):
        node = match['pool']
        if node.pool_step is None:
            node.stride = int64_array([1, 1, node.window[(-1)], node.window[(-1)]])
        shape = Shape(graph, {}).create_node()
        shape.in_port(0).connect(node.in_port(0).get_source())
        split = create_op_with_const_inputs(graph, VariadicSplit, {1:int64_array(0),  2:int64_array([1, -1])}, {'out_ports_count': 2}, shape)
        node_pool_stride = Const(graph, {'value': int64_array([node.pool_stride])}).create_node()
        pow_node = create_op_node_with_second_input(graph, Pow, int64_array([-1]))
        pow_node.in_port(0).connect(node_pool_stride.out_port(0))
        mul = Mul(graph, {}).create_node()
        mul.in_port(0).connect(split.out_port(1))
        mul.in_port(1).connect(pow_node.out_port(0))
        const_1 = Const(graph, {'value': int64_array([1])}).create_node()
        concat = Concat(graph, {'in_ports_count':4,  'axis':0}).create_node()
        concat.in_port(0).connect(split.out_port(0))
        concat.in_port(3).connect(mul.out_port(0))
        concat.in_port(2).connect(const_1.out_port(0))
        concat.in_port(1).connect(node_pool_stride.out_port(0))
        reshape_in = Reshape(graph, {'name': '/Reshape/' + node.name}).create_node()
        reshape_in.in_port(1).connect(concat.out_port(0))
        reshape_out = create_op_node_with_second_input(graph, Reshape, int64_array([0, -1]), {'name': node.name + '/Reshape/'})
        source = node.in_port(0).get_source()
        node.in_port(0).get_connection().set_source(reshape_in.out_port(0))
        reshape_in.in_port(0).connect(source)
        node.out_port(0).get_connection().set_source(reshape_out.out_port(0))
        node.out_port(0).connect(reshape_out.in_port(0))