# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extensions/ops/aten.py
# Compiled at: 2020-05-01 08:37:21
# Size of source mod 2**32: 1035 bytes
"""
 Copyright (c) 2020 Intel Corporation

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
from mo.front.common.partial_infer.utils import int64_array
from mo.graph.graph import Node, Graph
from mo.ops.op import Op

class ATen(Op):
    op = 'ATen'
    enabled = False

    def __init__(self, graph, attrs):
        super().__init__(graph, {'op':self.op, 
         'type':None, 
         'infer':None}, attrs)

    def supported_attrs(self):
        return [
         'mode', 'operator', 'scale_grad_by_freq']