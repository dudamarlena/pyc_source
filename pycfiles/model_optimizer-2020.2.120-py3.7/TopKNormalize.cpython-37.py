# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extensions/front/TopKNormalize.py
# Compiled at: 2020-05-01 08:37:19
# Size of source mod 2**32: 1794 bytes
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
from mo.front.common.partial_infer.utils import int64_array
from mo.front.common.replacement import FrontReplacementPattern
from mo.graph.graph import Graph
from mo.ops.const import Const
from mo.ops.result import Result

class TopKNormalize(FrontReplacementPattern):
    __doc__ = "\n    This pass do TopK layer normalization:\n        1. Adds the second input to the TopK layer if it has just one. In this case the attribute 'k' should be defined.\n        2. If one of TopK ports isn't connected - adds output on this port to keep this port in IR.\n\n    "
    enabled = True

    def find_and_replace_pattern(self, graph: Graph):
        for topk_node in graph.get_op_nodes(op='TopK'):
            if topk_node.in_port(1).disconnected():
                assert topk_node.has_valid('k'), 'The TopK node "{}" misses "k" attribute'.format(topk_node.name)
                k_node = Const(graph, {'name':topk_node.id + '/Dims',  'value':int64_array(topk_node.k)}).create_node()
                topk_node.in_port(1).connect(k_node.out_port(0))
                del topk_node['k']
            else:
                log.debug('The TopK node input "{}" is already normalized'.format(topk_node.name))