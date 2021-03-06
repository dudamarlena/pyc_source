# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extensions/back/ShufflenetReLUReorder.py
# Compiled at: 2020-05-01 08:37:19
# Size of source mod 2**32: 2938 bytes
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
from mo.back.replacement import BackReplacementPattern
from mo.graph.graph import Graph

class ShufflenetReLUReorder(BackReplacementPattern):
    __doc__ = '\n    This pass is workaround for GPU plugin\n    '
    enabled = False

    def run_before(self):
        import extensions.back.TransposeToPermute as TransposeToPermute
        return [
         TransposeToPermute]

    def pattern(self):
        return dict(nodes=[
         (
          'relu', dict(kind='op', type='ReLU')),
         (
          'relu_data', dict(kind='data')),
         (
          'reshape1', dict(kind='op', type='Reshape')),
         (
          'reshape1_data', dict(kind='data')),
         (
          'transpose', dict(kind='op', type='Transpose')),
         (
          'transpose_data', dict(kind='data')),
         (
          'reshape2', dict(kind='op', type='Reshape')),
         (
          'reshape2_data', dict(kind='data')),
         (
          'conv', dict(kind='op', type='Convolution'))],
          edges=[
         ('relu', 'relu_data'),
         ('relu_data', 'reshape1'),
         ('reshape1', 'reshape1_data'),
         ('reshape1_data', 'transpose'),
         ('transpose', 'transpose_data'),
         ('transpose_data', 'reshape2'),
         ('reshape2', 'reshape2_data'),
         ('reshape2_data', 'conv')])

    def replace_pattern(self, graph: Graph, match: dict):
        relu = match['relu']
        reshape1 = match['reshape1']
        reshape2_data = match['reshape2_data']
        conv = match['conv']
        if np.max(conv.pad) == 0:
            return
        relu_input = relu.in_node()
        edge_attrs = graph.get_edge_data(relu.out_node().id, reshape1.id)[0]
        graph.remove_edge(relu_input.id, relu.id)
        graph.remove_edge(relu.out_node().id, reshape1.id)
        graph.add_edges_from([(relu_input.id, reshape1.id, edge_attrs)])
        edge_attrs = graph.get_edge_data(reshape2_data.id, conv.id)[0]
        graph.remove_edge(reshape2_data.id, conv.id)
        graph.add_edges_from([(reshape2_data.id, relu.id, {'in': 0}), (relu.out_node().id, conv.id, edge_attrs)])