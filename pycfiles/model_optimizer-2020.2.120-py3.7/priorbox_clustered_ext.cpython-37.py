# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extensions/front/onnx/priorbox_clustered_ext.py
# Compiled at: 2020-05-01 08:37:20
# Size of source mod 2**32: 2115 bytes
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
from extensions.ops.priorbox_clustered import PriorBoxClusteredOp
from mo.front.extractor import FrontExtractorOp
from mo.front.onnx.extractors.utils import onnx_attr

class PriorBoxClusteredFrontExtractor(FrontExtractorOp):
    op = 'PriorBoxClustered'
    enabled = True

    @classmethod
    def extract(cls, node):
        variance = onnx_attr(node, 'variance', 'floats', default=[], dst_type=(lambda x: np.array(x, dtype=(np.float32))))
        if len(variance) == 0:
            variance = [
             0.1]
        update_attrs = {'width':onnx_attr(node, 'width', 'floats', dst_type=lambda x: np.array(x, dtype=(np.float32))), 
         'height':onnx_attr(node, 'height', 'floats', dst_type=lambda x: np.array(x, dtype=(np.float32))), 
         'flip':onnx_attr(node, 'flip', 'i', default=0), 
         'clip':onnx_attr(node, 'clip', 'i', default=0), 
         'variance':list(variance), 
         'img_size':onnx_attr(node, 'img_size', 'i', default=0), 
         'img_h':onnx_attr(node, 'img_h', 'i', default=0), 
         'img_w':onnx_attr(node, 'img_w', 'i', default=0), 
         'step':onnx_attr(node, 'step', 'f', default=0.0), 
         'step_h':onnx_attr(node, 'step_h', 'f', default=0.0), 
         'step_w':onnx_attr(node, 'step_w', 'f', default=0.0), 
         'offset':onnx_attr(node, 'offset', 'f', default=0.0)}
        PriorBoxClusteredOp.update_node_stat(node, update_attrs)
        return cls.enabled