# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extensions/back/kaldi_remove_memory_output.py
# Compiled at: 2020-05-01 08:37:19
# Size of source mod 2**32: 2186 bytes
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
from mo.graph.graph import Graph

class KaldiRemoveMemoryOutputBackReplacementPattern(BackReplacementPattern):
    enabled = True

    def run_after(self):
        from extensions.back.pass_separator import BackFinish
        return [
         BackFinish]

    def run_before(self):
        from extensions.back.SpecialNodesFinalization import RemoveOutputOps
        return [
         RemoveOutputOps]

    @staticmethod
    def pattern():
        return dict(nodes=[
         (
          'memory_node', dict(op='Memory')),
         (
          'data_node', dict(kind='data')),
         (
          'op_output', dict(op='Result'))],
          edges=[
         ('memory_node', 'data_node'),
         ('data_node', 'op_output')])

    @staticmethod
    def replace_pattern(graph: Graph, match: dict):
        """
        Need to find the pattern: Memory -> Data -> Result

        It is needed to make Memory nodes appear in IR,
        but they are output nodes by default and we remove the Result node after each output memory.

        DO NOT use graph clean up after it
        otherwise Memory nodes would be removed as they are not on the path from input to output

        Parameters
        ----------
        graph : Graph
           Graph with loaded model.
        match : dict
           Patterns which were found in graph structure.
        """
        memory = match['memory_node']
        data = match['data_node']
        graph.remove_edge(memory.id, data.id)
        graph.remove_node(data.id)