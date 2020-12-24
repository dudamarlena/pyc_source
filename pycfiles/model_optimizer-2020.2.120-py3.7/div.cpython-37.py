# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extensions/front/div.py
# Compiled at: 2020-05-01 08:37:19
# Size of source mod 2**32: 2335 bytes
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
from extensions.ops.elementwise import Mul, Pow
from mo.front.common.replacement import FrontReplacementPattern
from mo.front.tf.graph_utils import create_op_with_const_inputs
from mo.graph.graph import Graph, Node, rename_node

class Div(FrontReplacementPattern):
    enabled = True
    graph_condition = [lambda graph: not graph.graph['cmd_params'].generate_experimental_IR_V10]

    @staticmethod
    def div_to_mul_replacement(div: Node):
        if div.in_port(0).data.get_value() is not None:
            if div.in_port(1).data.get_value() is not None:
                return
        graph = div.graph
        name = div.soft_get('name', div.id)
        rename_node(node=div, name=(name + '/to_be_removed'))
        mul = Mul(graph, {'name': name}).create_node()
        rename_node(mul, name)
        div.in_port(0).get_connection().set_destination(mul.in_port(0))
        div.in_port(1).get_connection().set_destination(mul.in_port(1))
        div.out_port(0).get_connection().set_source(mul.out_port(0))
        reciprocal = create_op_with_const_inputs(graph, Pow, {1: np.float64(-1)}, {'name': name + '/reciprocal_'})
        mul.in_port(1).get_connection().insert_node(reciprocal)

    def find_and_replace_pattern(self, graph: Graph):
        for div in graph.get_op_nodes(op='Div'):
            self.div_to_mul_replacement(div)