# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extensions/front/mxnet/up_sampling_ext.py
# Compiled at: 2020-05-01 08:37:20
# Size of source mod 2**32: 3180 bytes
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
import math
from extensions.front.mxnet.conv_ext import DeconvFrontExtractor
from extensions.ops.interpolate import Interpolate
from mo.front.common.partial_infer.utils import int64_array
from mo.front.extractor import FrontExtractorOp
from mo.front.mxnet.extractors.utils import get_mxnet_layer_attrs
from mo.ops.convolution import Convolution

class UpSamplingFrontExtractor(FrontExtractorOp):
    op = 'UpSampling'
    enabled = True

    @classmethod
    def extract(cls, node):
        attrs = get_mxnet_layer_attrs(node.symbol_dict)
        scale = attrs.int('scale', 1)
        num_filter = attrs.int('num_filter', 0)
        mode = attrs.str('sample_type', None)
        if mode == 'nearest':
            node_attrs = {'factor':attrs.int('scale', 1),  'mode':mode, 
             'antialias':0, 
             'axes':int64_array([2, 3])}
            Interpolate.update_node_stat(node, node_attrs)
        else:
            if mode == 'bilinear':
                kernel = 2 * scale - scale % 2
                stride = scale
                pad = math.ceil((scale - 1) / 2)
                num_group = num_filter
                node_attrs = {'op':__class__.op, 
                 'type':'Deconvolution', 
                 'bias_addable':True, 
                 'bias_term':False, 
                 'pad':int64_array([[0, 0], [0, 0], [pad, pad], [pad, pad]]), 
                 'pad_spatial_shape':int64_array([[pad, pad], [pad, pad]]), 
                 'dilation':None, 
                 'output_spatial_shape':None, 
                 'output_shape':None, 
                 'stride':int64_array([1, 1, stride, stride]), 
                 'group':num_group, 
                 'output':num_filter, 
                 'kernel_spatial':int64_array([kernel, kernel]), 
                 'input_feature_channel':0, 
                 'output_feature_channel':1, 
                 'kernel_spatial_idx':None, 
                 'reshape_kernel':True, 
                 'spatial_dims':None, 
                 'channel_dims':int64_array([1]), 
                 'batch_dims':int64_array([0]), 
                 'layout':'NCHW', 
                 'get_pad':DeconvFrontExtractor.get_pad}
                Convolution.update_node_stat(node, node_attrs)
            return cls.enabled