# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mo/utils/unsupported_ops.py
# Compiled at: 2020-05-01 08:37:22
# Size of source mod 2**32: 1422 bytes
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
import collections, networkx as nx
from mo.graph.graph import Node, Graph

class UnsupportedOps(object):

    def __init__(self, graph: Graph):
        self.graph = graph
        self.unsupported = collections.defaultdict(list)

    def add(self, node: Node):
        op = node.op if node.has_valid('op') else '<UNKNOWN OP>'
        name = node.name if node.has_valid('name') else '<UNKNOWN NAME>'
        self.unsupported[op].append(name)

    def report(self, reporter, header=None):
        if len(self.unsupported) > 0:
            if header:
                reporter(header)
            for k, v in self.unsupported.items():
                reporter('    ' + str(k) + ' (' + str(len(v)) + ')')
                for node_name in v:
                    reporter('        ' + node_name)