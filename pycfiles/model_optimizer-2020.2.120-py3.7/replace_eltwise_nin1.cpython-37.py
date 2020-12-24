# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extensions/front/kaldi/replace_eltwise_nin1.py
# Compiled at: 2020-05-01 08:37:19
# Size of source mod 2**32: 2446 bytes
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
from extensions.ops.split import Split
from mo.front.common.partial_infer.utils import int64_array
from mo.front.common.replacement import FrontReplacementOp
from mo.front.tf.graph_utils import create_op_with_const_inputs
from mo.graph.graph import Node, Graph
from mo.ops.const import Const
from mo.ops.eltwise import Eltwise
from mo.ops.eltwise_n import EltwiseN
from mo.utils.error import Error

class ReplaceEltwiseNin1NodePattern(FrontReplacementOp):
    __doc__ = '\n    In nnet3 models Kaldi gather all inputs of Mul or Sum in 1. This pass separates inputs as it should be for IE.\n    '
    op = 'EltwiseNin1'
    enabled = True

    def run_after(self):
        from extensions.front.restore_ports import RestorePorts
        return [
         RestorePorts]

    def replace_op(self, graph: Graph, node: Node):
        ss_node = create_op_with_const_inputs(graph, Split, {1: int64_array(1)}, {'name':'Split_eltwise_' + node.name,  'num_splits':node['num_inputs']})
        inp = node.get_inputs()
        in_node = inp[0][0]
        edge_attrs = inp[0][1]
        (graph.add_edge)(in_node, (ss_node.id), **edge_attrs)
        if ss_node.num_splits == 2:
            eltwise_node = Eltwise(graph, attrs={'name':'Eltwise_' + node.name,  'operation':node['operation']}).create_node()
        else:
            if ss_node.num_splits > 2:
                eltwise_node = EltwiseN(graph, attrs={'name':'Eltwise_' + node.name,  'operation':node['operation']}).create_node()
            else:
                raise Error('Error on replacing Kaldi eltwise')
        for i in range(ss_node.num_splits):
            ss_node.out_port(i).get_connection().set_destination(eltwise_node.in_port(i))

        return [
         eltwise_node.id]