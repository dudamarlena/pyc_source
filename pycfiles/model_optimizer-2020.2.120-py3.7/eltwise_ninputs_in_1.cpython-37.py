# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mo/ops/eltwise_ninputs_in_1.py
# Compiled at: 2020-05-01 08:37:22
# Size of source mod 2**32: 1343 bytes
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
from mo.utils.error import Error

class EltwiseNin1(Op):
    __doc__ = '\n    The elementwise operation that has all inputs in 1 input. This operation is replaced in a front phase with\n    a number of simple elementwise operations with 2 inputs.\n    '
    op = 'EltwiseNin1'

    def __init__(self, graph, attrs):
        super().__init__(graph, {'op':__class__.op, 
         'type':None, 
         'infer':None, 
         'out_ports_count':1}, attrs)
        if 'operation' not in self.attrs:
            raise Error('"operation" attribute is not set for operation "{}".'.format(__class__.op))