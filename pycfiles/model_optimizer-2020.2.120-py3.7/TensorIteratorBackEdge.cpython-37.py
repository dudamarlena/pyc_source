# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extensions/middle/TensorIteratorBackEdge.py
# Compiled at: 2020-05-01 08:37:21
# Size of source mod 2**32: 5524 bytes
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
import logging as log
from extensions.middle.TensorIteratorCondition import DynamicDecoderConditionMatcher
from extensions.ops.TensorIterator_ops import TensorIteratorBackEdge, TensorIteratorOutput
from mo.graph.graph import Graph
from mo.middle.replacement import MiddleReplacementPattern

class BackEdgesMatching(MiddleReplacementPattern):
    __doc__ = '\n    This pattern are needed for matching back edges in while loops in TF graphs.\n    Back edge is a chain of nodes in while loop that iterate one variable in graph over loop steps. It consist of\n    nodes:\n                        Exit (optional)\n                            ^\n                            |\n    Enter () -> Merge -> Switch -> Identity -> SOME OPERATIONS -> NextIteration ->\n                ^                                                                 |\n                |                                                                 |\n                ------------------------------------------------------------------\n    The structure of pattern without Data nodes between ops (every node is named as op attribute of this node):\n                Data--\n                      |\n        NextIteration -> Merge--\n                                |\n                                ->Switch (out=1) -> Identity\n                                |\n       TensorIteratorCondition--\n    '
    enabled = True
    graph_condition = [lambda graph: graph.graph['is_cyclic']]

    def run_after(self):
        from extensions.middle.TensorIteratorCondition import SimpleConditionMatcher
        return [
         DynamicDecoderConditionMatcher]

    def run_before(self):
        import extensions.middle.TensorIteratorMerge as TensorIteratorMerge
        return [
         TensorIteratorMerge]

    @staticmethod
    def pattern():
        return dict(nodes=[
         (
          'Enter_1_data', dict(kind='data')),
         (
          'Merge_1', dict(kind='op', op='Merge')),
         (
          'Merge_1_data', dict(kind='data')),
         (
          'Switch_1', dict(kind='op', op='Switch')),
         (
          'Switch_1_data', dict(kind='data')),
         (
          'Identity_1', dict(kind='op', op='Identity')),
         (
          'Identity_1_data', dict(kind='data')),
         (
          'NextIteration', dict(kind='op', op='NextIteration')),
         (
          'NextIteration_data', dict(kind='data')),
         (
          'condition', dict(kind='op', op='TensorIteratorCondition')),
         (
          'condition_cond_data', dict(kind='data'))],
          edges=[
         ('Enter_1_data', 'Merge_1'),
         ('Merge_1', 'Merge_1_data'),
         ('Merge_1_data', 'Switch_1'),
         (
          'Switch_1', 'Switch_1_data', {'out': 1}),
         ('Switch_1_data', 'Identity_1'),
         ('Identity_1', 'Identity_1_data'),
         ('NextIteration', 'NextIteration_data'),
         ('NextIteration_data', 'Merge_1'),
         ('condition', 'condition_cond_data'),
         ('condition_cond_data', 'Switch_1')])

    def replace_pattern(self, graph: Graph, match: dict):
        log.debug('================== BackEdgeFind ===============')
        nodes_for_remove = []
        from_body_data = match['NextIteration'].in_node()
        if 0 in match['Switch_1'].out_nodes():
            Exit = match['Switch_1'].out_node(0).out_node(0)
            if not (Exit.has_valid('op') and Exit.op == 'Exit'):
                raise AssertionError
            output_data = Exit.out_node(0)
            nodes_for_remove.append(match['Switch_1'].out_node(0).id)
            nodes_for_remove.append(Exit.id)
            output = TensorIteratorOutput(graph, dict(external_port_id=None, internal_layer_id=None,
              name=(Exit.name + '/TensorIteratorOutput_')))
            output.create_node_with_data(inputs=[from_body_data, match['condition_cond_data']], data_nodes=[
             output_data])
        assert match['NextIteration_data'].id != match['Enter_1_data'].id
        backedge = TensorIteratorBackEdge(graph, dict(name=(match['Identity_1'].name + '/TensorIteratorBackEdge_')))
        backedge.create_node_with_data(inputs=[match['Enter_1_data'], from_body_data, match['condition_cond_data']], data_nodes=[
         match['Identity_1_data']])
        safe_nodes = [
         'Identity_1_data', 'condition', 'condition_cond_data', 'Enter_1_data']
        for node in match.keys():
            if node not in safe_nodes:
                nodes_for_remove.append(match[node].id)

        graph.remove_nodes_from(nodes_for_remove)