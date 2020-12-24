# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extensions/front/onnx/parameter_ext.py
# Compiled at: 2020-05-01 08:37:20
# Size of source mod 2**32: 1187 bytes
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
from onnx.mapping import TENSOR_TYPE_TO_NP_TYPE
from extensions.ops.parameter import Parameter
from mo.front.extractor import FrontExtractorOp

class PlaceholderFrontExtractor(FrontExtractorOp):
    op = 'Parameter'
    enabled = True

    @classmethod
    def extract(cls, node):
        t_type = node.pb.type.tensor_type
        attrs = {'shape':np.array([d.dim_value for d in t_type.shape.dim], dtype=np.int64), 
         'data_type':TENSOR_TYPE_TO_NP_TYPE[t_type.elem_type]}
        Parameter.update_node_stat(node, attrs)
        return cls.enabled