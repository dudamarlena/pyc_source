# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mo/middle/passes/fusing/helpers.py
# Compiled at: 2020-05-01 08:37:22
# Size of source mod 2**32: 4403 bytes
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
from collections import deque
from mo.graph.graph import Node
from mo.graph.port import Port

def get_value_id(node: Node):
    assert node.has_valid('op')
    value_id = None
    for port, in_node in node.in_nodes().items():
        if in_node.has_valid('value'):
            if value_id:
                return
            value_id = port

    return value_id


def get_tensor_id(node: Node):
    assert node.has_valid('op')
    tensor_id = None
    for port, in_node in node.in_nodes().items():
        if in_node.has_valid('value') or tensor_id:
            return
            tensor_id = port

    return tensor_id


def get_tensor_in_port(node) -> Port:
    tensor_ports = []
    for port in node.in_ports().values():
        if port.data.get_value() is None:
            tensor_ports.append(port)

    if len(tensor_ports) != 1:
        return
    return tensor_ports[0]


def get_value_in_port(node) -> Port:
    value_ports = []
    for port in node.in_ports().values():
        if port.data.get_value() is not None:
            value_ports.append(port)

    if len(value_ports) != 1:
        return
    return value_ports[0]


def common_bfs(start_node: Node, allowed_ops: list, op_name: list, is_backward: bool=True, allowed_all: bool=False):
    """
    The purpose of this algorithm is to find layers with 'op_name' located in given direction.
    In case of branching algorithm goes into each branch, but if it can't find layer in one of them it returns
    empty list.

    :param start_node: Start node for BFS algorithm
    :param allowed_ops: List of operations that we can jump over
    :param op_name: The list with names of operations for searching
    :param is_backward: The direction of BFS algorithm
    :param allowed_all: Bool flag meaning we can jump over all operations
    """
    ret = []
    q = deque([start_node])
    used = []
    while len(q) != 0:
        node = q.popleft()
        if node.id in used:
            log.debug('[BFS:ERROR] Graph contains cycle! BFS starts from {} node'.format(start_node.id))
            return []
        used.append(node.id)
        in_nodes_size = len(node.in_nodes()) if is_backward else len(node.out_nodes())
        for id in range(in_nodes_size):
            pnode = node.in_node(id) if is_backward else node.out_node(id)
            if pnode.has_valid('type'):
                if pnode.type in op_name:
                    if pnode.id not in ret:
                        ret.append(pnode.id)
                    else:
                        if allowed_all or pnode.op in allowed_ops:
                            q.append(pnode)
                        else:
                            return []
                elif pnode.kind == 'data' and pnode.value is None:
                    if is_backward:
                        if not is_backward or len(pnode.out_nodes()) == 1:
                            q.append(pnode)

    return [Node(start_node.graph, x) for x in ret]


def forward_bfs(start_node: Node, allowed_ops: list, op_name: list, allowed_all: bool=False):
    return common_bfs(start_node, allowed_ops, op_name, False, allowed_all=allowed_all)


def backward_bfs(start_node: Node, allowed_ops: list, op_name: list, allowed_all: bool=False):
    return common_bfs(start_node, allowed_ops, op_name, allowed_all=allowed_all)


def get_next_operation(node: Node):
    """
    This function returns next op node, so node should be an operation
    """
    assert node.kind == 'op'
    out_nodes = node.out_nodes()
    res = []
    for port, out_node in out_nodes.items():
        op_nodes = out_node.out_nodes()
        for op_node in op_nodes:
            if op_node.id not in [n.id for n in res]:
                res.append(op_node)

    return res