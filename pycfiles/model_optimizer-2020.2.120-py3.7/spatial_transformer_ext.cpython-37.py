# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extensions/front/caffe/spatial_transformer_ext.py
# Compiled at: 2020-05-01 08:37:19
# Size of source mod 2**32: 1693 bytes
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
from extensions.ops.spatial_transformer import SpatialTransformOp
from mo.front.caffe.collect_attributes import merge_attrs
from mo.front.extractor import FrontExtractorOp

class SpatialTransformFrontExtractor(FrontExtractorOp):
    op = 'SpatialTransformer'
    enabled = True

    @classmethod
    def extract(cls, node):
        proto_layer = node.pb
        param = proto_layer.st_param
        update_attrs = {'transform_type':param.transform_type, 
         'sampler_type':param.sampler_type, 
         'output_H':param.output_H, 
         'output_W':param.output_W, 
         'to_compute_dU':int(param.to_compute_dU), 
         'theta_1_1':param.theta_1_1, 
         'theta_1_2':param.theta_1_2, 
         'theta_1_3':param.theta_1_3, 
         'theta_2_1':param.theta_2_1, 
         'theta_2_2':param.theta_2_2, 
         'theta_2_3':param.theta_2_3}
        mapping_rule = merge_attrs(param, update_attrs)
        SpatialTransformOp.update_node_stat(node, mapping_rule)
        return cls.enabled