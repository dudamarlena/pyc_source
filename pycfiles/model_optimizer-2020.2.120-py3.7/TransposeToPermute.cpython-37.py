# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extensions/back/TransposeToPermute.py
# Compiled at: 2020-05-01 08:37:19
# Size of source mod 2**32: 1599 bytes
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
import extensions.back.OptimizeTransposeReshapeSequence as OptimizeTransposeReshapeSequence
from mo.back.replacement import BackReplacementPattern
from mo.graph.graph import Graph
from mo.ops.permute import Permute

class TransposeToPermute(BackReplacementPattern):
    enabled = True
    graph_condition = [lambda graph: not graph.graph['cmd_params'].generate_experimental_IR_V10]
    force_clean_up = True

    def run_after(self):
        return [
         OptimizeTransposeReshapeSequence]

    @staticmethod
    def pattern():
        return dict(nodes=[
         (
          'transpose', dict(type='Transpose'))],
          edges=[])

    @staticmethod
    def replace_pattern(graph: Graph, match: dict):
        node = match['transpose']
        order = node.in_port(1).data.get_value()
        assert order is not None
        Permute.update_node_stat(node=node, attrs={'order': order.copy()})
        node['force_precision_in_ports'] = None
        node.in_port(1).disconnect()