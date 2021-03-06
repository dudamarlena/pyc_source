# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mo/ops/constant_of_shape.py
# Compiled at: 2020-05-01 08:37:22
# Size of source mod 2**32: 1266 bytes
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
from mo.ops.op import Op

class ConstantOfShape(Op):
    __doc__ = " Create a tensor of the shape specified in the first input with all values equal to attribute 'value'.\n    The operation is converted to Broadcast operation\n    "
    op = 'ConstantOfShape'
    enabled = True

    def __init__(self, graph, attrs):
        super().__init__(graph, {'kind':'op', 
         'type':None, 
         'op':__class__.op, 
         'in_ports_count':1, 
         'out_ports_count':1, 
         'fill_value':0, 
         'infer':None}, attrs)

    def supported_attrs(self):
        return [
         'fill_value']