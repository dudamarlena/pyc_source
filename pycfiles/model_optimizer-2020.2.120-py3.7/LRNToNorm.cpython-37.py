# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extensions/back/LRNToNorm.py
# Compiled at: 2020-05-01 08:37:19
# Size of source mod 2**32: 2066 bytes
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
from mo.back.replacement import BackReplacementPattern
from mo.front.common.partial_infer.utils import int64_array
from mo.front.tf.graph_utils import create_op_node_with_second_input
from mo.graph.graph import Graph
from mo.ops.lrn import LRN

class LRN_normalization(BackReplacementPattern):
    __doc__ = '\n    Transforming LRN with `region` attribute to LRN with second `axis`-input\n    '
    enabled = True
    graph_condition = [lambda graph: graph.graph['cmd_params'].generate_experimental_IR_V10]

    def pattern(self):
        return dict(nodes=[
         (
          'lrn', dict(kind='op', op='AttributedLRN'))],
          edges=[])

    def replace_pattern(self, graph: Graph, match: dict):
        node = match['lrn']
        name = node.soft_get('name', node.id)
        assert node.has_valid('region')
        assert node.region in ('across', 'same')
        input_shape = node.in_port(0).data.get_shape()
        assert input_shape is not None
        axis = [1] if node.region == 'across' else list(range(2, input_shape.size))
        new_lrn = create_op_node_with_second_input(graph, LRN, int64_array(axis), {'name':name, 
         'alpha':node.alpha, 
         'beta':node.beta, 
         'size':node.local_size, 
         'bias':node.bias})
        node.out_port(0).get_connection().set_source(new_lrn.out_port(0))
        node.in_port(0).get_connection().set_destination(new_lrn.in_port(0))