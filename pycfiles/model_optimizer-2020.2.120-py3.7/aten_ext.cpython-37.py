# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extensions/front/onnx/aten_ext.py
# Compiled at: 2020-05-01 08:37:20
# Size of source mod 2**32: 1189 bytes
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
from extensions.ops.aten import ATen
from mo.front.extractor import FrontExtractorOp
from mo.front.onnx.extractors.utils import onnx_attr

class ATenFrontExtractor(FrontExtractorOp):
    op = 'ATen'
    enabled = True

    @classmethod
    def extract(cls, node):
        mode = onnx_attr(node, 'mode', 'i', default=1)
        operator = onnx_attr(node, 'operator', 's').decode()
        scale_grad_by_freq = onnx_attr(node, 'scale_grad_by_freq', 'i', default=0)
        ATen.update_node_stat(node, {'operator':operator,  'mode':mode,  'scale_grad_by_freq':scale_grad_by_freq})
        return cls.enabled