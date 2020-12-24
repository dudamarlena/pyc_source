# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mo/ops/deformable_convolution.py
# Compiled at: 2020-05-01 08:37:22
# Size of source mod 2**32: 1412 bytes
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
from mo.ops.convolution import Convolution
from mo.ops.op import Op

class DeformableConvolution(Op):
    op = 'DeformableConvolution'

    def __init__(self, graph, attrs):
        super().__init__(graph, {'kind':'op', 
         'type':__class__.op, 
         'op':__class__.op, 
         'infer':Convolution.infer, 
         'multiplication_transparent':True, 
         'multiplication_transparent_ports':[
          (0, 0), (2, 0)], 
         'in_ports_count':3, 
         'out_ports_count':1}, attrs)

    def backend_attrs(self):
        return Convolution(self.graph, {}).backend_attrs() + ['deformable_group', 'group']