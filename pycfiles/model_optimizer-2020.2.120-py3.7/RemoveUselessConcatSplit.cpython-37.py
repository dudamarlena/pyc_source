# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extensions/middle/RemoveUselessConcatSplit.py
# Compiled at: 2020-05-01 08:37:21
# Size of source mod 2**32: 2307 bytes
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
from mo.graph.graph import Graph
from mo.middle.replacement import MiddleReplacementPattern

class RemoveUselessConcatSplitPattern(MiddleReplacementPattern):
    __doc__ = '\n    Remove useless construction with concat and split like follows:\n         /    /   |    \\            br1  br2   ..  br(n-1)br(n)\n        \\    \\    |    /    /\n                concat\n                  |\n                split\n         /    /   |    \\            br1  br2   ..  br(n-1)br(n)\n\n    '
    enabled = True
    force_clean_up = True

    def run_after(self):
        import extensions.middle.ReplaceSpliceNodePattern as ReplaceSpliceNodePattern
        return [
         ReplaceSpliceNodePattern]

    @staticmethod
    def pattern():
        return dict(nodes=[
         (
          'concat', dict(op='Concat')),
         (
          'data', dict(kind='data')),
         (
          'split', dict(op='Split'))],
          edges=[
         ('concat', 'data'),
         ('data', 'split')])

    @staticmethod
    def replace_pattern(graph: Graph, match: dict):
        concat_node = match['concat']
        split_node = match['split']
        if len(concat_node.out_port(0).get_destinations()) != 1:
            return
        inputs = list(concat_node.in_ports().values())
        outputs = list(split_node.out_ports().values())
        if len(inputs) != len(outputs):
            return
        for i in range(len(inputs)):
            if not all(inputs[i].data.get_shape() == outputs[i].data.get_shape()):
                return

        for i in range(len(inputs)):
            outputs[i].get_connection().set_source(inputs[i].get_source())
            inputs[i].disconnect()