# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extensions/front/onnx/group_norm_ext.py
# Compiled at: 2020-05-01 08:37:20
# Size of source mod 2**32: 1625 bytes
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
from mo.front.extractor import FrontExtractorOp
from mo.front.onnx.extractors.utils import onnx_attr
from mo.ops.group_norm import GroupNorm

class ExperimentalDetectronGroupNorm(FrontExtractorOp):
    op = 'ExperimentalDetectronGroupNorm'
    enabled = True

    @classmethod
    def extract(cls, node):
        attrs = {'eps':np.array(onnx_attr(node, 'eps', 'f', default=1e-06), dtype=np.float), 
         'num_groups':np.array(onnx_attr(node, 'num_groups', 'i', default=1), dtype=np.int64)}
        GroupNorm.update_node_stat(node, attrs)
        return cls.enabled


class GroupNormExtractor(FrontExtractorOp):
    op = 'GroupNorm'
    enabled = True

    @classmethod
    def extract(cls, node):
        attrs = {'eps':np.array(onnx_attr(node, 'eps', 'f', default=1e-06), dtype=np.float), 
         'num_groups':np.array(onnx_attr(node, 'num_groups', 'i', default=1), dtype=np.int64)}
        GroupNorm.update_node_stat(node, attrs)
        return cls.enabled