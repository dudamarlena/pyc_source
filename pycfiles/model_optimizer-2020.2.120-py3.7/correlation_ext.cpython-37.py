# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extensions/front/caffe/correlation_ext.py
# Compiled at: 2020-05-01 08:37:19
# Size of source mod 2**32: 1802 bytes
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
from extensions.ops.correlation import CorrelationOp
from mo.front.caffe.collect_attributes import merge_attrs
from mo.front.common.extractors.utils import layout_attrs
from mo.front.extractor import FrontExtractorOp

class CorrelationFrontExtractor(FrontExtractorOp):
    op = 'Correlation'
    enabled = True

    @classmethod
    def extract(cls, node):
        proto_layer = node.pb
        param = proto_layer.correlation_param
        corr_type = 'caffe.CorrelationParameter.MULTIPLY'
        if param.correlation_type == 1:
            corr_type = 'caffe.CorrelationParameter.SUBTRACT'
        update_attrs = {'pad':param.pad, 
         'kernel_size':param.kernel_size, 
         'max_displacement':param.max_displacement, 
         'stride_1':param.stride_1, 
         'stride_2':param.stride_2, 
         'single_direction':param.single_direction, 
         'do_abs':int(param.do_abs), 
         'correlation_type':corr_type}
        mapping_rule = merge_attrs(param, update_attrs)
        mapping_rule.update(layout_attrs())
        CorrelationOp.update_node_stat(node, mapping_rule)
        return cls.enabled