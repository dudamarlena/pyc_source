# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extensions/middle/FuseReshapesSequence.py
# Compiled at: 2020-05-01 08:37:21
# Size of source mod 2**32: 2695 bytes
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
from extensions.middle.pass_separator import PostMiddleStart, MiddleFinish
from mo.graph.graph import Graph
from mo.middle.passes.eliminate import remove_op_node_with_data_node
from mo.middle.passes.fusing.helpers import get_next_operation
from mo.middle.replacement import MiddleReplacementPattern

class FuseReshapesSequence(MiddleReplacementPattern):
    __doc__ = '\n    Finds sequence of Reshapes operations and merge them to a single Reshape operation.\n    '
    enabled = True
    run_not_recursively = True

    def run_before(self):
        return [
         PostMiddleStart]

    def run_after(self):
        return [
         MiddleFinish]

    def find_and_replace_pattern(self, graph: Graph):
        reshape_nodes = graph.get_op_nodes(type='Reshape')
        for node in reshape_nodes:
            if not graph.has_node(node.id):
                continue
            if len(node.out_port(0).get_destinations()) == 1:
                log.debug('First phase for Reshape: {}'.format(node.soft_get('name')))
                next_op = get_next_operation(node)[0]
                log.debug('second node: id={}, type={}'.format(next_op.soft_get('id'), next_op.soft_get('type')))
                if next_op.has_valid('type'):
                    if next_op.type == 'Reshape':
                        dim_value = next_op.in_port(1).data.get_value()
                        if dim_value is None or 0 in dim_value or -1 in dim_value:
                            continue
                    log.debug('Second phase for Reshape: {}'.format(node.soft_get('name')))
                    remove_op_node_with_data_node(graph, node)