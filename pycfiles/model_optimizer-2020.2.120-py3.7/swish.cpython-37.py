# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extensions/front/tf/swish.py
# Compiled at: 2020-05-01 08:37:20
# Size of source mod 2**32: 1432 bytes
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
from extensions.ops.activation_ops import Sigmoid
from extensions.ops.elementwise import Mul
from mo.front.common.replacement import FrontReplacementOp
from mo.graph.graph import Node, Graph

class Swish(FrontReplacementOp):
    op = 'swish_f32'
    enabled = True

    def replace_op(self, graph: Graph, node: Node):
        mul_node = Mul(graph, {'name': node.name + '/mul_'}).create_node()
        sigmoid_node = Sigmoid(graph, {'name': node.name + '/sigmoid_'}).create_node()
        node.in_port(0).get_connection().get_source().connect(mul_node.in_port(0))
        node.in_port(0).get_connection().get_source().connect(sigmoid_node.in_port(0))
        sigmoid_node.out_port(0).connect(mul_node.in_port(1))
        return [
         mul_node.id]