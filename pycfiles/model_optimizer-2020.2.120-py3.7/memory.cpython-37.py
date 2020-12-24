# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mo/ops/memory.py
# Compiled at: 2020-05-01 08:37:22
# Size of source mod 2**32: 2719 bytes
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
from mo.front.common.partial_infer.elemental import copy_shape_infer
from mo.front.common.partial_infer.utils import int64_array
from mo.graph.graph import Node, Graph
from mo.middle.passes.convert_data_type import data_type_str_to_np
from mo.ops.op import Op
from mo.utils.error import Error
from mo.utils.utils import refer_to_faq_msg

class Memory(Op):
    op = 'Memory'
    enabled = True

    def __init__(self, graph, attrs):
        super().__init__(graph, {'type':'Memory', 
         'op':'Memory', 
         'id':None, 
         'size':None, 
         'index':None, 
         'infer':Memory.infer, 
         'in_ports_count':1, 
         'out_ports_count':1, 
         'type_infer':__class__.type_infer}, attrs)

    def supported_attrs(self):
        return [
         'id', 'size', 'index']

    @staticmethod
    def infer(node: Node):
        if len(node.in_nodes()) > 0:
            copy_shape_infer(node)
            return
        if node.has_valid('shape'):
            batch = 1
            for out_node in node.out_nodes().values():
                out_node.shape = int64_array([batch, *node.shape[:]])

            return
        raise Error('Model Optimizer is unable to calculate output shape of Memory node {}. ' + refer_to_faq_msg(88), node.id)

    @staticmethod
    def type_infer(node: Node):
        if node.has_valid('dst_type'):
            node.out_port(0).set_data_type(node.dst_type)
        else:
            node.out_port(0).set_data_type(data_type_str_to_np(node.graph.graph['cmd_params'].data_type))