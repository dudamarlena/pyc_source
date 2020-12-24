# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extensions/middle/TensorIterator_utils.py
# Compiled at: 2020-05-01 08:37:21
# Size of source mod 2**32: 1332 bytes
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
from mo.graph.graph import Graph, Node

def delete_selects_from(graph: Graph, node_idxs: list):
    for node_id in node_idxs:
        greater_equal = Node(graph, node_id)
        for port in greater_equal.out_port(0).get_destinations():
            port_node = port.node
            if port_node.soft_get('op') == 'Select':
                port_node.in_port(1).disconnect()
                port_node.in_port(0).disconnect()
                next_op_input_port = port_node.out_port(0).get_destination()
                select_input = port_node.in_port(2).get_source()
                next_op_input_port.get_connection().set_source(select_input)
                graph.remove_node(port_node.id)