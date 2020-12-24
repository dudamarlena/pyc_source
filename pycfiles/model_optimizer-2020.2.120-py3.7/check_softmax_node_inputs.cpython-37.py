# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extensions/front/mxnet/check_softmax_node_inputs.py
# Compiled at: 2020-05-01 08:37:20
# Size of source mod 2**32: 1783 bytes
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
from mo.front.common.replacement import FrontReplacementPattern
from mo.graph.graph import Graph

class CheckSoftmaxNodeInputs(FrontReplacementPattern):
    enabled = True

    def run_before(self):
        from extensions.front.user_data_repack import UserDataRepack
        return [
         UserDataRepack]

    def run_after(self):
        return []

    @staticmethod
    def pattern():
        return dict(nodes=[
         (
          'softmax', dict(op=(lambda op: op in ('SoftMax', 'SoftmaxActivation', 'SoftmaxOutput'))))],
          edges=[])

    @staticmethod
    def replace_pattern(graph: Graph, match: dict):
        """
        Need to remove from softmax layer all unused inputs
        Parameters
        ----------
        graph : Graph
           Graph with loaded model.
         match : dict
           Patterns which were found in graph structure.
        """
        softmax_node = match['softmax']
        softmax_nodes_len = len(softmax_node.in_nodes())
        for i in reversed(range(1, softmax_nodes_len)):
            in_node = softmax_node.in_node(i)
            graph.remove_edge(in_node.id, softmax_node.id)
            graph.remove_node(in_node.id)