# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extensions/back/insert_compatibility_l2normalization.py
# Compiled at: 2020-05-01 08:37:19
# Size of source mod 2**32: 2094 bytes
"""
 Copyright (C) 2017-2020 Intel Corporation

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
import numpy as np, networkx as nx
from mo.ops.const import Const
from mo.ops.op import Op
from mo.graph.graph import Graph
from mo.back.replacement import BackReplacementPattern

class CompatibilityL2NormalizationPattern(BackReplacementPattern):
    force_clean_up = True
    enabled = True

    def pattern(self):
        return dict(nodes=[
         (
          'l2_normalization', dict(op='Normalize'))],
          edges=[])

    def replace_pattern(self, graph: Graph, match: dict):
        """
        Adds Normalize layer weights, which are required by Inference Engine, 
        but do not always exist in MXNet model. 
        
        L2Normalization is mapped to Normalize layer
        so we need to generate Normalize weights filled with ones.
        
        Parameters
        ----------
        graph : Graph
           Graph with loaded model.
         match : dict
           Patterns which were found in graph structure.
        """
        l2_normalization_node = match['l2_normalization']
        if len(l2_normalization_node.in_nodes()) < 2:
            value = np.full([l2_normalization_node.in_node(0).shape[1]], 1.0, dtype=(np.float32))
            weights_node = Const(graph, dict(name=(l2_normalization_node['name'] + '_weights'), value=value)).create_node()
            l2_normalization_node.add_input_port(1)
            l2_normalization_node.in_port(1).connect(weights_node.out_port(0))
            l2_normalization_node.in_port(1).bin = 'weights'