# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mo/front/common/partial_infer/batch_norm.py
# Compiled at: 2020-05-01 08:37:21
# Size of source mod 2**32: 1109 bytes
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
import numpy as np
from mo.front.common.partial_infer.elemental import copy_shape_infer
from mo.front.common.partial_infer.utils import mark_input_bins
from mo.graph.graph import Node

def batch_norm_4_infer(node: Node):
    copy_shape_infer(node)
    mark_input_bins(node, ['weights', 'biases', 'mean', 'variance'])
    if node.has('fix_gamma'):
        if node.fix_gamma:
            node.in_node(1).value = np.full_like((node.in_node(1).value), 1, dtype=(np.float32))