# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extensions/front/onnx/deformable_conv_ext.py
# Compiled at: 2020-05-01 08:37:20
# Size of source mod 2**32: 3805 bytes
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
from mo.front.onnx.extractors.utils import onnx_attr, get_onnx_autopad
from mo.ops.deformable_convolution import DeformableConvolution
from mo.utils.error import Error
from mo.front.common.partial_infer.utils import int64_array

class DeformableConvExtractor(FrontExtractorOp):
    op = 'DeformableConv2D'
    enabled = True

    @classmethod
    def extract(cls, node):
        pads = onnx_attr(node, 'pads', 'ints', default=None, dst_type=(lambda x: np.array(x, dtype=(np.int64))))
        if not pads is None:
            assert len(pads) % 2 == 0
        final_pad = None
        if pads is not None:
            pads = pads.reshape([2, -1])
            pads = np.transpose(pads)
            final_pad = np.array([[0, 0], [0, 0], *pads], dtype=(np.int64))
        dilations = onnx_attr(node, 'dilations', 'ints', default=None, dst_type=(lambda x: np.array(x, dtype=(np.int64))))
        final_dilations = np.array([1, 1, *dilations], dtype=(np.int64)) if dilations is not None else None
        strides = onnx_attr(node, 'strides', 'ints', default=None, dst_type=(lambda x: np.array(x, dtype=(np.int64))))
        final_strides = np.array([1, 1, *strides], dtype=(np.int64)) if strides is not None else None
        kernel_shape = onnx_attr(node, 'kernel_shape', 'ints', default=None)
        auto_pad = onnx_attr(node, 'auto_pad', 's', default=None, dst_type=get_onnx_autopad)
        group = onnx_attr(node, 'group', 'i', default=1, dst_type=(lambda x: np.array(x, dtype=(np.int64))))
        deformable_groups = onnx_attr(node, 'deformable_groups', 'i', default=1)
        attrs = {'op':__class__.op, 
         'auto_pad':auto_pad, 
         'bias_addable':False, 
         'bias_term':False, 
         'pad':final_pad, 
         'pad_spatial_shape':np.array(pads, dtype=(np.int64)) if pads is not None else None, 
         'dilation':final_dilations, 
         'output_spatial_shape':None, 
         'output_shape':None, 
         'stride':final_strides, 
         'group':group, 
         'deformable_group':deformable_groups, 
         'output':None, 
         'weights_index':2, 
         'kernel_spatial':np.array(kernel_shape, dtype=(np.int64)) if kernel_shape is not None else None, 
         'input_feature_channel':1, 
         'output_feature_channel':0, 
         'kernel_spatial_idx':None, 
         'spatial_dims':None, 
         'channel_dims':np.array([1], dtype=np.int64), 
         'batch_dims':np.array([0], dtype=np.int64), 
         'layout':'NCHW'}
        DeformableConvolution.update_node_stat(node, attrs)
        return cls.enabled