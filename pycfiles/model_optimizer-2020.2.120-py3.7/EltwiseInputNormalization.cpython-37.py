# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extensions/middle/EltwiseInputNormalization.py
# Compiled at: 2020-05-01 08:37:21
# Size of source mod 2**32: 2168 bytes
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
import networkx as nx, numpy as np
import extensions.middle.EltwiseInputReshape as EltwiseInputReshape
from mo.graph.graph import Graph
from mo.middle.replacement import MiddleReplacementPattern

class EltwiseInputNormalize(EltwiseInputReshape, MiddleReplacementPattern):
    enabled = False

    def find_and_replace_pattern(self, graph):
        eltwise_nodes = graph.get_op_nodes(is_eltwise=True)
        for node in eltwise_nodes:
            output_shape = node.out_node().shape
            for in_node in node.in_nodes().values():
                if len(in_node.shape) != len(output_shape):
                    new_shape = in_node.shape
                    for x in range(len(output_shape) - len(in_node.shape)):
                        new_shape = np.insert(new_shape, 0, 1)

                    nx.set_edge_attributes(G=(node.graph), values={(
 in_node.id, node.id, 0): new_shape},
                      name='new_shape')

        super().find_and_replace_pattern(graph)