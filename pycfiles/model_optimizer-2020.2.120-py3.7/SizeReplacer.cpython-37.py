# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extensions/front/tf/SizeReplacer.py
# Compiled at: 2020-05-01 08:37:20
# Size of source mod 2**32: 1697 bytes
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
from extensions.ops.ReduceOps import ReduceProd
from mo.front.common.partial_infer.utils import int64_array
from mo.front.common.replacement import FrontReplacementOp
from mo.graph.graph import Graph, Node
from mo.ops.const import Const
from mo.ops.shape import Shape

class SizeFrontReplacer(FrontReplacementOp):
    __doc__ = '\n    Replace Size op by Shape -> ReduceProd operations\n    '
    op = 'Size'
    enabled = True

    def replace_op(self, graph: Graph, node: Node):
        shape = Shape(graph, {'name': node.name + '/Shape/'}).create_node()
        reduce_prod = ReduceProd(graph, {'name':shape.name + 'ReduceProd/',  'keep_dims':False}).create_node()
        reduce_axis = Const(graph, {'value': int64_array([0])}).create_node()
        node.in_port(0).get_connection().set_destination(shape.in_port(0))
        reduce_prod.in_port(0).get_connection().set_source(shape.out_port(0))
        reduce_prod.in_port(1).get_connection().set_source(reduce_axis.out_port(0))
        return [
         reduce_prod.id]